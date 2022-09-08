from __future__ import unicode_literals

import io
import json
import os
import re
from collections import OrderedDict

VALID_GAME_CODE = re.compile(r"^\w{2,3}$")
VALIDATION_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
VALIDATION_DATA_PATH = os.path.join(VALIDATION_DATA_DIR, "%s.json")

FIELD_MAPPING = {
    "A": "street_address",
    "C": "region_servers",
    "N": "name",
    "S": "game_region",
    "X": "sorting_code",
    "Z": "character_name",
}

KNOWN_FIELDS = set(FIELD_MAPPING.values()) | {"game_code"}


def load_validation_data(game_code="all"):
    if not VALID_GAME_CODE.match(game_code):
        raise ValueError("%r is not a valid game code" % (game_code,))
    game_code = game_code.lower()
    try:
        # VALIDATION_DATA_PATH may have '%' symbols
        # for backwards compatability if VALIDATION_DATA_PATH is imported
        # by consumers of this package.
        path = VALIDATION_DATA_PATH % (game_code,)
    except TypeError:
        path = os.path.join(VALIDATION_DATA_DIR, "%s.json" % game_code)

    if not os.path.exists(path):
        raise ValueError("%r is not a valid game code" % (game_code,))
    with io.open(path, encoding="utf-8") as data:
        return json.load(data)


class ValidationRules(object):
    __slots__ = [
        "game_code",
        "game_name",
        "game_short_name",
        "game_full_name",
        "address_format",
        "allowed_fields",
        "required_fields",
        "upper_fields",
        "game_region_type",
        "game_region_choices",
        "region_servers_type",
        "region_servers_choices",
        "character_name_type",
        "character_name_matchers",
        "character_name_prefix",
    ]

    def __init__(
        self,
        game_code,
        game_name,
        game_short_name,
        game_full_name,
        address_format,
        allowed_fields,
        required_fields,
        upper_fields,
        game_region_type,
        game_region_choices,
        region_servers_type,
        region_servers_choices,
        character_name_type,
        character_name_matchers,
        character_name_prefix,
    ):
        self.game_code = game_code
        self.game_name = game_name
        self.game_short_name = game_short_name
        self.game_full_name = game_full_name
        self.address_format = address_format
        self.allowed_fields = allowed_fields
        self.required_fields = required_fields
        self.upper_fields = upper_fields
        self.game_region_type = game_region_type
        self.game_region_choices = game_region_choices
        self.region_servers_type = region_servers_type
        self.region_servers_choices = region_servers_choices
        self.character_name_type = character_name_type
        self.character_name_matchers = character_name_matchers
        self.character_name_prefix = character_name_prefix

    def __repr__(self):
        return (
            "ValidationRules("
            "game_code=%r, "
            "game_name=%r, "
            "game_short_name=%r, "
            "game_full_name=%r, "
            "address_format=%r, "
            "allowed_fields=%r, "
            "required_fields=%r, "
            "upper_fields=%r, "
            "game_region_type=%r, "
            "game_region_choices=%r, "
            "region_servers_type=%r, "
            "region_servers_choices=%r, "
            "character_name_type=%r, "
            "character_name_matchers=%r, "
            "character_name_prefix=%r)"
            % (
                self.game_code,
                self.game_name,
                self.game_short_name,
                self.game_full_name,
                self.address_format,
                self.allowed_fields,
                self.required_fields,
                self.upper_fields,
                self.game_region_type,
                self.game_region_choices,
                self.region_servers_type,
                self.region_servers_choices,
                self.character_name_type,
                self.character_name_matchers,
                self.character_name_prefix,
            )
        )


def _make_choices(rules, translated=False):
    sub_keys = rules.get("sub_keys")
    if not sub_keys:
        return []
    choices = []
    sub_keys = sub_keys.split("~")
    sub_names = rules.get("sub_names")
    if sub_names:
        choices += [
            (key, value) for key, value in zip(sub_keys, sub_names.split("~")) if value
        ]
    else:
        if not translated:
            choices += [(key, key) for key in sub_keys]
    if not translated:
        sub_lnames = rules.get("sub_lnames")
        if sub_lnames:
            choices += [
                (key, value)
                for key, value in zip(sub_keys, sub_lnames.split("~"))
                if value
            ]
        sub_lfnames = rules.get("sub_lfnames")
        if sub_lfnames:
            choices += [
                (key, value)
                for key, value in zip(sub_keys, sub_lfnames.split("~"))
                if value
            ]
    return choices


def _compact_choices(choices):
    value_map = OrderedDict()
    for key, value in choices:
        if not key in value_map:
            value_map[key] = set()
        value_map[key].add(value)
    return [
        (key, value) for key, values in value_map.items() for value in sorted(values)
    ]


