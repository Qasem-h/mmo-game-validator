from MMOGameValidator import get_validation_rules
from MMOGameValidator import InvalidCharacter, normalize_character , format_character



# a = get_validation_rules({'game_code': 'NW'})


# print(a)
# for name in a.game_faction_choices:
#     print(name[0])
    
addr = {
    'game_code': 'NW',
    'game_region': 'USW',
    'region_servers': 'El Dorado',
    'character_name': 'my nameiseqwrrt '}
try:
    character = normalize_character(addr)
    
    # print(character)
    print(format_character(character,latin=True ))
    
except InvalidCharacter as e:
    print(e.errors)
