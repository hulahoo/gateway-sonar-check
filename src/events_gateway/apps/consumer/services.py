from typing import Dict

from config.log_conf import logger


def convert_to_dict(*, incoming_events: str) -> Dict[str, Dict[str, str]]:
    logger.info(f"Incoming events: {incoming_events}")
    splitted_event = incoming_events.split(" ")
    keys = []
    values = []
    for element in splitted_event:
        if ":" not in element and "%" not in element:
            keys.append(element)
        else:
            values.append(element)
    matched_key_value = list(zip(keys, values))
    result_dict = dict()
    for pair in matched_key_value:
        tmp = dict()
        key, value = pair
        tmp[key] = value.split(":", 1)[-1] if ":" in value else value
        result_dict[key] = tmp
    return result_dict


def base_field_extractor(data: dict):
    types = ('json', 'stix', 'free_text', 'misp', 'csv', 'txt')
    base_fields = ["name"]

    for field in base_fields:
        if field not in data:
            for key in data:
                if field in key.lower():
                    data[field] = data[key]
                    break
    if 'type' not in data and data['type'] not in types:
        data['type'] = 'json'
