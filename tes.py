from MMOGameValidator import get_validation_rules
from MMOGameValidator import InvalidAddress, normalize_address , format_address



# a = get_validation_rules({'game_code': 'WCW', 'game_region': 'US'})


# print(a)
addr = {
    'game_code': 'WCW',
    'game_region': 'US',
    'region_servers': 'Ashkandi',
    'character_name': 'qasemhakà',
    'street_address': '1600 Amphitheatre Pkwy'}
try:
    address = normalize_address(addr)
    
    print(address)
    # print(format_address(address,latin=True ))
    
except InvalidAddress as e:
    print(e.errors)
