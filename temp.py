import json
from datetime import datetime


def read_json():
    # Open and read the JSON file
    with (
        open('data/refund_test_cases.json', 'r', encoding='utf-8') as f1,
        open('data/refund_policy.json', 'r', encoding='utf-8') as f2,
        open('data/test_queries.json', 'r', encoding='utf-8') as f3
    ):
        data1 = json.load(f1)
        data2 = json.load(f2)
        data3 = json.load(f3)

        return data1,data2,data3

def check_Eligibility(data1,data2):

    day_difference=0
    date_format = "%Y-%m-%d"
    invalid_cases=[]
    for item1 in data1:
        try:
            shipped_date = datetime.strptime(item1["shipped_date"],date_format)
            refund_request_date = datetime.strptime(item1["refund_request_date"],date_format)
            day_difference = (refund_request_date - shipped_date).days
        except ValueError:
            invalid_cases.append(item1)
            continue
        #check for the eligibility
        if(0<=day_difference<=7):
            if(item1["reason"] in data2[0]["human_review_conditions"] or item1["evidence"]=="invalid reason"):
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
        elif(day_difference<0):
            item1["actual_decision"]="req before shipping"   
        else:
            item1["actual_decision"]="refund window expired"
    return data1

def test_refund_logic(data):
    count=0
    total_count=len(data)
    failed_cases=[]
    if(data):
        for i in data:
            if(i["expected_decision"]==i["actual_decision"]):
                count+=1
            else:
                failed_cases.append(i)
    else:
        print(f"no entry in the data {data}")
        return 0,0

    pass_percentage=count/total_count *100
    return pass_percentage,failed_cases
            

    

def main():

    data1,data2,data3=read_json()
    # with open("data/refund_test_cases.json", "w", encoding="utf-8") as file:
    #     json.dump(check_Eligibility(data1,data2),file, indent=4)

    
    # print(check_Eligibility(data,data2))
    pass_percentage,failed_cases=test_refund_logic(data1)
    print(f"pass percentage is  : {pass_percentage}%")
    print(f"Failed Cases  : {failed_cases}")

if __name__=="__main__":
    main()