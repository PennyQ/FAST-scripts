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

# TODO: In the future, add functionality to automatically seperate \
# first/second on off files; should not have intermediate folders to store

# TODO: In the future, when deal with stacks of data, we should enable \
# output plots in the data folder

# TODO: change the code to OOP style; each pipeline task should be a class
# with fields set by constructor

# TODO: add a progress bar for loading fits data based on time.txt

# =============User input initiation================#
cwd = os.getcwd()
dirname = os.path.dirname(cwd)
obj_name = str(raw_input('Please type the folder name: '))
obj_path = os.path.join(os.path.dirname(cwd), 'test_data', obj_name)

# Allow three times of input trials
for i in range(3):
    if not os.path.exists(obj_path):
        print('not path')
        obj_name = str(raw_input('Path - %s - does not exist \n '
                                 'Please retype : ' % obj_path))
        obj_path = os.path.join(os.path.dirname(cwd), 'test_data', obj_name)

freq = raw_input("enter freqency range (separated by a comma):").split(',')

tick_num = raw_input("Please enter tick number [1001]:") or 1001

smooth_box = raw_input('Please type the smoothing width of the boxcar' +
                       'average: [10]') or 10
bsl_flag = True
if raw_input('Baselining the result? [y/n] default as yes').lower() == 'n':
    bsl_flag = False

time_info = read_time_txt(obj_path)
print('time_info', time_info)
ses_on_data, ses_off_data = read_on_off_data_by_time(time_info, obj_path)

freq = np.linspace(float(freq[0]), float(freq[1]), ses_on_data.shape[0])

print('ses_on_data', ses_on_data, ses_on_data.shape)
print('ses_off_data', ses_off_data, ses_off_data.shape)

sessions_mean = np.zeros(ses_on_data.shape[0])
try:
    for i in range(ses_on_data.shape[2]):
        print('ses_on_data[..., i]', ses_on_data[..., i].shape)
        ses_on_data_bdp = np.mean(bdp_correction(ses_on_data[..., i], freq), axis=1)
        ses_off_data_bdp = np.mean(bdp_correction(ses_off_data[..., i], freq), axis=1)
        ses_on_off = plot_each_session(ses_on_data_bdp, ses_off_data_bdp, freq, obj_name, bsl_flag)
        sessions_mean += ses_on_off


except IndexError:  # only one session
    print('ses_on_data[..., i]', ses_on_data[..., i].shape)
    ses_on_data_bdp = np.mean(bdp_correction(ses_on_data[..., i], freq), axis=1)
    ses_off_data_bdp = np.mean(bdp_correction(ses_off_data[..., i], freq), axis=1)
    ses_on_off = plot_each_session(ses_on_data_bdp, ses_off_data_bdp, freq, obj_name, bsl_flag)
    sessions_mean = ses_on_off

plot_mean_sessions(freq, sessions_mean, smooth_box, bsl_flag)

# # =============== first session on off plot======================#
#
# first_on_data = read_data(os.path.join(obj_path, 'first-on'))
# first_off_data = read_data(os.path.join(obj_path, 'first-off'))
#
# first_on = np.mean(bdp_correction(first_on_data, freq), axis=1)
# first_off = np.mean(bdp_correction(first_off_data, freq), axis=1)
#

#
# # ===============second session on off plot======================#
#
# second_on_data = read_data(os.path.join(obj_path, 'second-on'))
# second_off_data = read_data(os.path.join(obj_path, 'second-off'))
#
# second_on = np.mean(bdp_correction(second_on_data, freq), axis=1)
# second_off = np.mean(bdp_correction(second_off_data, freq), axis=1)
#
# second_on_off = plot_each_session(second_on, second_off, freq, 'second',
#                                   bsl_flag)
#
#
# # ============= plot ON-OFF data ====================#
# sessions_mean = (first_on_off + second_on_off)/2.
#
# # print(np.min(first_second_mean), np.argmin(first_second_mean))
# # print('signal at '+str(1354.3+np.argmin(first_second_mean)/1000.)+' MHz')
#
# plot_mean_sessions(freq, sessions_mean, smooth_box, bsl_flag)

print('Pipeline quit!')
