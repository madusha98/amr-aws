import requests
import json

def get_bill_value(event, context):

    headers = {
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {'tariff_cat': '11',
            'iUnit': '150',
            'datepicker3': '2021-03-01',
            'datepicker4': '2021-03-31',
            'lastsegment': 'en'}

    response = requests.post(
        "https://ceb.lk/bill_calculation_commercial/calculate_bill", headers=headers, data=data, verify=False)

    print(response.text)
    response_load = json.loads(response.text)
    print('Bill Value:', response_load['Total'])

    return response
