import os
from level1 import *
from load_data import SpectrometerData
from plot import *


class SpectrometerDataProcessTask:

    """
    This class is the frame to use different modules and process data.
    Detailed functions (such as loading data, plot and processing) are not included in this class.
    """

    def __init__(self, obj_name, freq, bsl_flag, smooth_box):
        """
        Parameters and methods needed for data processing.

        :param obj_name:
        :param freq:
        :param bsl_flag:
        :param smooth_box:
        """
        self.bsl_flag = bsl_flag
        self.smooth_box = smooth_box

        self.obj_name = obj_name
        obj_path = os.path.join(os.path.dirname(os.getcwd()), 'test_data', obj_name)
        fits_path = os.path.join(os.path.dirname(os.getcwd()), 'test_data', obj_name, 'fits')

        spec_data = SpectrometerData(obj_path, fits_path)
        self.data = spec_data.data
        self.ses_on_data = spec_data.ses_on_data  # [n_channel, n_record, *n_sec]
        self.ses_off_data = spec_data.ses_off_data

        self.n_channel = self.ses_on_data.shape[0]

        self.freq = np.linspace(float(freq[0]), float(freq[1]), self.n_channel)

        self.ses_on_data_bdp = None
        self.ses_off_data_bdp = None
        self.sessions_mean = None

    # TODO: save the intermediate data
    def level1_process(self):
        """
        Level I processing for loaded data
        :return ON, OFF and mean(ON-OFF) data after bandpass for each record
        """
        sessions_mean = np.zeros(self.n_channel)

        ses_on_data_bdp = None
        ses_off_data_bdp = None

        # For each session, load ON and OFF data
        for i in range(self.get_session_num()):
            each_ses_on_bdp = bdp_correction(self.ses_on_data[..., i], self.freq)
            each_ses_off_bdp = bdp_correction(self.ses_off_data[..., i], self.freq)

            if ses_on_data_bdp is None:
                ses_on_data_bdp = np.mean(each_ses_on_bdp, axis=1)
            else:
                ses_on_data_bdp = np.stack((ses_on_data_bdp,
                                            np.mean(each_ses_on_bdp, axis=1)), axis=-1)

            if ses_off_data_bdp is None:
                ses_off_data_bdp = np.mean(each_ses_off_bdp, axis=1)

            else:
                ses_off_data_bdp = np.stack((ses_off_data_bdp,
                                            np.mean(each_ses_off_bdp, axis=1)),
                                            axis=-1)

        # array shape different for one session and multiple sessions
        if self.get_session_num() == 1:
            sessions_mean = (ses_on_data_bdp - ses_off_data_bdp)
        else:
            for i in range(self.get_session_num()):
                sessions_mean += (ses_on_data_bdp[..., i] - ses_off_data_bdp[..., i])

            sessions_mean /= self.get_session_num()

        self.ses_on_data_bdp = ses_on_data_bdp
        self.ses_off_data_bdp = ses_off_data_bdp
        self.sessions_mean = sessions_mean

    def plot_result(self):
        """
        Level processing for loaded data
        """
        if self.get_session_num() == 1:
            plot_each_session(self.ses_on_data_bdp, self.ses_off_data_bdp, self.freq, self.obj_name, self.bsl_flag)
        else:
            for i in range(self.get_session_num()):
                plot_each_session(self.ses_on_data_bdp[..., i], self.ses_off_data_bdp[..., i],
                                  self.freq, self.obj_name, self.bsl_flag)
        plot_mean_sessions(self.freq, self.sessions_mean, self.smooth_box, self.bsl_flag)

        print('Pipeline quit!')

    def get_session_num(self):
        """
        :return: session number from data shape [n_channel, n_record, *n_sec]
        """
        if len(self.ses_on_data.shape) == 2:
            return 1
        else:
            return self.ses_on_data.shape[2]
