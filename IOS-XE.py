import requests
import base64

url_base = 'https://10.88.247.78/restconf/'
credentials = 'restconf:cisco123' 

headers = {
    'Content-type' : 'application/yang-data+json',
    'Accept' : 'application/yang-data+json',
}

auth = ('restconf','cisco123')

url=f'{url_base}data/Cisco-IOS-XE-native:native/interface/Loopback'

response = requests.get(url, headers=headers, auth=auth, verify=False)

print(str(response.status_code))

print(response.json())