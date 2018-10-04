This is an example usage of processor and the processor-executors.

* We have a censor that takes an input (text to censor, configuration what to censor) and result the censored version of the text.

Usage: (replace <text> and <config>)

```
python censor.py \<text\> \<config\>
```

Example with "plain text" parameters:
```
python censor.py '"This is a good idea!"' '{"censored_words": ["good", "bad"]}'
```

Example if we want to read the parameters from a file:

```
python censor.py "$(< input/drama.txt)" "$(< censor_config.json)"
```

It gets more and more complicated:

* We would like to save the result in a file
* We would like to iterate over a directory to process all the files and save it
* We might want to log the result and indicate the progress
* We might want to run these with paralell
* ...

This is how the processor-executors given by this library can help.

## File based executor

```
python ../file_executor.py -i ./input/comedy.txt  -o ./output/comedy.censored -p ./censor.py -c '{"censored_words": ["Good", "Bad"] }'
cat ./output/comedy.censored
```

## Dir based executor

```
python ../dir_executor.py -i ./input -ie txt -o ./output -oe censored -p ./censor.py -c '{"configs": [ {"censored_words": ["Good", "Bad"] }, {"censored_words": ["Good", "Bad"] }  ] }'
```

The script above does the following:
1. Got an input (-i) directory where to look for the input
2. Got an input extensions (-ie) what files with extension to collect
3. Got an output directory (-o) where to save the output
4. Got an output extension (-oe) and will replace the input extension with the output extension. eg.: input.txt -> input.censored
5. Got the path to the processor file (NOTE: install all dependencies that required to run processor)
6. Got a configuration json (it works with a path to the config file as well) and starts as many process of the given processor as many configuration got in the parameter list.
