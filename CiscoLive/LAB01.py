import requests 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = 'https://198.18.128.2/restconf/'

headers = {
    'Content-type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json'
}

auth = ('ciscolive25','C!sco2025')

hostname = f'{url_base}data/Cisco-IOS-XE-native:native/hostname'

response = requests.get(hostname, headers=headers,auth=auth,verify=False)

if (response.status_code):
    data = response.json()
    hostname = data.get('Cisco-IOS-XE-native:hostname')
    print(f'The hostname of the router is: {hostname}')
