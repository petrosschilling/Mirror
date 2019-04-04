from model.mirror import *
from db.dba import *


def yn_to_yesno(arg):
    if arg == "Y" or arg == "y":
        return "yes"
    elif arg == "N" or arg == "N":
        return "no"
    else:
        return arg

class MirroringValidator():

    def __init__(self):
        pass

    def run():

        dbconfig1 = DBConfiguration()
        dbconfig1.usr = "root"
        dbconfig1.pwd = "LK3isMyL1feNowMySQL"
        dbconfig1.host = "203.98.82.40"
        dbconfig1.databse = "mystro"

        dbconfig2 = DBConfiguration()
        dbconfig2.usr = "nobody"
        dbconfig2.pwd = "noddy4U"
        dbconfig2.host = "203.176.98.232"
        dbconfig2.databse = "freeol"

        # Table Fields that will be checked/included in the hash string
        fields_mapping = [
            FieldLink("user_id", "uid"),
            FieldLink("loan_id", "loan_seq"),
            FieldLink("application_id", "main_seq"),
            FieldLink("account_id", "referenceid"),
            FieldLink("broker_id", "brokerid"),
            FieldLink("branch_id", "branch_id"),
            FieldLink("lender_id", "bank"),
            FieldLink("commission_file_id", "file_seq"),
            FieldLink("loan_account_number", "commission_refid"),
            FieldLink("processed", "testrun", func2=yn_to_yesno),
            FieldLink("processed_date", "commission_date"),
            FieldLink("client_name", "client_name"),
            FieldLink("commission_type", "commission_type"),
            FieldLink("original_balance", "original_balance"),
            FieldLink("current_balance", "current_balance"),
            FieldLink("commission_amount", "commission_amt"),
            FieldLink("gst", "gst"),
            FieldLink("broker_matched", "broker_found", func2=yn_to_yesno),
            FieldLink("loan_matched", "found", func2=yn_to_yesno),
            FieldLink("paid", "paid", func2=yn_to_yesno),
            FieldLink("loankit_fee", "fast_fee"),
            FieldLink("loankit_fee_gst", "fast_fee_gst"),
            FieldLink("aggregator", "aggregator"),
            FieldLink("stopped_payment", "stopped_payment", func2=yn_to_yesno),
            FieldLink("activity_note", "reason"),
            FieldLink("application_settled_date", "settle_date"),
            FieldLink("lender_broker_name", "broker_name_at_bank"),
            FieldLink("system_note", "comments"),
            FieldLink("file_upload_date", "file_date"),
            FieldLink("original_aggregator", "original_aggregator"),
            FieldLink("remitted_amount", "remit_amount"),
            FieldLink("excel_worksheet", "sheet", filterr=True, filter1_val=5, filter2_val=5),
            FieldLink("excel_row", "row"),
            FieldLink("run_date", "run_date"),
            FieldLink("auto_allocate", "auto_allocate"),
            FieldLink("vbi_eligible", "vbi_eligible"),
            FieldLink("additional_info", "additional_info")
        ]

        mirror = Mirror(
            dbconfig1,
            dbconfig2,
            "CommissionsLoanKit",
            "commission",
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
