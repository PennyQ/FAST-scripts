from astropy.io import fits
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from scipy import ndimage
from datetime import datetime


def bdp_correction(data, freq):
    data_after_bdp = None

    # iterate data with each spectra
    for spectra in np.nditer(data, flags=['external_loop'], order='F'):
        good_data_index = range(spectra.shape[0])

        # calculate 3 times for bandpass fitting and data filterring
        for k in range(3):
            #  select good data only with good_data_index indexing
            freq_sel = freq[good_data_index]
            data_sel = spectra[good_data_index]

            # bdp curve fitting
            polyfit = np.poly1d(np.polyfit(freq_sel, data_sel, 1))  # x, y, degree
            bdp_curv = polyfit(freq)

            # calculate residual and corresponding rms
            res_signal = abs(spectra) - polyfit(freq)
            rms = np.std(res_signal)

            # get index for good data
            good_data_index = np.where(res_signal <= 3.*rms)

        try:
            bdp_curv = bdp_curv/np.median(bdp_curv)  # normalization
        except ZeroDivisionError:
            bdp_curv = bdp_curv
        nor_bdp = spectra/bdp_curv
        nor_bdp = nor_bdp.reshape(nor_bdp.shape[0], 1)  # reshape for appending
        # print('spectra/bdp_curv - new', nor_bdp.shape)

        if data_after_bdp is None:
            data_after_bdp = nor_bdp
        else:
            data_after_bdp = np.append(data_after_bdp, nor_bdp, axis=1)  # bdp correction
            # print('data_after_bdp', data_after_bdp.shape)
            # print('spectra/bdp_curv', (spectra/bdp_curv).shape)
    return data_after_bdp


def baselined(freq, on_off):
    # bdp curve fitting
    polyfit = np.poly1d(np.polyfit(freq, on_off, 1))  # x, y, degree
    bsl_curv = polyfit(freq)
    return (on_off - bsl_curv)


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
    except OSError:
        print('File that saves on/off recoding time is not found,'
              'please check!')
        sys.exit()
    return on_start_time, on_end_time, off_start_time, off_end_time


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
    print('on_start_time length', len(on_start_time))
    ses_on_data = None
    ses_off_data = None
    for i in range(ses):
        on_data = None  # shape of (freq_index, record_index, session_idx)
        off_data = None
        for record_dir_path in os.listdir(os.path.join(obj_path, 'fits')):

            each_record_path = os.path.join(obj_path, 'fits', record_dir_path)

            if os.path.isfile(each_record_path) and 'fit' in os.path.basename(each_record_path):
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
                        # TODO: progress bar can use the loop here
                        # print('on_data shape in for loop', on_data.shape)

                if off_start_time[ses - 1] <= f_time <= off_end_time[ses - 1]:
                    if off_data is None:
                        off_data = data_linear
                    else:
                        off_data = np.append(off_data, data_linear, axis=1)
                hdulist.close()


        if ses_on_data is None:
            print('if ses on data is None', on_data.shape)
            ses_on_data = on_data
        else:
            print('else, ses_on_dat, on_data shape', ses_on_data.shape, on_data.shape)
            ses_on_data = np.stack((ses_on_data, on_data), axis=-1)

        if ses_off_data is None:
            ses_off_data = off_data
        else:
            ses_off_data = np.stack((ses_off_data, off_data), axis=-1)
    return ses_on_data, ses_off_data


# # plot bdp corrected, baselined for each session
def plot_each_session(on, off, freq, obj_name, bsl_flag=True):
    """
    :return: ON-OFF of each session, in numpy.array type.
    """
    # initiate the plot
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    # read between 2100-2110 as first on

    ax1.plot(freq, on)  # label='first on')
    ax1.set_title(obj_name + ' on')

    # ax1.legend(loc="upper right")

    # read between 2120-2130 as first off
    ax2.plot(freq, off)
    ax2.set_title(obj_name+' off')

    on_off = on - off
    # ax3.set_title('first on minus off')
    # ax3.set_ylim(-1, 1.5)
    ax3.set_title(obj_name+' on minus off')
    if bsl_flag:
        on_off = baselined(freq, on_off)
        ax3.set_title(obj_name+' on minus off - baselined')

    ax3.plot(freq, on_off)

    # ax1.ylabel('first on minus off')

    f.subplots_adjust(hspace=1)

    # plt.xlim(1381.8, 1387.8)
    # axes.set_ylim([ymin,ymax])
    # plt.ylim(4.5, 6)
    plt.savefig(obj_name+'-on-off', dpi=300)
    plt.show()
    # hdulist = fits.open('data_20171103T215857.fits')

    # plt.plot(hdulist[0].data)
    # plt.show()
    print('Plot and save ' + obj_name+' on minus off')
    return on_off


# plot bdp corrected, baselined, and smoothed data
def plot_mean_sessions(freq, sessions_mean, smooth_box, bsl_flag=True):
    if bsl_flag:
        sessions_mean = baselined(freq, sessions_mean)
    # smooth function is from IDL http://www.harrisgeospatial.com/docs/SMOOTH.html
    sessions_mean = ndimage.filters.uniform_filter(sessions_mean,
                                                   size=int(smooth_box))

    plt.plot(freq, sessions_mean)
    plt.annotate('Signal at '+str(freq[0]+np.argmin(sessions_mean)/1000.*6)
                 + ' MHz',
                 xy=(freq[0], 1e-12),
                 xytext=(freq[1], 1e-12),
                 arrowprops=dict(arrowstyle="->"))
    print('Plot and save ON-OFF (Baselined)')

    plt.title('ON-OFF (Baselined)')
    plt.savefig('bdp-smoothed-bsl', dpi=300)
    plt.show()
