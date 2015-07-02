#!/usr/local/bin/python

import os
import pprint
import run_class

#############################################################
# Set up cases
#    - This section can be customized to fit the 
#      application in run_cases.py
#    - Create the for loop structure that populates
#      the cases list with the appropriate run dictionaries
#    - Also provide the correct paths for the runs, grids, 
#      and executable
#############################################################


from run_cases import *
      
pprint.pprint(cases)        

#raise SystemExit(0)

########################################################################
# Create run directories and input files
#   - This section shouldn't need to change 
#     (unless the input file format changes or new paramters are added)
#     since all run parameters are specifed in the set-up section
########################################################################

run_dirs = []
for case in cases:
  
  direc = case['direc']
  proc = case['proc']

  # create run directory path
  run_dirs.append(direc)  
  print 'setting up directory: ' + direc  
  
  # make the directory if necessary
  if not os.path.exists(direc):
    os.makedirs(direc)      
  
  #run_case = run_class.Run(case)
  run_case = run_class.TACCRun(case)
  #run_case = run_class.CRCRun(case)  
  
  run_case.input_file()
  run_case.write_file()
  
  run_case.prep_file()
  run_case.write_file()
  
  run_case.run_file()
  run_case.write_file()
              
   
  
#raise SystemExit(0)

#####################################################
# Run cases
#####################################################
  
for direc in run_dirs:  
  
  run_case.submit_prep(direc)
  run_case.submit_run(direc)
