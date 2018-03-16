from astropy.io import fits
import matplotlib.pyplot as plt
import os, sys
import numpy as np

# TODO: modulize the pipeline
# run.py - excutive entry
# calculation.py - all scientific calculations
# plot.py - plotting codes

### =============Get user input================###
cwd = os.getcwd()
dirname = os.path.dirname(cwd)
print('cwd', cwd)
print('cwd dirname', os.path.dirname(cwd))
print('join2', os.path.join(dirname, 'test_data/20171105_UGC00613_HI_hql/first-on'))
obj_name = str(raw_input('Please type the folder name: '))
obj_path = os.path.join(os.path.dirname(cwd), 'test_data', obj_name)

# allow three times of wrong input for the object name
for i in range(3):
    if not os.path.exists(obj_path):
        print('not path')
        obj_name = str(raw_input('Path - %s - does not exist \n Please retype : '%obj_path))
        obj_path = os.path.join(os.path.dirname(cwd), 'test_data', obj_name)

# if raw_input('First or Second scan [F/S]').lower() == 'f':
#     cal_mode = 'F'
# if raw_input('First or Second scan [F/S]').lower() == 'S':
#     cal_mode = 'S'

### ===============calculations======================###
def mean_onoff(path, data=None):
    try:
        for dir_entry in os.listdir(path):
          dir_entry_path = os.path.join(path, dir_entry)
          if os.path.isfile(dir_entry_path) and 'fit' in dir_entry_path:
            hdulist = fits.open(dir_entry_path)

            # unit of dB tranfering a into linear space
            data_linear  = np.power(10.0, hdulist[0].data/10.0)

            if data is None:
                data = data_linear
            else:
                data=np.append(data, data_linear, axis=1)
        print('data shape',data.shape)
        data_mean=np.mean(data, axis=1)
        print('data_mean shape',data_mean.shape)
    except OSError:
        # If folder path is wrong after three trials
        print("Invalid folder input, please check the folder existance.")
        sys.exit()
    return data_mean #as a numpy array


first_on = mean_onoff(os.path.join(obj_path, 'first-on'))

f,(ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)

# fa=1381.8; fb =  1387.8
freq = np.linspace(1354.3, 1360.3, 1001)

# read between 2100-2110 as first on


ax1.plot(freq, first_on)#, label='first on')
ax1.set_title('first on')

# ax1.legend(loc="upper right")

### ===============first on off plot======================###
# read between 2120-2130 as first off
first_off = mean_onoff(os.path.join(os.path.dirname(cwd), 'test_data', obj_name, 'first-off'))
ax2.plot(freq, first_off)
ax2.set_title('first off')

first_on_off = first_on - first_off
# ax3.set_title('first on minus off')
# ax3.set_ylim(-1, 1.5)
ax3.plot(freq, first_on_off)
ax3.set_title('first on minus off')

#ax1.ylabel('first on minus off')

f.subplots_adjust(hspace=1)

#plt.xlim(1381.8, 1387.8)
# axes.set_ylim([ymin,ymax])
# plt.ylim(4.5, 6)
plt.savefig('first-on-off')
plt.show()
# hdulist = fits.open('data_20171103T215857.fits')

# plt.plot(hdulist[0].data)
# plt.show()

# ### ===============second on off plot======================###
# f,(ax4, ax5, ax6) = plt.subplots(3, 1, sharex=True)
# # read between 2140-2150 as second on
# second_on = mean_onoff('../second-on')
# ax4.plot(freq, second_on)
# ax4.set_title('second on')
#
# # read between 2200-2210 as second off
# second_off = mean_onoff('../second-off')
# ax5.plot(freq, second_off)
# ax5.set_title('second off')
#
# second_on_off = second_on - second_off
# # ax4.set_title('second on minus off')
# ax6.plot(freq, second_on_off)
# ax6.set_title('second on minus off')
#
# f.subplots_adjust(hspace=1)
# plt.savefig('second-on-off')
# plt.show()
#
# ### =============first second mean calculation and plot====================###
# first_second_mean = (first_on_off + second_on_off)/2.
# print(np.min(first_second_mean),np.argmin(first_second_mean))
# print('signal at '+str(1354.3+np.argmin(first_second_mean)/1000.)+' MHz')
#
# plt.plot(freq, first_second_mean)
#
# plt.annotate('Signal at '+str(1354.3+np.argmin(first_second_mean)/1000.*6)+' MHz',
#              xy=(1357.3, 1e-12),
#              xytext=(1358.3, 1e-12),
#              arrowprops=dict(arrowstyle="->"))
#
# # ax.annotate('signal at '+str(1419.5+np.argmin(first_second_mean)/1000.)+' MHz', xy=(1420.75, 0.5), xytext=(1420.75, 0.5),
# #             arrowprops=dict(facecolor='black', shrink=0.05),
# #             )
#
# plt.title('UGC00613 FAST 2017/11/5')
# plt.savefig('first-second-mean')
# plt.show()
