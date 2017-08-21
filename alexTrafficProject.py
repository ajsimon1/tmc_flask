"""
scrape traffic data off bing maps API, reformat to aleza flash brief json
API format
"""
import datetime
import json
import re
import requests
import time
import uuid


# constants for bound box, lat & long for box that traffic Incidents pull from
SOUTH = 40.166281254206545
WEST = -74.78668212890625
NORTH = 40.74101426921151
EAST = -74.06707763671875

# bing traffic api's details
# get traffic data by https://msdn.microsoft.com/en-us/library/hh441726.aspx


url = "http://dev.virtualearth.net/REST/v1/Traffic/Incidents/40.166281254206545,-74.78668212890625,40.74101426921151,-74.06707763671875/false?s=2,3,4&t=1,2,8,9&key=ApZQPDiXe83SL22Po1FDQcQ3KwjmbjIL1_wZxRu0JbHoaRWNYFO5NXg11M7g_M8G"
# scrape json data off web
response = requests.get(url)
# pull text out response object
json_str = response.text
# parse text into standard json format
parsed_json = dict(json.loads(json_str))

def build_total_count(parsed_json):
    alexa_incident_list = []
    total_uuid = uuid.uuid4()
    today = datetime.datetime.today().strftime("%Y-%m-%dT%H:%M:%S.0Z")
    incident_count = parsed_json['resourceSets'][0]['estimatedTotal']
    alexa_incident_count = {"uid": "{}".format(str(total_uuid)),
                            "updateDate": "{}".format(today),
                            "titleText": "Traffic Items for Today",
                            "mainText": "There are {} incidents to report".format(incident_count)}
    alexa_incident_list.append(alexa_incident_count)
    return alexa_incident_list

def build_incident_report(parsed_json):
    api_data = {"severity": {"2":"Minor", "3":"Moderate", "4":"Serious"},
                "type": {"1":"Accident", "2":"Congestion", "8":"Road hazard", "9":"Construction"}}
    final_incident_list = []
    for count, incident_dict in enumerate(parsed_json['resourceSets'][0]['resources']):
        total_uuid = uuid.uuid4()
        epoch_date = int(re.search(r'\d+', incident_dict['lastModified']).group())
        other_date = time.gmtime(epoch_date / 1000)
        convert_epoch_date = time.strftime("%Y-%m-%dT%H:%M:%S.0Z", other_date)
        incident_id = count + 1
        severity = api_data['severity'][str(incident_dict['severity'])]
        incident_type = api_data['type'][str(incident_dict['type'])]
        description= incident_dict['description']
        road_closed = incident_dict['roadClosed']
        verified = incident_dict['verified']
        main_text_str = "There is {} {} {}, its {} that the road is closed and its {} that the accident has been visually verified".format(severity, incident_type, description, road_closed, verified)
        final_incident_dict = {"uid": "{}".format(str(total_uuid)),
                               "updateDate": "{}".format(convert_epoch_date),
                               "titleText": "Info on incident #{}".format(incident_id),
                               "mainText": "{}".format(main_text_str)}
        final_incident_list.append(final_incident_dict)
    return final_incident_list

def build_final_list(a_list, b_list):
    for a_dict in b_list:
        a_list.append(a_dict)
    return a_list


exportable_json = json.dumps(build_final_list(build_total_count(parsed_json), build_incident_report(parsed_json)), sort_keys=True)
