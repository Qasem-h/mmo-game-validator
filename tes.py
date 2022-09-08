from i18naddress import get_validation_rules

a = get_validation_rules({'game_code': 'WCW', 'game_region': 'US'})


print(a)


# __slots__ = [
#         "country_code",
#         "country_name",
#         "allowed_fields",
#         "required_fields",
#         "upper_fields",
#         "country_area_type",
#         "country_area_choices",
#         "city_type",
#         "city_choices",
#         "city_area_type",
#         "city_area_choices",
#         "postal_code_type",
#         "postal_code_matchers",
#         "postal_code_examples",
#         "postal_code_prefix",
#     ]


# ValidationRules(game_code='WCW', game_name='World of Warcraft WOTLK', game_short_name='WOW Classic WOTLK', game_full_name='World of Warcraft: Wrath of the Lich King', 
#                 address_format='%O%n%N%n%A%n%D%n%C-%S%n%Z', address_latin_format='%O%n%N%n%A%n%D%n%C-%S%n%Z', allowed_fields={'city', 'game_region', 'city_area', 'street_address', 'postal_code', 'name', 'company_name'}, 
#                 required_fields={'game_region', 'street_address', 'postal_code', 'city'}, upper_fields={'city', 'game_region'}, game_region_type='region', game_region_choices=[('US', 'Americas'), ('EU', 'Europe'), ('OC', 'Oceania')], 
#                 server_type='city', server_choices=[('Maladath', 'Maladath'), ('Skyfury', 'Skyfury'), ('Ashkandi', 'Ashkandi'), ('Atiesh', 'Atiesh'), ('Azuresong', 'Azuresong'), ('Benediction', 'Benediction'), ('Bloodsail Buccaneers', 'Bloodsail Buccaneers'), ('Earthfury', 'Earthfury'), ('Faerlina', 'Faerlina'), ('Grobbulus', 'Grobbulus'), ('Mankrik', 'Mankrik'), ('Myzrael', 'Myzrael'), ('Old Blanchy', 'Old Blanchy'), ('Pagle', 'Pagle'), ('Sulfuras', 'Sulfuras'), ('Westfall', 'Westfall'), ('Whitemane', 'Whitemane'), ('Windseeker', 'Windseeker')], 
#                 city_area_type='neighborhood', city_area_choices=[], postal_code_type='postal', 
#                 postal_code_matchers=[re.compile('^\\d{5}-?\\d{3}$'), re.compile('^699')], postal_code_prefix='')