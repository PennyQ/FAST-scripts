import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from level1 import baselined

linecolor = 'black'
linewidth = 1.0
curvecolor = 'orange'
curvewidth = 2.0


def plot_each_session(on, off, freq, mode, bsl_flag=True, polyfit_deg=1):
    """
    Plot bdp corrected, baseline result for each session.

    :param on: On data of each session.
    :param off: Off data of each session.
    :param freq: Frequency range.
    :param mode: Which session mode.
    :param bsl_flag: Flag to mark baseline or not.
    :return:
    """
    # initiate the plot
    f, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True)

    ax1.plot(freq, on, color=linecolor, linewidth=linewidth)
    ax1.set_title(mode+' on')

    # ax1.legend(loc="upper right")

    ax2.plot(freq, off, color=linecolor, linewidth=linewidth)
    ax2.set_title(mode+' off')

    # TODO: add if baseline option is false
    ax4.set_title(mode+'ON-OFF')
    on_off = on - off
    if bsl_flag:
        bsl_curv, on_off_bsl = baselined(freq, on_off, polyfit_deg)
        ax3.set_title(mode + ' ON-OFF before baselined')
        ax4.set_title(mode+' ON-OFF after baselined')
    ax3.plot(freq, on_off, color=linecolor, linewidth=linewidth)
    ax3.plot(freq, bsl_curv, alpha=0.6, color=curvecolor, linewidth=curvewidth)
    ax4.plot(freq, on_off_bsl, color=linecolor, linewidth=linewidth)

    f.subplots_adjust(hspace=1)

    plt.savefig('output/Crane_'+mode+'_ON-OFF')
    plt.show()

    print('Plot and save {} ON minus OFF'.format(mode))


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

    ax2.plot(freq, sessions_mean_bsl - sessions_mean, linewidth=linewidth, color='grey')
    ax2.set_title('Sample Mask')

    ax3.plot(freq, sessions_mean_bsl, linewidth=linewidth, color=linecolor)
    ax3.annotate('Signal at '+str(freq[0]+np.argmin(sessions_mean)/1000.*6)
                 + ' MHz',
                 xy=(freq[0], 1e-12),
                 xytext=(freq[1], 1e-12),
                 arrowprops=dict(arrowstyle="->"))

    ax3.set_title('ON-OFF (Smoothed and Baselined)')
    f.subplots_adjust(hspace=1)
    plt.savefig('output/Crane-bdp-smoothed-bsl', dpi=200)
    plt.show()
