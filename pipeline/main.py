import sys
from drifting.spectrometer.data_process import SpectrometerDataProcessTask
from drifting.crane.data_process import CraneDataProcessTask
from user_input import UserInput


# TODO: test bandpass and baseline, polish the code - wait for Bo's figures

# TODO: rephrase the comments

# TODO: In the future, when deal with stacks of data, we should enable \
# output plots in the data folder

# TODO: all user input should be stored in a config, and read by functions
#       modulize the code structure;

# TODO: fix the annotation of plot

# TODO: poly fit = 2 looks wrong

# TODO: try poly fit with PGC 070403  2017/11/03

# TODO: put output results into output folder and clean the dir

def start_pipeline():
    """
    Main function to start the pipeline.
    :return:
    """
    user_input = UserInput()
    poly_fit = 1  # default as 1

    while(True):
        if user_input.obs_mode == 1 and user_input.instrument == 1:
            spectrometer_task = SpectrometerDataProcessTask(obj_name=user_input.obj_name,
                                                            freq=user_input.freq,
                                                            bsl_flag=user_input.bsl_flag,
                                                            smooth_box=user_input.smooth_box,
                                                            polyfit_deg=poly_fit)

            spectrometer_task.level1_process()
            spectrometer_task.plot_result()

        if user_input.obs_mode == 1 and user_input.instrument == 2:
            crane_task = CraneDataProcessTask(obj_name=user_input.obj_name,
                                              bsl_flag=user_input.bsl_flag,
                                              smooth_box=user_input.smooth_box,
                                              polyfit_deg=poly_fit)

            crane_task.subtract_bandpass()
            crane_task.level1_process()
            crane_task.plot_result()

        poly_fit = user_input.prompt_poly_fit()
        if poly_fit == 0:  # means poly fit degree accepted
            break

    print('Pipeline finished successfully!')


if __name__ == "__main__":
    sys.exit(start_pipeline())
