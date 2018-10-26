import sys, os, codecs, argparse
from datetime import datetime
import importlib.util
import json
from bson import json_util
from pymongo import MongoClient
import pandas as pd



def load_module(path):
    sys.path.append(os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_arguments(args):
    assert (os.path.isfile(args.processor))


def parse_args():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-p", "--processor", required=True, help="The processor python script file")
    required.add_argument("-c", "--processor_config", help="The processor config string (json structured)")

    args = parser.parse_args()
    validate_arguments(args)

    return args.processor, args.processor_config

def load_config(config_param):
    try:
        if os.path.isfile(config_param):
            with open(config_param, "r") as f:
                return json.load(f)
        else:
            return json.loads(config_param)
    except:
        exit('Processor config can not be loaded: ' + config_param +
            "\n Please validate that the file (or the string parameter) and the its json format is valid.")
    
client1 = MongoClient()
db1 = client1['tbalogh']
model_collection = db1['origo_author_fix']
client2 = MongoClient()
db2 = client1['tbalogh']
morph_collection = db2['articles']

def get_moprh_ids(portal, start, end):
    morphs = morph_collection.find( \
        { \
            'portal':portal, \
            'published_time': { "$gte": start, "$lt": end } \
        }, \
        { \
            'id': 1 \
        } \
    )
    return list(morphs)

def get_models(portal, start, end):
    models = model_collection.find( \
        { \
            'portal':portal, \
            'published_time': { "$gte": start, "$lt": end } \
        }, \
        { \
            'id': 1 \
        } \
    )
    return list(models)

def get_models_by_filter_ids(portal, start, end, ids, limit):
    models = model_collection.find( \
        { \
            'portal':portal, \
            'published_time': { "$gte": start, "$lt": end }, \
            'id': {"$nin":ids}
        }
    ).limit(limit)
    return list(models)

def get_model_by_filter_ids(portal, start, end, ids):
    model = model_collection.find_one( \
        { \
            'portal':portal, \
            'published_time': { "$gte": start, "$lt": end }, \
            'id': {"$nin":ids}
        }
    )
    return model


def execute(processor_file, config_param):
    processor_module = load_module(processor_file)
    config = load_config(config_param)
    portal = config['portal']
    start = datetime(2014, 1, 1)
    end = datetime(2014, 1, 5)

    # get already processed ids
    morphs = get_moprh_ids(portal, start, end)
    morphs_df = pd.DataFrame(morphs)
    morph_ids = morphs_df['id'].tolist()

    # get not processed articles
    while(True): 
        model = get_model_by_filter_ids(portal, start, end, morph_ids)
        if model is None:
            print("Finished")
            exit()
        text = json.dumps(model, default=json_util.default)
        result = processor_module.process(text, config)
        morph = json.loads(result,object_hook=json_util.object_hook)
        print('Processed: ' + str(morph['id']))
        morph_ids.append(morph['id'])
        morph_collection.insert_one(morph)


if __name__ == '__main__':
    (processor_file, processor_config) = parse_args()
    execute(processor_file, processor_config)

    # start = datetime(2015, 10, 1)
    # end = datetime(2015, 12, 1)
    # portal = 'origo'
    # morphs = get_moprh_ids(portal, start, end)
    # morphs_df = pd.DataFrame(morphs)
    # morph_ids = morphs_df['id'].tolist()
    # print(get_model_by_filter_ids(portal, start, end, morph_ids))

    # execute("/Users/tbalogh/dev/school/new_hope/morph-analyzer/morph_analyzer.py", '{"portal":"origo", "clean":"True"}')
