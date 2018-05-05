FAST Pipeline for data reduction
======================================

[![Build Status](https://travis-ci.org/PennyQ/FAST-scripts.svg?branch=master)](https://travis-ci.org/PennyQ/FAST-scripts)

INSTRUCTIONS
------------
### Prepare data

Be sure your data is put in the `test_data` folder, with the format downloaded from remote server.

### Download the code and install

In your terminal, type `git clone https://github.com/PennyQ/FAST-scripts.git` to download the code;

Go to the downloaded code directory and install with `python setup.py install`, this should grab all dependencies and automatically install them.


### Run the pipeline - Interactive mode

In the current pipeline directory, type `cd pipeline`;

Start the pipeline with typing the command in terminal `fastpipeline`;

Select local mode, follow the instructions on terminal to set object directory

**If select remote mode, edit the config_properties.py properly**

### Output

The plot of results should pop up during the interaction, also, figures are saved in the `pipeline/output` folder.

Status
------------
Support for remote access is still under development, currently the frequency information can be extracted from remote file set in the *config_properties.py*.
   
