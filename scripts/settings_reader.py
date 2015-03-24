import sys
import json
from os.path import dirname, isdir, isfile, join, realpath
from os import makedirs

# -------------------------------
# Input/Output directories
# -------------------------------
PROJ_DIR = realpath(dirname(dirname(__file__)))
INPUT_DIR = join(PROJ_DIR, 'query_lists')
OUTPUT_DIR = join(PROJ_DIR, 'query_counts')
for d in (INPUT_DIR, OUTPUT_DIR):
    if not isdir(d):
        makedirs(d)


# -------------------------------
# Settings file: Log Path and Delimiter
# -------------------------------
JSON_SETTINGS_FILE_NAME = 'settings.json'
SETTINGS_KEY_LOG_PATH = 'GLASSFISH_LOG_FILE_PATH'
SETTINGS_KEY_DELIMITER = 'DELIMITER'
DEFAULT_DELIMITER ='_YE_OLDE_QUERY_COUNTER_'


def get_settings_dict():
    """
    Pull the Glassfish Log Path and Delimiter from a JSON file
    """
    assert isfile(JSON_SETTINGS_FILE_NAME), "Could not find settings file: %s" % JSON_SETTINGS_FILE_NAME

    try:
        json_params = json.loads(open(JSON_SETTINGS_FILE_NAME, 'r').read())
    except Exception as e:
        print e.message, e.args
        assert False, 'Failed to open settings file as JSON.  File name: %s' % JSON_SETTINGS_FILE_NAME

    assert json_params.has_key(SETTINGS_KEY_LOG_PATH), 'Key "%s" not found in settings file "%s"' % (SETTINGS_KEY_LOG_PATH, JSON_SETTINGS_FILE_NAME)

    if not json_params.has_key(SETTINGS_KEY_DELIMITER):
        json_params[SETTINGS_KEY_DELIMITER] = DEFAULT_DELIMITER

    return json_params