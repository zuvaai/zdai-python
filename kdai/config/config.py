import json
import os
import shutil


def _get_config_data(config_name):
    fullname = os.path.join(os.path.dirname(__file__), config_name)

    if not os.path.exists(fullname):
        raise FileNotFoundError(f'Could not find {fullname}')
    else:
        with open(fullname, 'r') as file:
            config = json.load(file)

        return config


def get_access_config():
    config = _get_config_data('access.json')
    return config


def get_access():
    config = get_access_config()
    url = config.get('url')
    token = config.get('token')
    return url, token


def update_wrapper_config(token: str = None, url: str = None):
    config = get_access_config()
    _file = os.path.join(os.path.dirname(__file__), 'access.json')

    if token:
        config['token'] = token
    if url:
        config['url'] = url

    with open(_file, "w") as file:
        json.dump(config, file, indent = 4)


def create_wrapper_config():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    template_file = os.path.join(cur_dir, 'access.json.template')
    new_file = os.path.join(cur_dir, 'access.json')
    if not os.path.exists(os.path.join(cur_dir, 'access.json')):
        shutil.copy(template_file, new_file)
