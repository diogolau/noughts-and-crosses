import json

def binary_to_dict(b_message):
    json_message = b_message.decode("utf-8")
    dict_message = json.loads(json_message)

    return dict_message

def dict_to_binary(dict):
    json_dict = json.dumps(dict)
    b_message = bytes(json_dict, encoding="utf-8")

    return b_message