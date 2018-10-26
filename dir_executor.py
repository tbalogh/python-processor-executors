import sys, os, argparse
import importlib.util
from files_executor import execute_parallel as execute_with_files


def load_module(path):
    sys.path.append(os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def validate_args(args):
    assert (os.path.isdir(args.input_dir))
    assert (os.path.isfile(args.processor))
    if args.input_filter is not None:
        assert (os.path.isfile(args.input_filter))


def parse_args():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input_dir", required=True, help="Directory of input files with utf-8 encoding")
    required.add_argument("-ie", "--input_extension", required=True, help="Extension of processable files in input_dir")
    required.add_argument("-o", "--output_dir", required=True, help="Output directory to save the processed result")
    required.add_argument("-oe", "--output_extension", required=True, help="Extension of output files")
    required.add_argument("-p", "--processor", required=True, help="The processor python script file")
    required.add_argument("-c", "--processor_config",
                          help="The configuration file or str (json format) that interpreted by processors")
    required.add_argument("-if", "--input_filter",
                          help="Filter script path that can filter the processable documents")

    args = parser.parse_args()
    validate_args(args)

    return args.input_dir, args.input_extension, args.output_dir, args.output_extension, args.processor, args.processor_config, args.input_filter


def files_ends_with_filter(ends_with):
    return lambda f: f.endswith(ends_with)


def collect_files(root_path, filter_method):
    for dir_path, dir_names, file_names in os.walk(root_path):
        for file_name in list(filter(filter_method, file_names)):
            yield os.path.join(dir_path, file_name)


def files_ends_with(root_path, ends_with):
    return collect_files(root_path, files_ends_with_filter(ends_with))


def generate_output_file_name(input_file, output_extension):
    output_extension = 'out' if len(output_extension) == 0 else output_extension
    file_name = os.path.basename(input_file)
    file_name_without_extension = os.path.splitext(file_name)[0]
    return file_name_without_extension + '.' + output_extension


def generate_output_dir(input_file, output_dir):
    input_dir = os.path.dirname(input_file)
    if len(input_dir) == 0 and len(output_dir) == 0:
        return ''
    return os.path.dirname(input_file) if len(output_dir) == 0 else output_dir


def generate_output_path(input_file, output_dir, output_extension):
    if input_file is None or len(input_file) == 0:
        raise ValueError("Generate output path failed because the input file was invalid: \t" + input_file)
    output_file_name = generate_output_file_name(input_file, output_extension)
    output_dir = generate_output_dir(input_file, output_dir)
    return output_file_name if len(output_dir) == 0 else output_dir + os.path.sep + output_file_name


def generate_input_output_pairs(input_files, output_dir, output_extension):
    input_output_pairs = []
    for input_file in input_files:
        output_path = generate_output_path(input_file, output_dir, output_extension)
        input_output_pairs.append((input_file, output_path))
    return input_output_pairs


if __name__ == '__main__':
    (input_dir, input_extension, output_dir, output_extension, processor, processor_config, input_filter_path) = parse_args()
    input_files = list(files_ends_with(input_dir, input_extension))
    all_count = len(input_files)
    if input_filter_path is not None:
        input_filter = load_module(input_filter_path)
        input_files = input_filter.process(input_files)
        filtered_count = len(input_files)
    list_of_input_output_tuples = generate_input_output_pairs(input_files, output_dir, output_extension)
    execute_with_files(list_of_input_output_tuples, processor, processor_config)
