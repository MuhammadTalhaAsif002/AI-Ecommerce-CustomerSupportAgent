import json
from datetime import datetime


# Open and read the JSON file
with (
    open('data/refund_test_cases.json', 'r', encoding='utf-8') as f1,
    open('data/refund_policy.json', 'r', encoding='utf-8') as f2,
    open('data/test_queries.json', 'r', encoding='utf-8') as f3
):
    data1 = json.load(f1)
    data2 = json.load(f2)
    data3 = json.load(f3)

    day_difference=0
    date_format = "%Y-%m-%d"

    for item1 in data1:
        shipped_date = datetime.strptime(item1["shipped_date"],date_format)
        refund_request_date = datetime.strptime(item1["refund_request_date"],date_format)
        day_difference = (refund_request_date - shipped_date).days
        print(f"Day difference is : {day_difference}")
        #check for the eligibility
        if(day_difference<=7):
            if(item1["reason"] in data2[0]["human_review_conditions"]):
                item1["expected_decision"]="human_review"
            elif(item1["reason"] in data2[0]["eligible_reasons"]):
                item1["expected_decision"]="approved"
            elif(item1["reason"] in data2[0]["ineligible_reasons"]):
                item1["expected_decision"]="rejected"
            else:
                item1["expected_decision"]="human_review"
        else:
            item1["expected_decision"]="rejected"



