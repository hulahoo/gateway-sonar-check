import json

from loguru import logger


def clean_item(i: str):
    i = f"'{i.strip()}'"
    return i


def txt_to_normal(s: str):
    index = 0
    temp = ''
    dct = {'': None, "{": "}", "[": "]"}
    CUSTOM_CHAR = '  ' + ';;;' + '  '
    CUSTOM_CHAR_END = ',;;;,'

    for key in dct:
        if key in s:
            index_ = s.index(key)
        else:
            continue

        if index_ > index:
            index = index_
            temp = key
    end_key = dct[temp]
    if end_key:
        end_index = s.rindex(end_key)
        start = s[:index + 1]
        middle = s[index + 1:end_index].replace(f'{end_key},{temp}', CUSTOM_CHAR).strip()
        end = s[end_index:]

        if '=' in start:
            a_, b_ = start.split('=')
            start = f"'{a_}':{b_}"
        elif ':' in start:
            a_, b_ = start.split(':')
            start = f"'{a_}':{b_}"

    else:
        end_index = len(s)
        start = s[:index]
        middle = s[index:end_index].replace(f'{end_key},{temp}', CUSTOM_CHAR).replace('  ', ' ')
        end = s[end_index:]

    # start = s[:index]
    # middle = s[index:end_index]
    # end = s[end_index:]

    items = middle.split('  ')
    items_new = []

    split_char = '=' if '=' in middle else ':'

    for i in items:
        if ', ' in i:
            # тогда это массив
            a, b = i.split(split_char, maxsplit=1)
            b_items = b.split(',')

            ab = f"'{a.strip()}': [" + ','.join(list(map(lambda x: clean_item(x), b_items))) + "]"

            items_new.append(ab)
        else:
            try:
                a, b = i.split(split_char, maxsplit=1)

                items_new.append(f"'{a.strip()}':'{b}'")
            except Exception as e:
                logger.exception(f"Error occured: {e}")
                items_new.append(i)
    final = f'{start} {",".join(items_new)} {end}'.replace(CUSTOM_CHAR_END, f"{end_key},{temp}")
    return final


def clean(s: str):
    if '	' in s:
        # 'srcNetName:GO_RSHB.City.City_users   RE_IP RE_DATE'
        s = s.split('	', maxsplit=1)[0]
    if '   ' in s:
        s = s.split('   ', maxsplit=1)[0]
    s = s.replace('%', '')

    if ':' in s or '=' in s:
        return s, True

    return s, False


def log_text_to_json(text: str, pattern: str):
    text = text.split('	')
    text_new = []
    index = 0
    size = len(text)
    is_array = False
    is_dict = False

    for k in range(size):

        i = text[k]
        if '[' in i:
            text_new.append(i)
            is_array = True
            index = len(text_new) - 1
            continue
        if ']' in i and is_array:
            is_array = False
            text_new[index] += f' {i}'
            text_new.append('')
            continue

        if is_array:
            text_new[index] += f' {i}'
            continue

        if '{' in i:
            text_new.append(i)
            is_dict = True
            index = len(text_new) - 1
            continue
        if '}' in i and is_dict:
            is_dict = False
            text_new[index] += f'  {i}'
            text_new.append('')
            continue

        if is_dict:
            text_new[index] += f'  {i}'
            continue

        if ':' in i or '=' in i:
            text_new.append(i)
        else:
            if len(text_new) > 0:
                text_new[len(text_new) - 1] += f'  {i}'
            else:
                text_new.append(i)
                index += 1
            text_new.append(i)
    text_new_copy = text_new.copy()
    text_new = []
    for i, value in enumerate(text_new_copy):
        value_, is_normal = clean(value)
        if not is_normal:
            pass
        else:
            text_new.append(value_)

    dct = []
    for j in text_new:
        try:
            dct.append(txt_to_normal(j))
        except Exception as e:
            logger.exception(f"Error is occured: {e}")
            pass

    dct = ','.join(dct)
    dct = ('{' + dct + '}').replace('\'', '\"')
    dct = json.loads(dct)
    return dct


def base_field_extractor(data: dict):
    types = ('json', 'stix', 'free_text', 'misp', 'csv', 'txt')
    base_fields = ["name"]

    for field in base_fields:
        if field not in data:
            for key in data:
                if field in key.lower():
                    data[field] = data[key]
                    break
    if 'type' in data and data['type'] in types:
        pass
    else:
        data['type'] = 'json'
