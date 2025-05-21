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
    
    bgp_url = f'{url_base}Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-bgp:bgp'
    payload = {
        "bgp": [
            {
                "id": as_number,
                "address-family": {
                    "no-vrf": {
                        "ipv4": {
                            "ipv4-unicast": {
                                "neighbor": {
                                    "id": neighbor_router_id
                                }
                            }
                        }
                    }
                },
                "neighbor": {
                    "id": neighbor_router_id,
                    "remote-as": remote_as,
                    "update-source": {
                        "interface": {
                            source_interface_type: source_interface_number
                        }
                    }
                }
            }
        ]
    }
    payload = json.dumps(payload)

    try: 
        print("\n------ Performing RESTCONF request ------\n")
        response = requests.patch( bgp_url, headers=headers,auth=auth, data=payload, verify=False)
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

    route_url = f'{url_base}Cisco-IOS-XE-bgp-oper:bgp-state-data/bgp-route-vrfs/bgp-route-vrf=default' 

    try: 
        response = requests.get(route_url, headers=headers, auth=auth, verify=False)
        response.raise_for_status()

        routes_lst = []
        routes = response.json()['Cisco-IOS-XE-bgp-oper:bgp-route-vrf'][0]['bgp-route-afs']['bgp-route-af'][2]['bgp-route-filters']['bgp-route-filter'][0]['bgp-route-entries']['bgp-route-entry']

        for route in routes:
            route_dic = {}
            route_dic['prefix'] = route['prefix']
            route_dic['available-paths'] = route['available-paths']
            paths = []
            for entry in route['bgp-path-entries']['bgp-path-entry']:
                path = {}
                path['nexthop'] = entry['nexthop']
                path['metric'] = entry['metric']
                path['local-pref'] = entry['local-pref']
                path['weight'] = entry['weight']
                paths.append(path)
            route_dic['paths'] = paths
            routes_lst.append(route_dic)
        
        for route in routes_lst:
            prefix = route['prefix']
            print(f'Prefix: {prefix}')
            av_pths = route['available-paths']
            print(f'Available paths: {av_pths}')
            for path in route['paths']:
                path_no = route['paths'].index(path)+1
                nxt_hp = path['nexthop']
                metric = path['metric']
                loc_pref = path['local-pref']
                weight = path['weight']
                print(f'Path {path_no}')
                print(f'    - Next hop: {nxt_hp}')
                print(f'    - Metric: {metric}')
                print(f'    - Local preference: {loc_pref}')
                print(f'    - Weight: {weight}')
            print('\n')
            



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
        print('----------------------------------------------------')
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
        
        print('\n')
        print('----------------------------------------------------')


if __name__ == '__main__':
    main()