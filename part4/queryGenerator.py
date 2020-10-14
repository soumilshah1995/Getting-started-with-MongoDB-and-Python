try:
    import os
    import pandas as pd
    import sys
    import io
    import json

    import pymongo
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    from bson.son import SON

    print("All Modules loaded ")
except Exception as e:
    print("Error : {} ".format(e))


class QueryGenerator(object):
    def __init__(self):
        self.__base_query = {
            "$facet":{

            }
        }

    def __str__(self):
        return "Mongo Db Query Generator"

    def add_aggregation(self, feildName=None, limit=5, columnName=None):
        """
        addAggreadtion is withouth the Range

        X : 22
        Y: 77
        Above example shows  this is how you will receive aggreation

        :param feildName: str
        :param limit: int
        :param columnName: str
        :return:str
        """
        try:
            if feildName is None and columnName is None:
                return "Please Provide  valid feild Name and columnName for Aggreation "
            else:
                _ = {
                    "{}".format(feildName):[
                        {"$unwind": "${}".format(feildName) },
                        { "$sortByCount": "${}".format(feildName) },
                        { "$limit": limit}
                    ]
                }
                self.__base_query['$facet'][columnName] = _.get(feildName)
                print("Query Added ")
                return "Query Added "
        except Exception as e:
            return "Error"

    def add_aggregation_range(self, columnName=None,feildName=None,limit=5 ):
        """
        This will add Query for Range Based Aggreation in MongoDb

        This will add Query for $bucketAuto

        :param columnName: str
        :param feildName: str
        :param limit: int
        :return: str
        """
        try:
            if columnName is None or feildName is None:
                return "Please Provide Valid columnName and  feildName "
            else:
                _ = {
                    "{}".format(columnName):[
                        {
                            "$bucketAuto":{
                                "groupBy": "${}".format(feildName),
                                "buckets": limit

                            }

                        }
                    ]
                }
                self.__base_query['$facet'][columnName] = _.get(columnName)
                print("Query Added ")
        except Exception as e:
            pass

    @property
    def completeAggreation(self):
        return  [self.__base_query]


def main():
    _helper = QueryGenerator()
    rule1 = _helper.add_aggregation(feildName='rating',columnName='Rating', limit=5)
    rule1 = _helper.add_aggregation_range(feildName='cast',columnName='Cast', limit=5)
    query = _helper.completeAggreation
    print(json.dumps(query , indent=3))

if __name__ == "__main__":
    main()