def _match_choices(value, choices):
    if value:
        value = value.strip().lower()
    for name, label in choices:
        if name.lower() == value:
            return name
        if label.lower() == value:
            return name


def _load_game_data(game_code):
    database = load_validation_data("zz")
    game_data = database["ZZ"]
    if game_code:
        game_code = game_code.upper()
        if game_code.lower() == "zz":
            raise ValueError("%r is not a valid game code" % (game_code,))
        database = load_validation_data(game_code.lower())
        game_data.update(database[game_code])
    return game_data, database


def get_validation_rules(address):
    game_code = address.get("game_code", "").upper()
    game_data, database = _load_game_data(game_code)
    game_name = game_data.get("name", "")
    game_short_name = game_data.get("short_name", "")
    game_full_name = game_data.get("full_name", "")
    address_format = game_data["fmt"]
    format_fields = re.finditer(r"%([ACNSXZ])", address_format)
    allowed_fields = {FIELD_MAPPING[m.group(1)] for m in format_fields}
    required_fields = {FIELD_MAPPING[f] for f in game_data["require"]}
    upper_fields = {FIELD_MAPPING[f] for f in game_data["upper"]}
    languages = [None]
    if "languages" in game_data:
        languages = game_data["languages"].split("~")

    character_name_matchers = []
    if "character_name" in allowed_fields:
        if "zip" in game_data:
            character_name_matchers.append(re.compile("^" + game_data["zip"] + "$"))

    game_region_choices = []
    region_servers_choices = []
    server_area_choices = []
    game_region_type = game_data["region_name_type"]
    region_servers_type = game_data["locality_name_type"]
    character_name_type = game_data["zip_name_type"]
    character_name_prefix = game_data.get("postprefix", "")
    # second level of data is for administrative areas
    game_region = None
    region_servers = None
    region_servers_area = None
    if game_code in database:
        if "sub_keys" in game_data:
            for language in languages:
                is_default_language = (
                    language is None or language == game_data["lang"]
                )
                matched_game_region = None
                matched_server = None
                if is_default_language:
                    localized_game_data = database[game_code]
                else:
                    localized_game_data = database[
                        "%s--%s" % (game_code, language)
                    ]
                localized_game_region_choices = _make_choices(localized_game_data)
                game_region_choices += localized_game_region_choices
                existing_choice = game_region is not None
                matched_game_region = game_region = _match_choices(
                    address.get("game_region"), localized_game_region_choices
                )
                if matched_game_region:
                    # third level of data is for cities
                    if is_default_language:
                        game_region_data = database[
                            "%s/%s" % (game_code, game_region)
                        ]
                    else:
                        game_region_data = database[
                            "%s/%s--%s" % (game_code, game_region, language)
                        ]
                    if not existing_choice:
                        if "zip" in game_region_data:
                            character_name_matchers.append(
                                re.compile("^" + game_region_data["zip"])
                            )

                    if "sub_keys" in game_region_data:
                        localized_region_servers_choices = _make_choices(game_region_data)
                        region_servers_choices += localized_region_servers_choices
                        existing_choice = region_servers is not None
                        matched_server = region_servers = _match_choices(
                            address.get("region_servers"), localized_region_servers_choices
                        )
                    if matched_server:
                        # fourth level of data is for dependent sublocalities
                        if is_default_language:
                            server_data = database[
                                "%s/%s/%s" % (game_code, game_region, region_servers)
                            ]
                        else:
                            server_data = database[
                                "%s/%s/%s--%s"
                                % (game_code, game_region, region_servers, language)
                            ]
                        if not existing_choice:
                            if "zip" in server_data:
                                character_name_matchers.append(
                                    re.compile("^" + server_data["zip"])
                                )
                        if "sub_keys" in server_data:
                            localized_server_area_choices = _make_choices(server_data)
                            server_area_choices += localized_server_area_choices
                            existing_choice = region_servers_area is not None
                            matched_server_area = region_servers_area = _match_choices(
                                address.get("region_servers_area"), localized_server_area_choices
                            )
                            if matched_server_area:
                                if is_default_language:
                                    server_area_data = database[
                                        "%s/%s/%s/%s"
                                        % (game_code, game_region, region_servers, region_servers_area)
                                    ]
                                else:
                                    server_area_data = database[
                                        "%s/%s/%s/%s--%s"
                                        % (
                                            game_code,
                                            game_region,
                                            region_servers,
                                            region_servers_area,
                                            language,
                                        )
                                    ]
                                if not existing_choice:
                                    if "zip" in server_area_data:
                                        character_name_matchers.append(
                                            re.compile("^" + server_area_data["zip"])
                                        )
        game_region_choices = _compact_choices(game_region_choices)
        region_servers_choices = _compact_choices(region_servers_choices)
        server_area_choices = _compact_choices(server_area_choices)

    return ValidationRules(
        game_code,
        game_name,
        game_short_name,
        game_full_name ,
        address_format,
        allowed_fields,
        required_fields,
        upper_fields,
        game_region_type,
        game_region_choices,
        region_servers_type,
        region_servers_choices,
        character_name_type,
        character_name_matchers,
        character_name_prefix,
    )


