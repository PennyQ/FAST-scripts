from astropy.io import fits
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from scipy import ndimage

# TODO: modulize the pipeline
# run.py - excutive entry
# calculation.py - all scientific calculations
# plot.py - plotting codes

# TODO: In the future, add functionality to automatically seperate \
# first/second on off files

# TODO: In the future, when deal with stacks of data, we should enable \
# output plots in the data folder

# TODO: add bandpass

# TODO: add baseline

# =============Get user input================#
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
smooth_box = raw_input('Please type the smoothing width of the boxcar \
                        average: [10]') or 10
                        
# ===============calculations======================#


def mean_onoff(path, data=None):
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
        print('data shape', data.shape)
        data_mean = np.mean(data, axis=1)
        print('data_mean shape', data_mean.shape)
    except OSError:
        # If the folder path is wrong after three trials
        print("Invalid folder input, please check the folder existance.")
        sys.exit()
    return data_mean  # as a numpy array


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


first_on = mean_onoff(os.path.join(obj_path, 'first-on'))
first_off = mean_onoff(os.path.join(obj_path, 'first-off'))
freq = np.linspace(float(freq[0]), float(freq[1]), tick_num)
first_on_off = plot_on_off(first_on, first_off, freq, 'first')

# ===============second session on off plot======================#

second_on = mean_onoff(os.path.join(obj_path, 'second-on'))
second_off = mean_onoff(os.path.join(obj_path, 'second-off'))
freq = np.linspace(float(freq[0]), float(freq[1]), tick_num)
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
