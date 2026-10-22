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
        #check for the eligibility
        if(0<day_difference<=7):
            if(item1["reason"] in data2[0]["human_review_conditions"] or  item1["evidence"]=="invalid reason"):
                item1["actual_decision"]="human_review" 
            elif(item1["reason"] in data2[0]["eligible_reasons"]):
                item1["actual_decision"]="approved"
            elif(item1["reason"] in data2[0]["ineligible_reasons"]):
                item1["actual_decision"]="rejected"
            elif(item1["reason"]=="" or item1["reason"]=="something unusual"):
                item1["reason"]="unknown"
                item1["actual_decision"]="human_review"
            else:
                item1["actual_decision"]="human_review"
        else:
            item1["actual_decision"]="rejected"
    with open("data/refund_test_cases.json", "w", encoding="utf-8") as file:
        json.dump(data1,file, indent=4)



