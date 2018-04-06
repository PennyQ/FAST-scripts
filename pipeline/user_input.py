import os


class UserInput:
    def __init__(self):
        self.obs_mode = None
        self.instrument = None
        self.obj_name = None
        self.freq = None
        self.smooth_box = None
        self.bsl_flag = None
        self.get_user_input()

    def get_user_input(self):

        # TODO: depends on the mode chosen, entry to different obs mode
        try:
            self.obs_mode = int(raw_input('Please choose your observation mode \n [1 - Drifting 2 - Tracking]'))
        except TypeError:
            print('Selection out of options range! Please choose 1 or 2.')

        self.instrument = int(raw_input('Please choose your instrument option \n [1 - Spectrometer 2 - Crane]'))

        cwd = os.getcwd()
        self.obj_name = str(raw_input('Please type the folder name: '))
        obj_path = os.path.join(os.path.dirname(cwd), 'test_data', self.obj_name)

        # Allow three times of input trials
        for i in range(3):
            if not os.path.exists(obj_path):
                print('not path')
                self.obj_name = str(raw_input('Path - %s - does not exist \n '
                                              'Please retype : ' % obj_path))
                obj_path = os.path.join(os.path.dirname(cwd), 'test_data', self.obj_name)

        self.freq = raw_input("enter freqency range (separated by a comma):").split(',')

        # tick_num = raw_input("Please enter tick number [1001]:") or 1001

        self.smooth_box = raw_input('Please type the smoothing width of the boxcar' +
                                    'average: [10]') or 10

        self.bsl_flag = True
        if raw_input('Baseline the result? [y/n] default as yes').lower() == 'n':
            self.bsl_flag = False
