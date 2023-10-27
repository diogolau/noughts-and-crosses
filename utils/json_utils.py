import json

def binary_to_json(b_message):
        json_message = json.loads(b_message)

        return json_message

def json_to_binary(str_message):
        b_message = (json.dumps(str_message)).encode()

        return b_message