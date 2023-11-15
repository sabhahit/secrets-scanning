# version 1.0.0
import requests
import sys
import logging
import urllib.parse
import os

def find_sysid_of_ritm(ritm_number):
    headers = {"Content-Type":"text/plain","Accept":"application/json"}
    to_encode = 'number=' + ritm_number
    encoded_querystring = urllib.parse.quote_plus(to_encode)
    sys_user_url = snow_url + '/api/now/table/sc_req_item?sysparm_query=' + encoded_querystring + '&sysparm_fields=sys_id'
    response = requests.get(sys_user_url, auth=(user, pwd), headers=headers )
    if response.status_code != 200: 
        logging.info("Status: {} Headers: {} Error Response:{}".format( response.status_code, response.headers, response.json()))
        exit(1)
    data = response.json()
    ritm_sysid = data['result'][0]['sys_id']
    logging.info("Got sysid from ServiceNow for RITM number:{} as {}".format(ritm_number,ritm_sysid))
    return ritm_sysid

def attachfile(ritm_sysid, filename):
    headers = {"Content-Type":"text/plain","Accept":"application/json"}
    url = snow_url + '/api/now/attachment/file?table_name=sc_req_item&table_sys_id=' + ritm_sysid + '&file_name=' + filename
    data = open(filename, 'rb').read()
    response = requests.post(url, auth=(user, pwd), headers=headers, data=data)
    if response.status_code != 201: 
        logging.info("Status: {} Headers: {} Error Response:{}".format( response.status_code, response.headers, response.json()))
        exit(1)
    resp = response.json()
    

def update_comments(ritm_sysid, comments):
    url = snow_url + '/api/now/table/sc_req_item/' + ritm_sysid
    cheaders = {"Content-Type":"application/json","Accept":"application/json"}
    d='{"comments":"' + comments + '"}'
    logging.info("the content of data d is {}".format(d))
    response = requests.put(url, auth=(user, pwd), headers=cheaders, data=d)
    if response.status_code != 200 : 
        logging.info("Status: {} Headers: {} Error Response:{}".format( response.status_code, response.headers, response.json()))
        exit(1)
    


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')
user = os.environ['SNOW_USER']
pwd = os.environ['SNOW_PASS']
snow_url = os.environ['SNOW_URL']
ritm_number = sys.argv[1]
filename = sys.argv[2]
status_file = sys.argv[3]
ritm_sysid = find_sysid_of_ritm(ritm_number)
attachfile(ritm_sysid, filename)
attachfile(ritm_sysid, status_file)
