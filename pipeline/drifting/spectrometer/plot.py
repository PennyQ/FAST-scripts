import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from level1 import baselined


# # plot bdp corrected, baselined for each session
def plot_each_session(on, off, freq, mode, bsl_flag=True):
    """
    :return: ON-OFF of each session, in numpy.array type.
    """
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


# plot bdp corrected, baselined, and smoothed data
def plot_mean_sessions(freq, sessions_mean, smooth_box, bsl_flag=True, polyfit_deg=1):
    if bsl_flag:
        bsl_curv, sessions_mean_bsl = baselined(freq, sessions_mean, polyfit_deg)
    # smooth function is from IDL http://www.harrisgeospatial.com/docs/SMOOTH.html
    sessions_mean_bsl = ndimage.filters.uniform_filter(sessions_mean_bsl,
                                                       size=int(smooth_box))
    # initiate the plot
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    ax1.plot(freq, sessions_mean)
    ax1.plot(freq, bsl_curv, alpha=0.6)
    ax1.set_title('ON-OFF (Before Smoothed and Baselined)')

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