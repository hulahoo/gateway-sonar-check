from typing import Dict

from events_gateway.config.log_conf import logger


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
    logger.info(f"Keys:{keys}, values:{values}")
    matched_key_value = list(zip(keys, values))
    logger.info(f"MATHCED PAIRS: {matched_key_value}")
    result_dict = dict()
    for pair in matched_key_value:
        tmp = dict()
        key, value = pair
        child_key, child_value = value.split(":", 1) if ":" in value else value
        tmp[child_key] = child_value
        result_dict[key] = tmp
    logger.info(f"Result: {result_dict}")
    return result_dict
