import json

# Sample dictionary
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": ["list", "of", "values"],
    "key4": {
        "nested_key": "nested_value"
    }
}

# Convert dictionary to JSON string
json_string = json.dumps(data)

# Print JSON string
print(json_string)

