from model.mirror import *
from db.dba import *


def yn_to_yesno(arg):
    if arg == "Y" or arg == "y":
        return "yes"
    elif arg == "N" or arg == "N":
        return "no"
    else:
        return arg


def readdigit(inputmessage=""):
    val = ""
    while not val.isdigit():
        val = input(inputmessage)
        try:
            val = int(val)
            if val <= 0:
                val = ""
                print("Value must be greater than 0")
            else:
                break
        except ValueError:
            print("Value must be an integer")
    return val


def decimal_to_float(arg):
    return float(arg)

def y_to_no_and_n_to_yes(arg):
    if arg.lower() == "y":
        return "no"
    elif arg.lower() == "n":
        return "yes"
    else:
        return arg


class MirroringValidator():

    def __init__(self):
        pass

    def run():

        dbconfig1 = DBConfiguration()
        dbconfig1.usr = "root"
        dbconfig1.pwd = "LK3isMyL1feNowMySQL"
        dbconfig1.host = "203.98.82.14"
        dbconfig1.databse = "mystro"

        dbconfig2 = DBConfiguration()
        dbconfig2.usr = "nobody"
        dbconfig2.pwd = "noddy4U"
        dbconfig2.host = "203.176.98.232"
        dbconfig2.databse = "freeol"

        dba1 = DBA(dbconfig1)
        dba2 = DBA(dbconfig2)

        # Read filter values
        id1 = readdigit("Comission file id 1: ")
        id2 = readdigit("Comission file id 2: ")

        # Table Fields that will be checked/included in the hash string
        fields_mapping = [
            FieldLink("user_id", "uid"),
            FieldLink("loan_id", "loan_seq"),
            FieldLink("application_id", "main_seq"),
            FieldLink("account_id", "referenceid"),
            FieldLink("broker_user_id", "brokerid"),
            FieldLink("branch_id", "branch_id"),
            FieldLink("lender_id", "bank"),
            FieldLink("commission_file_id", "file_seq", uid=True, filterr=True, filter1_val=id1, filter2_val=id2),
            FieldLink("loan_account_number", "commission_refid"),
            FieldLink("processed", "testrun", func2=y_to_no_and_n_to_yes),
            FieldLink("processed_date", "commission_date"),
            FieldLink("client_name", "client_name"),
            FieldLink("commission_type", "commission_type"),
            FieldLink("original_balance", "original_balance", func1=decimal_to_float),
            FieldLink("current_balance", "current_balance", func1=decimal_to_float),
            FieldLink("commission_amount", "commission_amt", func1=decimal_to_float),
            FieldLink("gst", "gst", func1=decimal_to_float),
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
            FieldLink("remitted_amount", "remit_amount", func1=decimal_to_float),
            FieldLink("excel_worksheet", "sheet", uid=True),
            FieldLink("excel_row", "row", uid=True),
            FieldLink("run_date", "run_date"),
            FieldLink("auto_allocate", "auto_allocate", func2=yn_to_yesno),
            FieldLink("vbi_eligible", "vbi_eligible", func2=yn_to_yesno),
        ]

        mirror = Mirror(
            dba1,
            dba2,
            "CommissionsFinsure",
            "commission_finsure",
            fields_mapping
        )

        # Retrieve all data from database as dictionary
        mirror.run_diff()
        # Export file to csv
        mirror.to_csv()


MirroringValidator.run()
