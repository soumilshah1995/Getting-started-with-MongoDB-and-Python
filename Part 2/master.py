__NAME__ = "Soumil Nitin Shah "
__VERSION__ = "0.0.1"


try:
    import os
    import pandas as pd
    import sys
    import io
    import pymongo
    import json
    from pymongo import MongoClient
    from bson.objectid import ObjectId
    print("All Modules loaded ")
except Exception as e:
    print("Error : {} ".format(e))


class Singleton(type):

    """This would be a Singleton  Design pattern """

    _instance = {}

    def __call__(cls, *args, **kwargs):
        """Creates one one instance of the class """
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class Settings(metaclass=Singleton):
    def __init__(self, host=None, maxPoolSize=50, port=27010):
        self.host = host
        self.maxPoolSize = maxPoolSize
        self.port = port


class Client(metaclass=Singleton):

    def __init__(self, _settings=None):
        self.settings = _settings
        self.mclient = MongoClient(host=self.settings.host,
                                    port=self.settings.port,
                                    maxPoolSize=self.settings.maxPoolSize)


class MongoInsert(object):

    def __init__(self, _client=None, dbName=None, collectionName=None):
        self.client = _client
        self.dbName=dbName
        self.collectionName=collectionName

    def insert_one(self, record={}):
        """
        Insert record in Mongo DB
        :param record: Json
        :return: Bool
        """
        try:
            self.client.mclient[self.dbName][self.collectionName].insert_one(record)
            return True
        except Exception as e:
            print("Error : {} ".format(e))
            return False

    def insert_pandas_df(self,df=None):
        """

        :param df: Pandas DF
        :return: Bool
        """

        try:
            self.client.mclient[self.dbName][self.collectionName].insert_many(df.to_dict(), ordered=False)
            return True
        except Exception as e:
            return False


class Mongoinformation(object):

    def __init__(self, _client=None):
        self.client = _client

    def getALllDatabase(self):
        """
        Rreturn all Database Name in Mongo Db
        :return: List
        """
        return self.client.mclient.list_database_names()

    def getAllCollections(self, DbName=None):
        """

        :param DbName: Str
        :return: List
        """
        if DbName is None:
            return []
        else:
            self.client.mclient[DbName].list_collection_names()


class Mongoose(object):

    """facade Class """

    def __init__(self, host=None,port=27010, maxPoolSize=50,dbName=None, collectionName=None):
        self._settings =Settings(host=host, port=port, maxPoolSize=maxPoolSize)     # Cretes a instance of settings class
        self.client = Client(_settings=self._settings)                              # creates a single instance of client object
        self.dbName=dbName
        self.collectionNam = collectionName
        self._insert = MongoInsert(_client=self.client, dbName=self.dbName,collectionName=self.collectionNam)

    def insert_one_record(self, record):
        return self._insert.insert_one(record=record)


def main1():
    _helper = Mongoose(host="mongodb://root:rootpassword@localhost:27017",dbName='person',collectionName='names')
    _record = {"name":"Nitin  shah"}
    _helper.insert_one_record(record=_record)


#
# def main():
#
#     url = "mongodb://root:rootpassword@localhost:27017"
#
#     # Cretes a instance of settings class
#     _settings = Settings(host=url)
#
#     # creates a single instance of client object
#     _client = Client(_settings=_settings)
#
#     _record = {"name":"Soumil shah"}
#     dbName= "person"
#     collectionName = "names"
#
#     _helper = MongoInsert(_client=_client, dbName=dbName,collectionName=collectionName)
#     res = _helper.insert_one(record=_record)
#     print(res)


if __name__ == "__main__":
    main1()

