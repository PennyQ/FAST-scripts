import os
import subprocess
import properties


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

        self.smooth_box = raw_input('Please type the smoothing width of the boxcar' +
                                    'average: [10]') or 10

        self.bsl_flag = True
        if raw_input('Baseline the result? [y/n] default as yes').lower() == 'n':
            self.bsl_flag = False

        # Init data and freq from properties file
        cwd = os.getcwd()
        if self.instrument == 1:
            self.obj_name = properties.SPEC_DATA_OBJECT
        if self.instrument == 2:
            self.obj_name = properties.CRANE_DATA_OBJECT

        obj_path = os.path.join(os.path.dirname(cwd), 'test_data', self.obj_name)
        if not os.path.exists(obj_path):
            print("Not valid object name, check properties.py!")
            exit(0)

        # spectrometer data freq from remote .m file, set in properties
        if self.instrument == 1:
            ssh = subprocess.Popen(['ssh', '-p 33322', properties.REMOTE, 'cat', properties.FREQ_FILE],
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

    @staticmethod
    def prompt_poly_fit():
        poly_fit = raw_input('Fitting result acceptable? (default fitting degree as 1) \n'
                             'If yes, please type 0, otherwise type the new fitting degree num: ')
        if int(poly_fit) > 2:
            if raw_input('Polyfit degree > 2 may decrease the performance, you sure? [yes/no]') == 'no':
                print('Poly fitting degree is 2')
                return 2
        return int(poly_fit)
