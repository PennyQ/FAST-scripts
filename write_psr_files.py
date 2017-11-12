'''
Automatically add coordinate and source info to the Pulsar observation record files.
Simply run the script and follow the terminate output.

Author: Penny Qian
Date: 20171112
'''

import os

comfirm = 'n'
while comfirm is not 'y':

    coor = raw_input('Input coor here:')
    source_name = raw_input('Input source name here:')
    init_f_line = 'FASTteam  %s commissioning %s'%(source_name, coor)
    keyfile_f_line = coor

    init_fname = 'data_record_init.txt'
    keyfile_fname = 'data_record_keyfile.txt'

    comfirm = str(raw_input('Comfirm the following lines will be wrote[y/n]: %s'\
                        %'\n'+init_fname+'  ->  '+init_f_line+'\n'+\
                        keyfile_fname+'  ->  '+keyfile_f_line+'\n'))

# append to init file
if os.path.exists(init_fname):
    init_f = open(init_fname,'a')
    init_f.write('\n')
    init_f.write(init_f_line)

# append to keyfile
if os.path.exists(keyfile_fname):
    keyfile_f = open(keyfile_fname, 'a')
    keyfile_f.write('\n')
    keyfile_f.write(keyfile_f_line)
    


# close files
init_f.close()
keyfile_f.close()