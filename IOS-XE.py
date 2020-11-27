import requests
import base64
from pprint import pprint
from datetime import date, datetime
from dateutil import parser
from pytz import timezone
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = 'https://10.88.247.79:443/restconf/'

headers = {
    'Content-type' : 'application/yang-data+json',
    'Accept' : 'application/yang-data+json',
}

auth = ('marintor','7Ring$')


# hostname = open("Filters/17_3_X/hostname.xml").read()
# config = open("Filters/17_3_X/BGP-690329194.xml").read() # Apply BGP conf 
# bgp = open("Filters/17_3_X/BGP-690329194-2.xml").read() # Delete BGP conf -> Wrongo 
# bgp2 = open("Filters/17_3_X/BGP-690329194-3.xml").read() # DElete BGP cong -> Succesfull 

###Get config
# response = requests.get(runnung_config, headers=headers, auth=auth, verify=False)

# if (response.status_code):
#     print(response.json())

'''
def set_status(admin, oper):

    intf_stats = {}

    if admin == 'if-state-up' and oper == 'if-oper-state-ready':
        intf_stats['status'] = 'UP'
        intf_stats['protocol'] = 'UP'
    elif admin == 'if-state-down' and oper == 'if-oper-state-no-pass':
        intf_stats['status'] = 'ADMINISTRATIVELY DOWN'
        intf_stats['protocol'] = 'DOWN'
    else:
        intf_stats['status'] = 'DOWN'
        intf_stats['protocol'] = 'DOWN'
        
    return intf_stats

### Interfaces
interfaces = {}

runnung_config = f'{url_base}/data/Cisco-IOS-XE-native:native/'
interfaces_conf = f'{url_base}data/Cisco-IOS-XE-native:native/interface'
interfaces_oper_status = f'{url_base}/interfaces/interface/oper-status'

response = requests.get(interfaces_conf, headers=headers, auth=auth, verify=False)
if (response.status_code):
    interfaces_conf = response.json()['Cisco-IOS-XE-native:interface']

for int_type in interfaces_conf:
    for intf in interfaces_conf[int_type]:
        name = int_type + intf['name']
        
        if 'ip' in intf:
            ip = intf['ip']['address']['primary']['address']
        else:
            ip = 'unassigned'
        
        interfaces_admin_status = f'{url_base}/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface={name}/admin-status'
        response = requests.get(interfaces_admin_status, headers=headers, auth=auth, verify=False)
        if(response.status_code):
            admin_status = response.json()['Cisco-IOS-XE-interfaces-oper:admin-status']
        
        interfaces_oper_status = f'{url_base}/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface={name}/oper-status'
        response = requests.get(interfaces_oper_status, headers=headers, auth=auth, verify=False)
        if(response.status_code):
            oper_status = response.json()['Cisco-IOS-XE-interfaces-oper:oper-status']
        
        result = set_status(admin_status,oper_status)
        result['ip'] = ip

        interfaces[name] = result

print('{:<23} {:<14} {:<23} {:<5}'.format('Interface','IP-Address','Status', 'Protocol'))
    
for i in interfaces:
    print('{:<23} {:<14} {:<23} {:<5}'.format(i,interfaces[i]['ip'], interfaces[i]['status'],interfaces[i]['protocol']))

### Device Status

device_status = f'{url_base}/data/Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-hardware/device-system-data'

response = requests.get(device_status, headers=headers, auth=auth, verify=False)
if (response.status_code):
    device_status = response.json()['Cisco-IOS-XE-device-hardware-oper:device-system-data']

    #software version
    soft_ver = device_status['software-version']
    print(f'--- VERSION ---\n\n{soft_ver}')

    #boot time
    b_time = parser.parse(device_status['boot-time']).replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Mexico_City'))
    boot_time = b_time.strftime('%A %d %b %Y %X')
    
    print(f'\n--- BOOT TIME ---\n\n{boot_time}')

    #current time
    c_time = parser.parse(device_status['current-time']).replace(tzinfo=timezone('UTC')).astimezone(timezone('America/Mexico_City'))
    current_time = c_time.strftime('%A %d %b %Y %X')  
    print(f'\n--- CURRENT TIME ---\n\n{current_time}')

    #uptime time
    uptime = c_time - b_time
    print(f'\n--- UPTIME ---\n\n{uptime}')

    #last reload reason
    last_r_reason = device_status['last-reboot-reason']
    print(f'\n--- RELOAD REASON ---\n\n{last_r_reason}')
'''
### Change hostname

hostname = f'{url_base}/data/Cisco-IOS-XE-native:native/hostname'
payload = '{\'Cisco-IOS-XE-native:hostname\': \'Marinthor\'}'

response = requests.patch(hostname, data=payload, headers=headers, auth=auth, verify=False)
if (response.status_code):
    print(response.status_code)
    print(response.json())