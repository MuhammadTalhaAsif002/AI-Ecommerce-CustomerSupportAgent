import json
from datetime import datetime


def read_json():
    # Open and read the JSON file
    with (
        open('data/refund_test_cases.json', 'r', encoding='utf-8') as f1,
        open('data/refund_policy.json', 'r', encoding='utf-8') as f2,
        open('data/test_queries.json', 'r', encoding='utf-8') as f3,
        open('data/orders.json', 'r', encoding='utf-8') as f4
    ):
        data1 = json.load(f1)
        data2 = json.load(f2)
        data3 = json.load(f3)
        data4 = json.load(f4)

        return data1,data2,data3,data4

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
    print(f"invalid cases are{invalid_cases}")
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
            

def order_lookup(data3,data4):
    boolean=False
    mismatch=[]
    match=[]
    invalid_queries=[]
    
    if(data4):
        for i in range(len(data3)):
            boolean=False
            invalid_queries_flag=False
            for j  in range(len(data4)):
                try:
                    if(data3[i]["order_id"] == data4[j]["order_id"]):
                        boolean=True
                        break
                    else:
                        boolean=False
                except KeyError:
                    print(f"order_id is missing at i,j{(i,j)}")
                    invalid_queries.append(data3[i])
                    invalid_queries_flag=True
                    break
            if(invalid_queries_flag==True):
                continue
            if(boolean==True):
                match.append(data4[j])
                print(f"in match i,j {(i,j)} data3:{data3[i]['order_id']}  data4:{data4[j]['order_id']}")
            elif(data3[i]["order_id"]==""):
                invalid_queries.append(data3[i])
            else:
                mismatch.append(data3[i])
                print(f"in mismatch i,j {(i,j)} data3:{data3[i]['order_id']}  data4:{data4[j]['order_id']}")
        return match,mismatch,invalid_queries
    else:
        return "data4 is empty"


def main():

    data1,data2,data3,data4=read_json()
    with open("data/refund_test_cases.json", "w", encoding="utf-8") as file:
        json.dump(check_Eligibility(data1,data2),file, indent=4)

    result=order_lookup(data3,data4)
    if(result == "data4 is empty"):
        print(result)
    else:
        match, mismatch,invalid_queries= result
        print(f"match ids are : {match}")
        print(f"mismatch ids are : {mismatch}")
        print(f"invalid_queries ids are : {invalid_queries}")
       

    # print(check_Eligibility(data1,data2))
    # pass_percentage,failed_cases=test_refund_logic(data1)
    # print(f"pass percentage is  : {pass_percentage}%")
    # print(f"Failed Cases  : {failed_cases}")

if __name__=="__main__":
    main()