from MMOGameValidator import get_validation_rules
from MMOGameValidator import InvalidCharacter, normalize_character , format_character



# a = get_validation_rules({'game_code': 'WCW', 'game_region': "NA"})


# print(a)
# for name, v in a.region_servers_choices:
#     print(name)
#     print(v)

# for name in a.game_faction_choices:
#     print(name[0])
 
# import re
# zip = "[A-Za-z]{3,15}"
# character_name_matchers = re.compile("^" + zip + "$")

# character_name = "hello "
# if character_name_matchers.match(character_name):
#         print("mach")
# else:
#     print("motmath")
    
addr = {
    'game_code': 'WCW',
    'game_region': 'EU',
    'region_servers': 'Giantstalker',
    'game_faction': 'horde',
    'character_name': 'hieewe'
    }
try:
    character = normalize_character(addr)
    
    print(character)
    # print(format_character(character,latin=True ))
    
except InvalidCharacter as e:
    print(e.errors)

# class LostArk_EUW:

#     RM  = "rethramis"
#     SO  = "stonehearth"
#     PN  = "petrania"
#     TO  = "tortoyk"
#     SD  = "shadespire"
#     PU  = "punika"
#     MP  = "moonkeep"
#     TG  = "tragon"

#     CHOICES = [

#         (RM,  "Rethramis"),
#         (SO,  "Stonehearth"),
#         (PN,  "Petrania"),
#         (TO,  "Tortoyk"),
#         (SD,  "Shadespire"),
#         (PU,  "Punika"),
#         (MP,  "Moonkeep"),
#         (TG,  "Tragon"),
#     ] 

# class LostArk_SA:
#     KZ  = "kazeros"
#     AC  = "arcturus"
#     VE  = "vern"
#     AG  = "agaton"
#     YN  = "yorn"
#     KU  = "kurzan"
#     GG  = "gienah"
#     FN  = "feiton"
#     PD  = "prideholme"

#     CHOICES = [

#         (KZ,  "Kazeros"),
#         (AC,  "Arcturus"),
#         (VE,  "Vern"),
#         (AG,  "Agaton"),
#         (YN,  "Yorn"),
#         (KU,  "Kurzan"),
#         (GG,  "Gienah"),
#         (FN,  "Feiton"),
#         (PD,  "Prideholme"),
#     ] 

# # 'GIANTSTALKER', 'giantstalker'
# #  ("dropdown", "Dropdown"),

# def prepare_all_games_servers_dict():
#     game_servers_dict = {
#         server: item
#         for servers in [LostArk_EUW, LostArk_SA]
#         for server, item in servers.CHOICES
#     }
#     game_servers_dict["CHOICES"] = [(v, k) for v, k in game_servers_dict.items()]
#     return game_servers_dict


# GameServers = type("GameServers", (object,), prepare_all_games_servers_dict())

# print(GameServers.CHOICES)