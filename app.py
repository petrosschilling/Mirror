from model.mirror import *
from db.dba import *


class MirroringValidator():

    def __init__(self):
        pass

    def run():

        # Databases Configuration
        dbconfig1 = DBConfiguration()
        dbconfig1.usr = "root"
        dbconfig1.pwd = "LK3isMyL1feNowMySQL"
        dbconfig1.host = "203.98.82.40"
        dbconfig1.databse = "mystro"

        dbconfig2 = DBConfiguration()
        dbconfig2.usr = "root"
        dbconfig2.pwd = "LK3isMyL1feNowMySQL"
        dbconfig2.host = "203.98.82.40"
        dbconfig2.databse = "mystro"

        # Table Fields that will be checked/included in the hash string
        fields_mapping = [
            FieldLink("list_priority", "list_priority"),
            FieldLink("archive", "archive"),
            FieldLink("created", "created")
        ]

        mirror = Mirror(
            dbconfig1,
            dbconfig2,
            "StaticExpenseTypes",
            "StaticExpenseTypes",
            fields_mapping
        )

        # Retrieve all data from database as dictionary
        # TODO Retrieving the data is working but all the data is 4GB
        # total.
        # Check for the possibility of querying chunks of data from a
        # temporarytable.
        mirror.load_db_data()
        mirror.sort_data()
        # print(mirror.data1)
        # print("###########")
        # print(mirror.data2)

        # TODO generate a hash for each row based on the fields
        # included in the mapping

        # TODO include data in buckets, the bucket id will be the
        # hash key.
        # This way we ensure that a mapping 1 to 1 exists for records
        # with repeated data.

        # TODO for hashes without pair must inclue an error


MirroringValidator.run()



