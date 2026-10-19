import json
from datetime import datetime


# Open and read the JSON file
with open("data/refund_test_cases.json", "r") as file:
    data = json.load(file)
    # print(data[0]['refund_window'])

    day_difference=0
    date_format = "%Y-%m-%d"
    for item in data:
        shipped_date = datetime.strptime(item["shipped_date"],date_format)
        refund_request_date = datetime.strptime(item["refund_request_date"],date_format)
        day_difference = (refund_request_date - shipped_date).days
        print(f"Day difference is : {day_difference}")

    
    

# # 'data' is now a standard Python list of dictionaries
# for item in data:
#     print(f"Category: {item['query_category']}")
#     print(f"Message: {item['customer_message']}\n")
