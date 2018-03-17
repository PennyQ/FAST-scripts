from astropy.io import fits
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from scipy import ndimage

# TODO: test bandpass and polish the code

# TODO: add baseline

# TODO: rephrase the comments

# TODO: modulize the pipeline
# run.py - excutive entry
# calculation.py - all scientific calculations
# plot.py - plotting codes

# TODO: In the future, add functionality to automatically seperate \
# first/second on off files

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

# if raw_input('First or Second scan [F/S]').lower() == 'f':
#     cal_mode = 'F'
# if raw_input('First or Second scan [F/S]').lower() == 'S':
#     cal_mode = 'S'

# fa=1381.8; fb =  1387.8
freq = raw_input("enter freqency range (separated by a comma):").split(',')

tick_num = raw_input("Please enter tick number [1001]:") or 1001

freq = np.linspace(float(freq[0]), float(freq[1]), tick_num)

smooth_box = raw_input('Please type the smoothing width of the boxcar \
                        average: [10]') or 10

# ===============calculations======================#


def bandpass_correction(data, freq):
    # for each spectra in data
    data_after_bdp = None

    # iterate data with each spectra
    for spectra in np.nditer(data, flags=['external_loop'], order='F'):
        good_data_index = range(spectra.shape[0])
        # calculate 3 times for bandpass fitting and subtraction
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
        print('spectra/bdp_curv', nor_bdp.shape)
        nor_bdp = nor_bdp.reshape(nor_bdp.shape[0], 1)
        print('spectra/bdp_curv - new', nor_bdp.shape)

        if data_after_bdp is None:
            data_after_bdp = nor_bdp
        else:
            data_after_bdp = np.append(data_after_bdp, nor_bdp, axis=1)  # bdp correction
            print('data_after_bdp', data_after_bdp.shape)
            print('spectra/bdp_curv', (spectra/bdp_curv).shape)
    return data_after_bdp


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
    except OSError:
        # If the folder path is wrong after three trials
        print("Invalid folder input, please check the folder existance.")
        sys.exit()
    return data  # as a numpy array


def plot_on_off(on, off, freq, mode):
    # initiate the plot
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    # read between 2100-2110 as first on

    ax1.plot(freq, on)  # label='first on')
    ax1.set_title(mode+' on')

    # ax1.legend(loc="upper right")

    # read between 2120-2130 as first off
    ax2.plot(freq, off)
    ax2.set_title(mode+' off')

    on_off = on - off
    # ax3.set_title('first on minus off')
    # ax3.set_ylim(-1, 1.5)
    ax3.plot(freq, on_off)
    ax3.set_title(mode+' on minus off')

    # ax1.ylabel('first on minus off')

    f.subplots_adjust(hspace=1)

    # plt.xlim(1381.8, 1387.8)
    # axes.set_ylim([ymin,ymax])
    # plt.ylim(4.5, 6)
    plt.savefig(mode+'-on-off')
    plt.show()
    # hdulist = fits.open('data_20171103T215857.fits')

    # plt.plot(hdulist[0].data)
    # plt.show()
    return on_off

# =============== first session on off plot======================#

first_on_data = read_data(os.path.join(obj_path, 'first-on'))
first_off_data = read_data(os.path.join(obj_path, 'first-off'))

first_on = np.mean(bandpass_correction(first_on_data, freq), axis=1)
first_off = np.mean(bandpass_correction(first_off_data, freq), axis=1)

first_on_off = plot_on_off(first_on, first_off, freq, 'first')

# ===============second session on off plot======================#

second_on_data = read_data(os.path.join(obj_path, 'second-on'))
second_off_data = read_data(os.path.join(obj_path, 'second-off'))

second_on = np.mean(bandpass_correction(second_on_data, freq), axis=1)
second_off = np.mean(bandpass_correction(second_off_data, freq), axis=1)

second_on_off = plot_on_off(second_on, second_off, freq, 'second')


# ============= plot ON-OFF data ====================#
first_second_mean = (first_on_off + second_on_off)/2.

print(np.min(first_second_mean), np.argmin(first_second_mean))
print('signal at '+str(1354.3+np.argmin(first_second_mean)/1000.)+' MHz')

# smooth function is from IDL http://www.harrisgeospatial.com/docs/SMOOTH.html
first_second_mean = ndimage.filters.uniform_filter(first_second_mean,
                                                   size=int(smooth_box))

plt.plot(freq, first_second_mean)
plt.annotate('Signal at '+str(1354.3+np.argmin(first_second_mean)/1000.*6)
             + ' MHz',
             xy=(1357.3, 1e-12),
             xytext=(1358.3, 1e-12),
             arrowprops=dict(arrowstyle="->"))

# ax.annotate('signal at '+str(1419.5+np.argmin(first_second_mean)/1000.)
#             +' MHz', xy=(1420.75, 0.5), xytext=(1420.75, 0.5),
#             arrowprops=dict(facecolor='black', shrink=0.05),
#             )

plt.title(obj_name)
plt.savefig('first-second-mean')
plt.show()
