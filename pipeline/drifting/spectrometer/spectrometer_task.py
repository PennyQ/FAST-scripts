import os
from level1 import *
from load_data import *
from plot import *


class SpectrometerTask:

    def __init__(self, obj_name, freq, bsl_flag, smooth_box):
        # param needed for data processing
        self.freq = None
        self.on_data = None
        self.off_data = None
        self.on_off = None
        self.bsl_flag = bsl_flag
        self.smooth_box = smooth_box
        self.ses_on_data = None
        self.ses_off_data = None

        self.obj_name = obj_name
        obj_path = os.path.join(os.path.dirname(os.getcwd()), 'test_data', obj_name)
        fits_path = os.path.join(os.path.dirname(os.getcwd()), 'test_data', obj_name, 'fits')

        time_info = read_time_txt(obj_path)
        print('obj_path', obj_path)
        self.data = read_data(fits_path)
        self.ses_on_data, self.ses_off_data = read_on_off_data_by_time(time_info, obj_path)

        self.freq = np.linspace(float(freq[0]), float(freq[1]), self.ses_on_data.shape[0])

        # TODO: move processing from plot to here, and save the intermediate data
    # def level1_process(self):
    #     # calibration, bandpass, baseline, rfi
    #     bdp_correction(self.data, self.freq)
    #     baselined(self.freq, self.on_off)

    def plot_result(self):
        sessions_mean = np.zeros(self.ses_on_data.shape[0])
        try:
            for i in range(self.ses_on_data.shape[2]):
                print('ses_on_data[..., i]', self.ses_on_data[..., i].shape)
                ses_on_data_bdp = np.mean(bdp_correction(self.ses_on_data[..., i], self.freq), axis=1)
                ses_off_data_bdp = np.mean(bdp_correction(self.ses_off_data[..., i], self.freq), axis=1)
                ses_on_off = plot_each_session(ses_on_data_bdp, ses_off_data_bdp, self.freq,
                                               self.obj_name, self.bsl_flag)
                sessions_mean += ses_on_off

        except IndexError:  # only one session
            i = 0
            print('ses_on_data[..., i]', self.ses_on_data[..., i].shape)
            ses_on_data_bdp = np.mean(bdp_correction(self.ses_on_data[..., i], self.freq), axis=1)
            ses_off_data_bdp = np.mean(bdp_correction(self.ses_off_data[..., i], self.freq), axis=1)
            ses_on_off = plot_each_session(ses_on_data_bdp, ses_off_data_bdp, self.freq, self.obj_name, self.bsl_flag)
            sessions_mean = ses_on_off

        plot_mean_sessions(self.freq, sessions_mean, self.smooth_box, self.bsl_flag)

        print('Pipeline quit!')
