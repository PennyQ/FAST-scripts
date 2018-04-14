import numpy as np
from astropy.io import fits

class CraneData:
    def __init__(self):
        pass

# 第一维长度65536，表示每个频段有65536个光谱通道
# 第二维是频段，最多同时记录4个频段，所以大小为4，但现在观测往往不会记录这么多频段，所以很可能某几组数据是一样的
# 第三维是Stokes参量，看偏振用的，也是大小为4

crane_file = 'spctrum__2018-01-28T07-03-36.fits'
hdu_list = fits.open(crane_file)
hdu_list.info()
print(hdu_list[1].columns)

hdu_data = hdu_list[1].data
data = hdu_data['DATA'].T

n_channel = 65536 #channel number
n_rec = 127 #total records number in each file

data_on1 = np.array((n_channel, n_rec))
data_on1 = data[:, 0, 0, 0, 0, :]