import requests 
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_base = 'https://198.18.128.2:443/restconf/'

headers = {
    'Content-type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json'
}

auth = ('ciscolive25','C!sco2025')

def create_neigbor():
    
    as_number = input('Autonomous system number: ')
    neighbor_router_id = input('Neighbor id: ')
    remote_as = input('Remote autonomus system: ')
    source_interface = input('Update source interface: ')
    
    bgp_url = ''
    payload = {}

def main():
    menu = '''
1. Create new BGP connection 
2. View BGP neighbors
3. Show BGP routes  

'''
    print(menu)
    option_selected = int(input('Enter the number of the desired option: '))

    if option_selected == 1:
        create_neigbor()
    elif option_selected == 2:
        create_neigbor()
    elif option_selected == 3:
        create_neigbor()
    else:
        print("\nNo option found\n")


if __name__ == '__main__':
    main()