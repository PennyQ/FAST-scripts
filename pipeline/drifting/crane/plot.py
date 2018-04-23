import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from level1 import baselined


# TODO: add ON, OFF plot
# TODO: optimize the annotation, also for spectrometer

def plot_mean_sessions(freq, sessions_mean, smooth_box, bsl_flag=True, polyfit_deg=1):
    """
    Plot bdp corrected, baselined, and smoothed data

    :param freq:
    :param sessions_mean:
    :param smooth_box:
    :param bsl_flag:
    :param polyfit_deg:
    :return:
    """
    if bsl_flag:
        bsl_curv, sessions_mean_bsl = baselined(freq, sessions_mean, polyfit_deg)
    # smooth function is from IDL http://www.harrisgeospatial.com/docs/SMOOTH.html
    sessions_mean_bsl = ndimage.filters.uniform_filter(sessions_mean_bsl,
                                                       size=int(smooth_box))

    # initiate the plot
    f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

    ax1.plot(freq, sessions_mean)
    ax1.plot(freq, bsl_curv, alpha=0.6)
    ax1.set_title('ON-OFF (Before Smoothed and Baselined)')

    ax2.plot(freq, bsl_curv - sessions_mean, linewidth=1.0, color='grey')
    ax2.set_title('Sample Mask')

    ax3.plot(freq, sessions_mean_bsl)
    # print('freq[0] = {}'.format(freq[0]))
    # print('np.argmin(sessions_mean) = {}'.format(np.argmin(sessions_mean)))
    # ax3.annotate('Signal at '+str(freq[0]+np.argmin(sessions_mean)/1000.*6) + ' MHz',
    #              xy=(freq[0], 1e-12),
    #              xytext=(freq[1], 1e-12),
    #              arrowprops=dict(arrowstyle="->"))

    ax3.set_title('ON-OFF (Smoothed and Baselined)')
    f.subplots_adjust(hspace=1)
    plt.savefig('bdp-smoothed-bsl', dpi=200)
    plt.show()
