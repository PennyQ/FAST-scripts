import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from level1 import baselined


# TODO: add ON, OFF plot
# TODO: optimize the annotation, also for spectrometer

linecolor = 'black'
linewidth = 1.0
curvecolor = 'orange'
curvewidth = 2.0


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

    ax1.plot(freq, sessions_mean, linewidth=linewidth, color=linecolor)
    ax1.plot(freq, bsl_curv, alpha=0.6, color=curvecolor, linewidth=curvewidth)
    ax1.set_title('ON-OFF (Before Smoothed and Baselined)')
    y1_min = np.mean(sessions_mean) - 1.5 * np.std(sessions_mean)
    y1_max = np.mean(sessions_mean) + 3 * np.std(sessions_mean)
    ax1.set_ylim([y1_min, y1_max])

    print('sessions mean =', np.mean(sessions_mean))

    ax2.plot(freq, sessions_mean_bsl - sessions_mean, linewidth=linewidth, color='grey')
    ax2.set_title('Sample Mask')

    ax3.plot(freq, sessions_mean_bsl, linewidth=linewidth, color=linecolor)
    # print('freq[0] = {}'.format(freq[0]))
    # print('np.argmin(sessions_mean) = {}'.format(np.argmin(sessions_mean)))
    # ax3.annotate('Signal at '+str(freq[0]+np.argmin(sessions_mean)/1000.*6) + ' MHz',
    #              xy=(freq[0], 1e-12),
    #              xytext=(freq[1], 1e-12),
    #              arrowprops=dict(arrowstyle="->"))

    ax3.set_title('ON-OFF (Smoothed and Baselined)')
    y2_min = np.mean(sessions_mean_bsl) - 1.5 * np.std(sessions_mean_bsl)
    y2_max = np.mean(sessions_mean_bsl) + 3 * np.std(sessions_mean_bsl)
    ax3.set_ylim([y2_min, y2_max])
    print('sessions mean bsl =', np.mean(sessions_mean_bsl))

    f.subplots_adjust(hspace=1)
    plt.savefig('output/Crane-bdp-smoothed-bsl', dpi=200)
    plt.show()


def plot_substract(freq, sessions_mean, start_i, end_i):
    """
    Plot subtracted crane data.

    :param freq:
    :param sessions_mean:
    :return:
    """

    ymin = np.mean(sessions_mean) - 1.5 * np.std(sessions_mean)
    ymax = np.mean(sessions_mean) + 3 * np.std(sessions_mean)
    plt.plot(freq, sessions_mean, color=linecolor, linewidth=linewidth)
    axes = plt.gca()
    axes.set_ylim([ymin, ymax])

    plt.axvline(x=start_i, color='red', linewidth=2, alpha=0.7)
    plt.axvline(x=end_i, color='red', linewidth=2, alpha=0.7)
    plt.show()
