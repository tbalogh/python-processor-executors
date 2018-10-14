import os, codecs, json, argparse
import importlib.util
from ast import literal_eval as make_tuple
from file_executor import execute as execute_with_file
from logger import ProcessedFileLogger
from progress_indicator import ProgressIndicator
from multiprocessing import Pool

def load_module(path):
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def read_json(path):
    with codecs.open(path, 'r', encoding='utf8') as f:
        json_content = json.load(f)

    return json_content

def validate_arguments(args):
    for input_output_pair in args.input_output_pairs:
        (input_file, output_file) = parse_input_output_pair(input_output_pair)
        assert (os.path.isfile(input_file))
    assert (os.path.isfile(args.processor))

def parse_args():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-io", "--input_output_pairs", required=True,
                          help="Input-Output pairs like <[input_file:output_file]>. Input file encoding must be utf-8.",
                          nargs="+")
    required.add_argument("-p", "--processor", required=True, help="The processor python script file")
    required.add_argument("-c", "--processor_config",
                          help="The configuration file or string (json format) that interpreted by processors")

    args = parser.parse_args()
    validate_arguments(args)

    transformed_input_output_pairs = []
    for input_output_pair in args.input_output_pairs:
        input_file, output_file = parse_input_output_pair(input_output_pair)
        transformed_input_output_pairs.append((input_file, output_file))

    return transformed_input_output_pairs, args.processor, args.processor_config


def chunk_list(some_list, num_of_chunks):
    average_length = int(len(some_list) / num_of_chunks)
    remaining = len(some_list) - (num_of_chunks * average_length)
    chunks = []

    for i in range(num_of_chunks):
        start = i * average_length
        end = (i + 1) * average_length
        chunks.append(list(some_list[start:end]))

    for i in range(remaining):
        chunks[i].append(some_list[num_of_chunks * average_length + i])

    return chunks


def parse_input_output_pair(input_output_pair):
    (input_file, output_file) = input_output_pair.split(":", 2)
    return input_file, output_file


def execute(input_output_pairs, processor_file, processor_config=None):
    """
    :param input_output_pairs: [(input_file, output_file)] list
    :param processor_file: the *processor.py absolute path
    :param processor_config: the config map that can be interpreted by the processors
    :return:
    """
    progress = ProgressIndicator("{}_process_{}".format(processor_file, str(os.getpid())),
                                 int(len(input_output_pairs)))
    progress.start()
    log = ProcessedFileLogger(os.getcwd() + os.path.sep + "execution_{}.log".format(str(os.getpid())))
    for (input_file, output_file) in input_output_pairs:
        try:
            execute_with_file(input_file, output_file, processor_file, processor_config)
            log.processed(input_file)
            progress.next()
        except Exception as e:
            log.failed(input_file + "\t" + str(e))
            progress.next()
    progress.finish()

def read_config(processor_config):
    if processor_config is not None:
        try:
            if os.path.isfile(processor_config):
                with open(processor_config, "r") as f:
                    return json.load(f)['configs']
            else:
                    return json.loads(processor_config)['configs']
        except:
            exit('Processor config can not be loaded: ' + processor_config +
                "\n Please validate that the file (or the string parameter) and the its json format is valid. The config file format is described in the Readme.md")
    else:
        return json.loads('{"configs": [ {} ]}')['configs']
        
def execute_parallel(input_output_pairs, processor_file, processor_config_param=None):
    configs = read_config(processor_config_param)
    n_parallel = len(configs) if configs is not None else 1
    chunks = chunk_list(input_output_pairs, n_parallel)
    list_of_params = []
    for i in range(n_parallel):
        list_of_params.append((chunks[i], processor_file, configs[i]))
    pool = Pool()
    pool.starmap(execute, list_of_params)


if __name__ == '__main__':
    (input_output_pairs, processor_file, processor_config) = parse_args()
    execute_parallel(input_output_pairs, processor_file, processor_config)
