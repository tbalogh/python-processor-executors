import sys, os, json

def read(path):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    return ""

def error(message, ex):
    sys.stderr.write("\n" + message + "\n")
    raise ex

def read_config(config_param):
    if type(config_param) is dict:
        if 'censored_words' in config_param.keys():
            return config_param
        else:
            error("The given config does not contains censored_words: " + str(config_param), Exception(""))
        
    try:
        if os.path.isfile(config_param):
            with open(config_param, 'r') as f:
                return json.load(f)
        else:
            return json.loads(config_param)
    except Exception as ex:
        error("The given config param is invalid. Validate that the file exist and the json format is valid.", ex)
            

def process(text, config_param):
    config = read_config(config_param)
    words = config['censored_words']
    for word in words:
        text = text.replace(word, "-censored-")
    return text

if __name__ == '__main__':
    text = sys.argv[1]
    config_param = sys.argv[2]
    print(process(text, config_param))
