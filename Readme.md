# Introduction

Python scripts for helping text processing. I usually have the typical scenario for several python scripts used for text processing:

1. Process some input text and produce some output text (eg.: parse an article from html) 
    -> these are processors reading standard in and printing result to standard out
2. The input was mostly stored in a file so I should read it and save the result to another file 
    -> this is file\_executor.py that takes an input file, output file a script and a configuration.
3. However it was not just a single file but most of the times there are a bunch of files I required to process, log the result and progress. 
    -> this is files\_executor.py that takes input-output file pairs a script and a configuration then
       its responsibility is to log execution progress and result and use file executor to execute it.
       Beside that processing can be parallelized configure it in the config file
4. It is rare that I have a list of input-output file list but mostly I have an input directory with 
   a number of specific files and an output directory where to save. 
    -> this dir\_executor.py takes the responsibility to enumerate a directory for looking files with specific extensions
       then generate the input-output pairs and call files\_executor.py with it.

To eliminate implementing those function over and over again I created this project. There are might better open source alternatives but I didn't find them.

# Dependencies

Python 3.x

# Usage

Check out this repository into your python environment and use the scripts as described below and in the ./example/Readme.md.

## file\_executor

```
python file_executor.py -i <input_path> -o <output_path> -p <processor_path> -c <config_path>
```

## dir\executor
```
python dir_executor.py -i <input_dir> -ie <input_files_extension> -o <output_dir> -oe <output_files_extension> -p <processor_path> -c <processor_config_file>
```

Processor config file must have the following json structure:
```
{
    // The dir_processor.py will paralellize text processing with the # of config (eg.: the config below will be executed on 2 threads). The multiple config is used for that purpose to paralelize execution or run the same processor with different configurations at the same time (if you need to run different configurations on the same input).
    "configs": [
        {"key1":"value1", "key2":"value2"}, // config parameters for processor
        ...
        {"key1":"value1", "key2":"value2"} // config parameters for processor
    ]
}
```

# Example

See the Readme.md on the example folder.

# Known issues:

If a processor exited unexpectedly (eg.: calling sys.exit()) then the files_exeuctor.py will stuck. Raise an error instead of exit. The issues detail: 
https://bugs.python.org/issue9205

