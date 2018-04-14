from astropy.io import fits
import sys
from drifting.spectrometer.data_process import DataProcessTask
from user_input import UserInput


# TODO: test bandpass and baseline, polish the code - wait for Bo's figures

# TODO: rephrase the comments

# TODO: In the future, when deal with stacks of data, we should enable \
# output plots in the data folder

# TODO: all user input should be stored in a config, and read by functions
#       modulize the code structure;

# TODO: fix the annotation of plot


def start_pipeline():
    """
    Main function to start the pipeline.
    :return:
    """
    user_input = UserInput()
    if user_input.obs_mode == 1 and user_input.instrument == 1:
        spectrometer_task = DataProcessTask(obj_name=user_input.obj_name,
                                            freq=user_input.freq,
                                            bsl_flag=user_input.bsl_flag,
                                            smooth_box=user_input.smooth_box)

        spectrometer_task.level1_process()
        spectrometer_task.plot_result()
    else:
        print('Mode not supported yet, pipeline quit!')


if __name__ == "__main__":
    sys.exit(start_pipeline())
