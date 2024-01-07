CONFIG = {
    "user": "",
    "password": "",
    "target": "",
    "email" : "",
    "bio" : "",
    'name' : '',
    'phone' : ''

}
def read_config(key):
    return CONFIG.get(key)

def update_config(key, value):
    CONFIG[key] = value

def remove_config(key):
    removed_value = CONFIG.pop(key, None)
    return removed_value