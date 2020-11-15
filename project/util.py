def serialize_data(data, schema):
    serialized_data = []
    if schema:
        if type(data) != list:
            return {k:v for (k,v) in data.__dict__.items() if k in schema.__fields__}
        else:
            for obj in data:
                serialized_data.append({k:v for (k,v) in obj.__dict__.items() if k in schema.__fields__})
    return serialized_data


