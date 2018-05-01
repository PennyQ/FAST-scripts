import os
import subprocess
import remote_properties


class UserInput:
    def __init__(self):
        self.obs_mode = None
        self.instrument = None
        self.obj_name = None
        self.smooth_box = None
        self.bsl_flag = None
        self.freq = None
        self.user_init_input()

    def user_init_input(self):

        # Get user input for obs mode and other interactive
        try:
            self.obs_mode = int(raw_input('Please choose your observation mode \n [1 - Drifting 2 - Tracking]'))
        except TypeError:
            print('Selection out of options range! Please choose 1 or 2.')

        self.instrument = int(raw_input('Please choose your instrument option \n [1 - Spectrometer 2 - Crane]'))

        # Choose load data from local or remote
        local_or_remote = raw_input('Load data from local or remote? [l/r]')
        cwd = os.getcwd()

        if local_or_remote == 'l':
            # local
            self.obj_name = raw_input('Please type folder name: ')
            obj_path = os.path.join(os.path.dirname(cwd), 'test_data', self.obj_name)
            if not os.path.exists(obj_path):
                print("Not valid object name, check remote_properties.py!")
                exit(0)
            # Get spectrometer data freq from remote .m file, set in properties
            if self.instrument == 1:
                ssh = open(os.path.join(os.path.dirname(cwd), 'test_data', self.obj_name, 'b51_get_spec_HI_RF.m'), 'r')
                for line in ssh.readlines():
                    if 'fa =' in line:
                        fa = line.split()  # do stuff
                    if 'fb =' in line:
                        fb = line.split()
                    if 'npt =' in line:
                        npt = line.split()
                self.freq = [fa[2][:-1], fb[2][:-1]]
                # tick_num = npt[2][:-1]
                print('self.freq is', self.freq)

        if local_or_remote == 'r':
            # TODO: change this part to fully get data from remote
            # Get data object name from properties setting and check whether the file exists locally
            if self.instrument == 1:
                self.obj_name = remote_properties.SPEC_DATA_OBJECT
            if self.instrument == 2:
                self.obj_name = remote_properties.CRANE_DATA_OBJECT

            obj_path = os.path.join(os.path.dirname(cwd), 'test_data', self.obj_name)
            if not os.path.exists(obj_path):
                print("Not valid object name, check remote_properties.py!")
                exit(0)

            # Get spectrometer data freq from remote .m file, set in properties
            if self.instrument == 1:
                ssh = subprocess.Popen(
                    ['ssh', '-p 33322', remote_properties.REMOTE, 'cat', remote_properties.FREQ_FILE],
                    stdout=subprocess.PIPE)
                for line in ssh.stdout:
                    if 'fa =' in line:
                        fa = line.split()  # do stuff
                    if 'fb =' in line:
                        fb = line.split()
                    if 'npt =' in line:
                        npt = line.split()
                self.freq = [fa[2][:-1], fb[2][:-1]]
                # tick_num = npt[2][:-1]
                print('self.freq is', self.freq)

        # Smooth box width for final result
        self.smooth_box = raw_input('Please type the smoothing width of the boxcar' +
                                    'average: [10]') or 10

        # Baseline or not
        self.bsl_flag = True
        if raw_input('Baseline the result? [y/n] default as yes').lower() == 'n':
            self.bsl_flag = False

    @staticmethod
    def prompt_poly_fit():
        poly_fit = raw_input('Fitting result acceptable? (default fitting degree as 1) \n'
                             'If yes, please type 0, otherwise type the new fitting degree num: ')
        if int(poly_fit) > 2:
            if raw_input('Polyfit degree > 2 may decrease the performance, you sure? [yes/no]') == 'no':
                print('Poly fitting degree is 2')
                return 2
        return int(poly_fit)
