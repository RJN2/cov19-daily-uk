import requests
import pandas as pd
import json

briefing_list = requests.get('https://www.gov.uk/api/content/government/collections/slides-and-datasets-to-accompany-coronavirus-press-conferences').json()
briefings = briefing_list['links']['documents']
latest = max(briefings, key=lambda x:x['public_updated_at'])

briefing_detail = requests.get(latest['api_url']).json()
attachments = briefing_detail['details']['attachments']
dataset = next(attachment for attachment in attachments if attachment['content_type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
latest_data = requests.get(dataset['url']).content

xls = pd.ExcelFile(latest_data)

daily = {}

for sht in xls.sheet_names:
    daily[sht] = pd.read_excel(xls, sht).to_dict('records')

with open('daily.json', 'w') as json_file:
  json.dump(daily, json_file, indent=4, sort_keys=True, default=str)