import requests 
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = 'https://198.18.128.2:443/restconf/data/'

headers = {
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json'
}

auth = ('ciscolive25','C!sco2025')

def create_neighbor():
    
    as_number = input('Autonomous system number: ')
    neighbor_router_id = input('Neighbor id: ')
    remote_as = input('Remote autonomus system: ')
    source_interface_type = input('Update source interface type: ')
    source_interface_number = input('Update source interface number: ')
    
    bgp_url = f'{url_base}'
    payload = {}
    payload = json.dumps(payload)

    try: 
        print("\n------ Performing RESTCONF request ------\n")
        response = requests.patch( bgp_url, headers=headers,auth=auth, data=payload,  verify=False)
        response.raise_for_status()
        print("\n------ Neighbor Created ------\n")

    except requests.exceptions.HTTPError as e:
        print (e.response.text)

def delete_neighbor():

    as_number = input('Autonomous system number: ')
    neighbor_id = input('Neighbor id: ')

    neighbor_url = f'{url_base}Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-bgp:bgp={as_number}/neighbor={neighbor_id}' 
    

    try: 
        response = requests.delete(neighbor_url, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        print("\n------ Neighbor deleted ------\n")

    except requests.exceptions.HTTPError as e:
        print (e.response.text)

def view_neighbors():
    neighbor_url = f'{url_base}Cisco-IOS-XE-bgp-oper:bgp-state-data/neighbors' 

    try: 
        response = requests.get(neighbor_url, headers=headers, auth=auth, verify=False)
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print (e.response.text)
    
    for neighbor in response.json()['Cisco-IOS-XE-bgp-oper:neighbors']['neighbor']:
        neighbor_id = neighbor['neighbor-id']
        neighbor_as = neighbor['as']
        print(f"\n Neighbor: {neighbor_id}  AS: {neighbor_as}\n")
        bgp_counters_sent =  neighbor['bgp-neighbor-counters']['sent']
        bgp_counters_received =  neighbor['bgp-neighbor-counters']['received']


        print('{:^15} {:^15} {:^15} {:^15} {:^15}'.format('opens', 'updates', 'notifications', 'keepalives', 'route-refreshes'))
        print('Sent: {:^6} {:^15} {:^15} {:^15} {:^15}'.format(bgp_counters_sent['opens'], bgp_counters_sent['updates'], bgp_counters_sent['notifications'], bgp_counters_sent['keepalives'], bgp_counters_sent['route-refreshes']))
        print('Received: {:^2} {:^15} {:^15} {:^15} {:^15}'.format(bgp_counters_received['opens'], bgp_counters_received['updates'], bgp_counters_received['notifications'], bgp_counters_sent['keepalives'], bgp_counters_received['route-refreshes']))

def view_bgp_routes():

    as_number = input('Autonomous system number: ')
    neighbor_id = input('Neighbor id: ')

    neighbor_url = f'{url_base}Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-bgp:bgp={as_number}/neighbor={neighbor_id}' 
    

    try: 
        response = requests.delete(neighbor_url, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        print("\n------ Neighbor deleted ------\n")

    except requests.exceptions.HTTPError as e:
        print (e.response.text)

def main():
    option_selected = 0
    menu = '''
1. Create new BGP connection 
2. Delete Nighbor
3. View BGP neighbors
4. Show BGP routes  

Type 9 to exit 
'''
    while option_selected in [0,1,2,3,4]:
        print(menu)
        option_selected = int(input('Enter the number of the desired option: '))
        print('\n')

        if option_selected == 1:
            create_neighbor()
        elif option_selected == 2:
            delete_neighbor()
        elif option_selected == 3:
            view_neighbors()
        elif option_selected == 4:
            view_bgp_routes()
        elif option_selected == 9:
            print("\n------ End Session ------\n")
        else:
            print("\n------ No option found ------\n")


if __name__ == '__main__':
    main()