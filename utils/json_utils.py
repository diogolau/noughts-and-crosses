import json

def binary_to_json(b_message):
        json_message = json.loads(b_message)

        return json_message

def json_to_binary(json_message):
        b_message = (json.dumps(json_message)).encode()

        return b_message