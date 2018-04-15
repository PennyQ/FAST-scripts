import os
import sys

import numpy as np
from astropy.io import fits


class CraneData:

    """
    The data container for crane data.
    """
    def __init__(self, obj_path):
        self.ses_on_data, self.ses_off_data = self.read_on_off_data(obj_path)
        self.freq = self.get_freq(obj_path)

    @staticmethod
    def get_freq(obj_path):
        try:
            for each_rec in os.listdir(os.path.join(obj_path, '2018-01-28_15-03-24_PegII-UDG23_on_tracking')):
                # read on data into an array and return
                each_rec_path = os.path.join(obj_path, '2018-01-28_15-03-24_PegII-UDG23_on_tracking', each_rec)
                if os.path.isfile(each_rec_path) and '.fit' in os.path.basename(each_rec_path):
                    hdu_list = fits.open(each_rec_path)
                    hdu_data = hdu_list[1].data
                    freq = hdu_data['SUBFREQ']  # shape(127,4)
                    freq1 = freq[:, 0]  # center frequency of first frequency range
                    n_channel = 65536
                    n_rec = 127

                    delt = hdu_data['CDELT1']
                    start = freq1 - delt / 2.
                    stop = freq1 + delt / 2.
                    # print('start, stop', start.shape, stop)

                    freq1 = np.linspace(start[0], stop[0], n_channel)
                    break

        except OSError:
            print("Invalid folder input, please check the folder existance.")
            sys.exit()
        return freq1

    @staticmethod
    def read_on_off_data(obj_path):
        on_data_mean = None
        off_data_mean = None
        n_on_rec = 0.0
        n_off_rec = 0.0
        try:
            for each_rec in os.listdir(os.path.join(obj_path, '2018-01-28_15-03-24_PegII-UDG23_on_tracking')):
                # read on data into an array and return
                each_rec_path = os.path.join(obj_path, '2018-01-28_15-03-24_PegII-UDG23_on_tracking', each_rec)
                print('each_rec_path is {}'.format(each_rec_path))
                if os.path.isfile(each_rec_path) and '.fit' in os.path.basename(each_rec_path):
                    hdu_list = fits.open(each_rec_path)
                    hdu_data = hdu_list[1].data
                    data = hdu_data['DATA'].T
                    print('data from open is {}'.format(data))
                    each_rec_data_mean = np.mean(data[:, 0, 0, 0, 0, :], axis=1)
                    if on_data_mean is None:
                        on_data_mean = each_rec_data_mean
                    else:
                        on_data_mean += each_rec_data_mean
                    n_on_rec += 1.0
            on_data_mean = on_data_mean/n_on_rec   # shape 65536

            for each_rec in os.listdir(os.path.join(obj_path, '2018-01-28_15-31-37_PegII-UDG23_off_tracking')):
                # read on data into an array and return
                each_rec_path = os.path.join(obj_path, '2018-01-28_15-31-37_PegII-UDG23_off_tracking', each_rec)
                print('each_rec_path is {}'.format(each_rec_path))
                if os.path.isfile(each_rec_path) and '.fit' in os.path.basename(each_rec_path):
                    hdu_list = fits.open(each_rec_path)
                    hdu_data = hdu_list[1].data
                    data = hdu_data['DATA'].T
                    each_rec_data_mean = np.mean(data[:, 0, 0, 0, 0, :], axis=1)
                    if off_data_mean is None:
                        off_data_mean = each_rec_data_mean
                    else:
                        off_data_mean += each_rec_data_mean
                    n_off_rec += 1.0
            off_data_mean = off_data_mean/n_off_rec

        except OSError:
            print("Invalid folder input, please check the folder existance.")
            sys.exit()
        return on_data_mean, off_data_mean
