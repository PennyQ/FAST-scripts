"""
This file is to store user input as a config file.

Loading data from remote server is still underdevelopment. Currently, the frequency information for
spectrometer can be read from remote file, the file location is set by FREQ_FILE.
"""

SPEC_DATA_OBJECT = '20171105_UGC00613_HI_hql'

CRANE_DATA_OBJECT = '2018-01-28_15-03-24_PegII-UDG23'

# ===REMOTE ===

# change to your user name to the FAST remote server and be sure the connection is built
REMOTE = 'xrqian@220.172.166.33'

FREQ_FILE = '/public/home/pub/obs/spectrometer_data/2017.11/20171105_UGC00613_HI_hql/b51_get_spec_HI_RF.m'
# FREQ_FILE = '/public/home/pub/obs/spectrometer_data/2017.11/20171103_HI_PGC070403_tracking_mcc/b51_get_spec_HI_RF.m'

# ====Plot=====
COLOR = 'black'
ALPHA = 0.6