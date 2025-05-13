import requests 
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'Content-type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json'
}
auth = ('ciscolive25','C!sco2025')

def main():

    url_base = 'https://DEVICE_IP:443/restconf/data/'

    print('\n\nThis app provides detailed system information for the selected device.')

    router_ip = input('\nEnter the IP of the device: ')
    url_base = url_base.replace('DEVICE_IP', router_ip)

    device_system_data_url = f'{url_base}Cisco-IOS-XE-device-hardware-oper:device-hardware-data/device-hardware/device-system-data'
    
    try: 
        print('\n------ Performing RESTCONF request ------\n')
        response = requests.get(device_system_data_url, headers=headers,auth=auth,verify=False)
        response.raise_for_status()
        device_info = response.json()['Cisco-IOS-XE-device-hardware-oper:device-system-data' ]

        print('\n------ System Information ------\n')

        version = device_info['software-version']
        boot_time =  device_info['boot-time']
        current_time =  device_info['current-time']
        last_r_reason =  device_info['last-reboot-reason']

        print(f'+++ VERSION +++\n\n  {version}')
        print(f'\n+++ BOOT TIME +++\n\n  {boot_time}')
        print(f'\n+++ CURRENT TIME +++\n\n  {current_time}')
        print(f'\n+++ RELOAD REASON +++\n\n  {last_r_reason}')

        print('\n------ Reload History ------\n')

        reload_history =  device_info['reload-history']['rl-history']

        print('{:^15} {:^15} {:^20} {:^20}'.format('Categorty','Severity', 'Description', 'Time'))
        for reload in reload_history:
            category = reload['reload-category']
            severity = reload['reload-severity']
            time = reload['reload-time']
            desc = reload['reload-desc']
            print('{:^15} {:^15} {:^20} {:^20}'.format(category,severity, desc, time ))



    except requests.exceptions.HTTPError as e:
        print (e.response.text)


if __name__ == '__main__':
    main()