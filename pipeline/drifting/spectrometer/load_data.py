from astropy.io import fits
import os
import sys
import numpy as np
from datetime import datetime


def progress_bar(val, val_max, val_min=0, prefix='', suffix='', bar_len=20):
    """
    Displays a progress bar when loading data.
    :param val: current value
    :param val_max: maximum value
    :param val_min: minimum value
    :param prefix: marker for the completed part
    :param suffix: marker for the incomplete part
    :param bar_len: total length of the progress bar
    :return: a string representation of the progressbar
    """
    if val_max == 0:
        return ''
    else:
        skipped_len = int(round(bar_len * val_min) / float(val_max))
        filled_len = int(round(bar_len * (val - val_min) / float(val_max)))
        # percents = round(100.0 * count / float(total), 1)
        bar = '.' * skipped_len + '|' * filled_len + '.' * (bar_len - filled_len - skipped_len)
        # return '[%s] %s%s %s\r' % (bar, percents, '%', suffix)
        return '%s [%s] %s\r' % (prefix, bar, suffix)


def read_data(path, data=None):
    try:
        for dir_entry in os.listdir(path):
            dir_entry_path = os.path.join(path, dir_entry)
            if os.path.isfile(dir_entry_path) and 'fit' in dir_entry_path:
                hdulist = fits.open(dir_entry_path)
                # unit of dB tranfering a into linear space
                data_linear = np.power(10.0, hdulist[0].data/10.0)
                if data is None:
                    data = data_linear
                else:
                    data = np.append(data, data_linear, axis=1)
                hdulist.close()
    except OSError:
        # If the folder path is wrong after three trials
        print("Invalid folder input, please check the folder existance.")
        sys.exit()
    return data  # as a numpy array


def read_time_txt(obj_path):
    try:
        if os.path.isfile(os.path.join(obj_path, 'time.txt')):
            t_array = []
            for each_line in open(os.path.join(obj_path, 'time.txt')).read().decode('utf-8').split():
                if each_line[0].isdigit():
                    print(each_line.encode('utf-8'))
                    t_array.append(each_line.encode('utf-8'))
            on_start_time = []  # for each session
            on_end_time = []
            off_start_time = []
            off_end_time = []
            print('t_array', t_array)
            for i in range(len(t_array)):
                if i % 4 == 0:
                    on_start_time.append(datetime.strptime(t_array[i], '%H:%M'))
                if i % 4 == 1:
                    on_end_time.append(datetime.strptime(t_array[i].replace('-', ''), '%H:%M'))
                if i % 4 == 2:
                    off_start_time.append(datetime.strptime(t_array[i], '%H:%M'))
                if i % 4 == 3:
                    off_end_time.append(datetime.strptime(t_array[i].replace('-', ''), '%H:%M'))
            print('on_start_time', on_start_time, len(on_start_time))
            print('on_end_time', on_end_time)
            print('off_start_time', off_start_time)
            print('off_end_time', off_end_time)
            return on_start_time, on_end_time, off_start_time, off_end_time
    except OSError:
        print('File that saves on/off recoding time is not found,'
              'please check!')
        sys.exit()


def read_on_off_data_by_time(time_info, obj_path):
    """
    Read fits data to different array based on session stage, fits data expected to be saved in
    FAST - scripts / test_data / AGC12885 / fits

    :param time_info: An array includes start and end time for each session.
    :param obj_path: Absolute path of the object directory.
    """
    on_start_time, on_end_time, off_start_time, off_end_time = time_info

    # read files from the data folder between start - end to an array
    ses = len(on_start_time)
    ses_on_data = None
    ses_off_data = None
    fits_total_num = [0]*ses

    print('Reading data by time for [%d] Sessions' % ses)

    # Get total number of files to be loaded, for progress bar
    for i in range(ses):
        for record_dir_path in os.listdir(os.path.join(obj_path, 'fits')):

            each_record_path = os.path.join(obj_path, 'fits', record_dir_path)

            if os.path.isfile(each_record_path) and '.fit' in os.path.basename(each_record_path):
                # unit of dB tranfering a into linear space
                f_time = os.path.basename(each_record_path).split('T')[1]  # time in file name
                f_time = f_time.split('.')[0]

                # format time to python datetime format
                f_time = datetime.strptime(f_time[0:4], '%H%M')
                if on_start_time[ses - 1] <= f_time <= on_end_time[ses - 1]:
                    fits_total_num[i] += 1

    for i in range(ses):
        on_data = None  # shape of (freq_index, record_index, session_idx)
        off_data = None

        toolbar_width = 100
        # setup toolbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width + 1))  # return to start of line, after '['

        for record_dir_path in os.listdir(os.path.join(obj_path, 'fits')):

            each_record_path = os.path.join(obj_path, 'fits', record_dir_path)

            if os.path.isfile(each_record_path) and '.fit' in os.path.basename(each_record_path):
                hdulist = fits.open(each_record_path)

                # unit of dB tranfering a into linear space
                data_linear = np.power(10.0, hdulist[0].data/10.0)
                f_time = os.path.basename(each_record_path).split('T')[1]  # time in file name
                f_time = f_time.split('.')[0]

                # format time to python datetime format
                f_time = datetime.strptime(f_time[0:4], '%H%M')
                if on_start_time[ses - 1] <= f_time <= on_end_time[ses - 1]:
                    if on_data is None:
                        on_data = data_linear
                    else:
                        on_data = np.append(on_data, data_linear, axis=1)

                        progressbar = progress_bar(val=on_data.shape[1],
                                                   val_max=fits_total_num[i],
                                                   bar_len=30)
                        sys.stdout.write('Loading session %d : %s' % (i+1, progressbar))
                        sys.stdout.flush()

                if off_start_time[ses - 1] <= f_time <= off_end_time[ses - 1]:
                    if off_data is None:
                        off_data = data_linear
                    else:
                        off_data = np.append(off_data, data_linear, axis=1)
                hdulist.close()

        if ses_on_data is None:
            ses_on_data = on_data
        else:
            ses_on_data = np.stack((ses_on_data, on_data), axis=-1)

        if ses_off_data is None:
            ses_off_data = off_data
        else:
            ses_off_data = np.stack((ses_off_data, off_data), axis=-1)
    return ses_on_data, ses_off_data
