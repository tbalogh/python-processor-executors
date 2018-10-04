import sys, os, codecs, argparse
import importlib.util


def load_module(path):
    sys.path.append(os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path):
    with codecs.open(path, 'r', encoding='utf8') as f:
        text = f.read()
    return text


def save(content, path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with codecs.open(path, "w+", encoding='utf8') as f:
        f.write(content)


def validate_arguments(args):
    assert (os.path.isfile(args.input))
    assert (not os.path.isfile(args.output))
    assert (os.path.isfile(args.processor))


def parse_args():
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group('required arguments')
    required.add_argument("-i", "--input", required=True, help="Input file with utf-8 encoding")
    required.add_argument("-o", "--output", required=True, help="Output file to save the processed result")
    required.add_argument("-p", "--processor", required=True, help="The processor python script file")
    required.add_argument("-c", "--processor_config", help="The processor config string (json structured)")

    args = parser.parse_args()
    validate_arguments(args)

    return args.input, args.output, args.processor, args.processor_config


def execute(input_file, output_file, processor_file, processor_config=None):
    processor_module = load_module(processor_file)
    text = read(input_file)
    result = processor_module.process(text, processor_config)
    save(result, output_file)


if __name__ == '__main__':
    (input_file, output_file, processor_file, processor_config) = parse_args()
    execute(input_file, output_file, processor_file, processor_config)
