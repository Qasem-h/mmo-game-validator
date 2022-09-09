from MMOGameValidator import get_validation_rules
from MMOGameValidator import InvalidCharacter, normalize_character , format_character



# a = get_validation_rules({'game_code': 'WCW', 'game_region': 'US'})


# print(a)
addr = {
    'game_code': 'WCW',
    'game_region': 'US',
    'region_servers': 'Ashkandi',
    'character_name': 'qasemhakà'}
try:
    character = normalize_character(addr)
    
    print(character)
    # print(format_character(character,latin=True ))
    
except InvalidCharacter as e:
    print(e.errors)
