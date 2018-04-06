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
        self.data = read_data(fits_path)
        self.ses_on_data, self.ses_off_data = read_on_off_data_by_time(time_info, obj_path)

        self.freq = np.linspace(float(freq[0]), float(freq[1]), self.ses_on_data.shape[0])

    # TODO: save the intermediate data
    def level1_process(self):
        """
        Level processing for loaded data
        :return ON, OFF and mean(ON-OFF) data after bandpass for each record
        """
        sessions_mean = np.zeros(self.ses_on_data.shape[0])
        # if self.get_session_num() == 1:
        #     sessions_mean = np.zeros(self.ses_on_data.shape[0])
        # else:
        #     sessions_mean = np.zeros((self.ses_on_data.shape[0], self.get_session_num()))
        ses_on_data_bdp = None
        ses_off_data_bdp = None
        try:
            for i in range(self.get_session_num()):
                print('ses_on_data[..., i]', self.ses_on_data[..., i].shape)

                if ses_on_data_bdp is None:
                    ses_on_data_bdp = np.mean(bdp_correction(self.ses_on_data[..., i], self.freq), axis=1)
                else:
                    ses_on_data_bdp = np.stack((ses_on_data_bdp,
                                                np.mean(bdp_correction(self.ses_on_data[..., i], self.freq), axis=1)),
                                               axis=-1)

                if ses_off_data_bdp is None:
                    ses_off_data_bdp = np.mean(bdp_correction(self.ses_off_data[..., i], self.freq), axis=1)
                else:
                    ses_off_data_bdp = np.stack((ses_off_data_bdp,
                                                np.mean(bdp_correction(self.ses_off_data[..., i], self.freq), axis=1)),
                                                axis=-1)
                print('sessions_mean += (ses_on_data_bdp - ses_off_data_bdp)', sessions_mean.shape, ses_on_data_bdp.shape,
                      ses_off_data_bdp.shape)

            for i in range(self.get_session_num()):
                sessions_mean += (ses_on_data_bdp[...,i] - ses_off_data_bdp[...,i])
            sessions_mean /= self.get_session_num()

        except IndexError:  # only one session
            i = 0
            print('ses_on_data[..., i]', self.ses_on_data[..., i].shape)
            ses_on_data_bdp = np.mean(bdp_correction(self.ses_on_data[..., i], self.freq), axis=1)
            ses_off_data_bdp = np.mean(bdp_correction(self.ses_off_data[..., i], self.freq), axis=1)
            sessions_mean = (ses_on_data_bdp - ses_off_data_bdp)

        return ses_on_data_bdp, ses_off_data_bdp, sessions_mean

    def plot_result(self, ses_on_data_bdp, ses_off_data_bdp, sessions_mean):
        """
        Level processing for loaded data
        :param ses_on_data_bdp
        :param ses_off_data_bdp
        :param sessions_mean
        """
        if self.get_session_num()==1:
            plot_each_session(ses_on_data_bdp, ses_off_data_bdp, self.freq, self.obj_name, self.bsl_flag)
        else:
            for i in range(self.get_session_num()):
                plot_each_session(ses_on_data_bdp[..., i], ses_off_data_bdp[..., i], self.freq, self.obj_name, self.bsl_flag)

        plot_mean_sessions(self.freq, sessions_mean, self.smooth_box, self.bsl_flag)

        print('Pipeline quit!')

    def get_session_num(self):
        if len(self.ses_on_data.shape) == 2:
            return 1
        else:
            return self.ses_on_data.shape[2]