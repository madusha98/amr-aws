import requests
import json
import base64


def get_bill_value(event, context):

    # 1. parse out request json body
    body_dec = base64.b64decode(event['body'])
    request = json.loads(body_dec)
    noOfUnits = request['NoOfUnits']
    fromDate = request['FromDate']
    toDate = request['ToDate']

    # 2. construct the header and body of the CEB endpoint
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {'tariff_cat': '11',
            'iUnit': noOfUnits,
            'datepicker3': fromDate,
            'datepicker4': toDate,
            'lastsegment': 'en'}
    
    # 3. construct the http response from CEB endpoint
    response = requests.post(
        "https://ceb.lk/bill_calculation_commercial/calculate_bill", headers=headers, data=data, verify=False)

    # response_load = json.loads(response.text)
    # print('Bill Value:', response_load['Total'])

    # 4. return the repsonse object
    response = json.loads(response.text)
    return {
        "body": json.dumps(response)
    }

