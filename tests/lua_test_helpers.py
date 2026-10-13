import json
def lua_data(value):
    if isinstance(value,dict): return "{"+",".join("["+json.dumps(k)+"]="+lua_data(v) for k,v in value.items())+"}"
    if isinstance(value,list): return "{"+",".join(lua_data(v) for v in value)+"}"
    if isinstance(value,bool): return str(value).lower()
    return json.dumps(value)
