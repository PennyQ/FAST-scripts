import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from level1 import baselined

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
    plt.savefig('output/'+obj_name+'-on-off', dpi=300)
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
    print('Plot and save ON-OFF (Baselined and Smoothed)')

    plt.title('ON-OFF (Baselined)')
    plt.savefig('output/bdp-smoothed-bsl', dpi=300)
    plt.show()