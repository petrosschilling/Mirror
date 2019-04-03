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
            FieldLink("expense_type_id", "expense_type_id", isid=True),
            FieldLink("list_priority", "list_priority"),
            FieldLink("archive", "archive"),
            FieldLink("created", "created"),
            FieldLink("updated", "updated")
        ]

        mirror = Mirror(
            dbconfig1,
            dbconfig2,
            "StaticExpenseTypes",
            "StaticExpenseTypes_copy",
            fields_mapping
        )

        # Retrieve all data from database as dictionary
        # TODO Retrieving the data is working but all the data is 4GB
        # total.
        # Check for the possibility of querying chunks of data from a
        # temporarytable.
        mirror.run_diff()

        # TODO Export to excel

MirroringValidator.run()