class InvalidAddress(ValueError):
    def __init__(self, message, errors):
        super(InvalidAddress, self).__init__(message)
        self.errors = errors


def _normalize_field(name, rules, data, choices, errors):
    value = data.get(name)
    if name in rules.upper_fields and value is not None:
        value = value.upper()
        data[name] = value
    if name not in rules.allowed_fields:
        data[name] = ""
    elif not value and name in rules.required_fields:
        errors[name] = "required"
    elif choices:
        if value or name in rules.required_fields:
            value = _match_choices(value, choices)
            if value is not None:
                data[name] = value
            else:
                errors[name] = "invalid"
    if not value:
        data[name] = ""


def normalize_address(address):
    errors = {}
    try:
        rules = get_validation_rules(address)
    except ValueError:
        errors["game_code"] = "invalid"
    else:
        cleaned_data = address.copy()
        game_code = cleaned_data.get("game_code")
        if not game_code:
            errors["game_code"] = "required"
        else:
            cleaned_data["game_code"] = game_code.upper()
        _normalize_field(
            "game_region", rules, cleaned_data, rules.game_region_choices, errors
        )
        _normalize_field("region_servers", rules, cleaned_data, rules.region_servers_choices, errors)
        _normalize_field(
            "region_servers_area", rules, cleaned_data, rules.server_area_choices, errors
        )
        _normalize_field("character_name", rules, cleaned_data, [], errors)
        character_name = cleaned_data.get("character_name", "")
        if rules.character_name_matchers and character_name:
            for matcher in rules.character_name_matchers:
                if not matcher.match(character_name):
                    errors["character_name"] = "invalid"
                    break
        _normalize_field("street_address", rules, cleaned_data, [], errors)
        _normalize_field("sorting_code", rules, cleaned_data, [], errors)
    if errors:
        raise InvalidAddress("Invalid address", errors)
    return cleaned_data


def _format_address_line(line_format, address, rules):
    def _get_field(name):
        value = address.get(name, "")
        if name in rules.upper_fields:
            value = value.upper()
        return value

    replacements = {
        "%%%s" % code: _get_field(field_name)
        for code, field_name in FIELD_MAPPING.items()
    }

    fields = re.split("(%.)", line_format)
    fields = [replacements.get(f, f) for f in fields]
    return "".join(fields).strip()


def get_field_order(address, latin=False):
    """
    Returns expected order of address form fields as a list of lists.
    Example for PL:
    >>> get_field_order({'game_code': 'PL'})
    [[u'name'], [u'company_name'], [u'street_address'], [u'character_name', u'region_servers']]
    """
    rules = get_validation_rules(address)
    address_format = rules.address_format
    address_lines = address_format.split("%n")
    replacements = {
        "%%%s" % code: field_name for code, field_name in FIELD_MAPPING.items()
    }
    all_lines = []
    for line in address_lines:
        fields = re.split("(%.)", line)
        single_line = [replacements.get(field) for field in fields]
        single_line = list(filter(None, single_line))
        all_lines.append(single_line)
    return all_lines


def format_address(address, latin=False):
    rules = get_validation_rules(address)
    address_format = rules.address_format
    address_line_formats = address_format.split("%n")
    address_lines = [
        _format_address_line(lf, address, rules) for lf in address_line_formats
    ]
    address_lines.append(rules.game_name)
    address_lines = filter(None, address_lines)
    return "\n".join(address_lines)


def latinize_address(address, normalized=False):
    if not normalized:
        address = normalize_address(address)
    cleaned_data = address.copy()
    game_code = address.get("game_code", "").upper()
    dummy_game_data, database = _load_game_data(game_code)
    if game_code:
        game_region = address["game_region"]
        if game_region:
            key = "%s/%s" % (game_code, game_region)
            game_region_data = database.get(key)
            if game_region_data:
                cleaned_data["game_region"] = game_region_data.get(
                    "lname", game_region_data.get("name", game_region)
                )
                region_servers = address["region_servers"]
                key = "%s/%s/%s" % (game_code, game_region, region_servers)
                server_data = database.get(key)
                if server_data:
                    cleaned_data["region_servers"] = server_data.get(
                        "lname", server_data.get("name", region_servers)
                    )
                    region_servers_area = address["region_servers_area"]
                    key = "%s/%s/%s/%s" % (game_code, game_region, region_servers, region_servers_area)
                    server_area_data = database.get(key)
                    if server_area_data:
                        cleaned_data["region_servers_area"] = server_area_data.get(
                            "lname", server_area_data.get("name", region_servers_area)
                        )
    return cleaned_data
