from astropy.io import fits
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from scipy import ndimage
from bandpass import bdp_correction
from baselining import baselined


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


# # plot bdp corrected, baselined for each session
def plot_each_session(on, off, freq, mode, bsl_flag=True):
    # initiate the plot
    f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    # read between 2100-2110 as first on

    ax1.plot(freq, on)  # label='first on')
    ax1.set_title(mode+' on')

    # ax1.legend(loc="upper right")

    # read between 2120-2130 as first off
    ax2.plot(freq, off)
    ax2.set_title(mode+' off')

    # TODO: add if baseline option is false
    ax4.set_title(mode+'ON-OFF')
    on_off = on - off
    if bsl_flag:
        bsl_curv, on_off_bsl = baselined(freq, on_off)
        ax3.set_title(mode + 'ON-OFF before baselined')
        ax4.set_title(mode+' ON-OFF after baselined')
    ax3.plot(freq, on_off)
    ax3.plot(freq, bsl_curv, alpha=0.6)
    ax4.plot(freq, on_off_bsl)

    f.subplots_adjust(hspace=1)

    plt.savefig(mode+'_ON-OFF')
    plt.show()

    print('Plot and save ' + mode+' on minus off')
    return on_off


# plot bdp corrected, baselined, and smoothed data
def plot_mean_sessions(freq, sessions_mean, smooth_box,
                       bsl_flag=True, polyfit_deg=1):
    if bsl_flag:
        bsl_curv, sessions_mean_bsl = baselined(freq, sessions_mean, polyfit_deg)
    # smooth function is from IDL http://www.harrisgeospatial.com/docs/SMOOTH.html
    sessions_mean_bsl = ndimage.filters.uniform_filter(sessions_mean_bsl,
                                                   size=int(smooth_box))
    # initiate the plot
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(freq, sessions_mean)
    ax1.plot(freq, bsl_curv, alpha=0.6)
    ax1.set_title('ON-OFF (Smoothed and Before baselined)')

    ax2.plot(freq, sessions_mean_bsl)
    ax2.annotate('Signal at '+str(freq[0]+np.argmin(sessions_mean)/1000.*6)
                 + ' MHz',
                 xy=(freq[0], 1e-12),
                 xytext=(freq[1], 1e-12),
                 arrowprops=dict(arrowstyle="->"))

    ax2.set_title('ON-OFF (Smoothed and Baselined)')
    f.subplots_adjust(hspace=1)
    plt.savefig('bdp-smoothed-bsl')
    plt.show()
