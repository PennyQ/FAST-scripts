from astropy.io import fits
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from scipy import ndimage
from functions import *

# TODO: test bandpass and baseline, polish the code - wait for Bo's figures

# TODO: rephrase the comments

# TODO: modulize the pipeline
# run.py - excutive entry
# calculation.py - all scientific calculations
# plot.py - plotting codes

<<<<<<< HEAD
# TODO: automatically seperate first/second on off files;
# should not have intermediate folders to store
=======
# TODO: In the future, add functionality to automatically seperate \
# first/second on off files; should not have intermediate folders to store
>>>>>>> a75fbd94ea39ce1787d8b187b2f3caff7086e998

# TODO: In the future, when deal with stacks of data, we should enable \
# output plots in the data folder


# =============User input initiation================#
cwd = os.getcwd()
dirname = os.path.dirname(cwd)
obj_name = str(raw_input('Please type the folder name: '))
obj_path = os.path.join(os.path.dirname(cwd), 'test_data', obj_name)

# Allow three times of input trials
for i in range(3):
    if not os.path.exists(obj_path):
        print('not path')
        obj_name = str(raw_input('Path - %s - does not exist \n \
        Please retype : ' % obj_path))
        obj_path = os.path.join(os.path.dirname(cwd), 'test_data', obj_name)

freq = raw_input("enter freqency range (separated by a comma):").split(',')

tick_num = raw_input("Please enter tick number [1001]:") or 1001

freq = np.linspace(float(freq[0]), float(freq[1]), tick_num)

<<<<<<< HEAD
smooth_box = raw_input('Please type the smoothing width of the boxcar' +
                       'average: [10]') or 10
=======
smooth_box = raw_input('Please type the smoothing width of the boxcar \
                        average: [10]') or 10
>>>>>>> a75fbd94ea39ce1787d8b187b2f3caff7086e998

bsl_flag = True
if raw_input('Baselining the result? [y/n] default as yes').lower() == 'n':
    bsl_flag = False

# =============== first session on off plot======================#

first_on_data = read_data(os.path.join(obj_path, 'first-on'))
first_off_data = read_data(os.path.join(obj_path, 'first-off'))

first_on = np.mean(bdp_correction(first_on_data, freq), axis=1)
first_off = np.mean(bdp_correction(first_off_data, freq), axis=1)

first_on_off = plot_each_session(first_on, first_off, freq, 'first', bsl_flag)

# ===============second session on off plot======================#

second_on_data = read_data(os.path.join(obj_path, 'second-on'))
second_off_data = read_data(os.path.join(obj_path, 'second-off'))

second_on = np.mean(bdp_correction(second_on_data, freq), axis=1)
second_off = np.mean(bdp_correction(second_off_data, freq), axis=1)

second_on_off = plot_each_session(second_on, second_off, freq, 'second',
                                  bsl_flag)


# ============= plot ON-OFF data ====================#
sessions_mean = (first_on_off + second_on_off)/2.

# print(np.min(first_second_mean), np.argmin(first_second_mean))
# print('signal at '+str(1354.3+np.argmin(first_second_mean)/1000.)+' MHz')

plot_mean_sessions(freq, sessions_mean, smooth_box, bsl_flag)
<<<<<<< HEAD

print('Pipeline quit!')
=======
>>>>>>> a75fbd94ea39ce1787d8b187b2f3caff7086e998
