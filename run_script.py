#!/usr/local/bin/python

import os
import sys
import pprint
import getopt
import run_class

try:
  opts,args = getopt.getopt(sys.argv[1:],"dw",["dry","write"])
except getopt.GetoptError:
  print "Incorrect command line arguments"
  raise SystemExit(0)

dry_run = False
write_only = False

for opt,arg in opts:  
  if opt in ["-d","--dry"]:
    dry_run = True
  elif opt in ["-w","--write"]:
    write_only = True
    
  

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

if dry_run == True:
  raise SystemExit(0)

########################################################################
# Create run directories and input files
#   - This section shouldn't need to change 
#     (unless the input file format changes or new paramters are added)
#     since all run parameters are specifed in the set-up section
########################################################################

run_cases = []
bundle = {}
n = 0
for case in cases:
  
  direc = case['direc']
  proc = case['proc']
  
  if bundle_flag:
    proc = case['proc']
  else:
    n = n + 1
    proc = str(n)

  # create run directory path
  print 'setting up directory: ' + direc  
  
  # make the directory if necessary
  if not os.path.exists(direc):
    os.makedirs(direc)      
  
  if proc not in bundle:
    
    #run_case = run_class.Run()
    run_case = run_class.TACCRun()
    #run_case = run_class.CRCRun() 
    
    bundle[proc] = run_case
    
  else:
    
    run_case = bundle[proc]
    
    
  run_case.input_file(case)
  run_case.write_file('input')
  
  run_case.prep_file(case)
  
  run_case.run_file(case)
  
for run_case in bundle.itervalues():
  
  run_case.write_file('prep')  
  run_case.write_file('run')
                 
  
if write_only == True:  
  raise SystemExit(0)

#####################################################
# Run cases
#####################################################
  
  
for run_case in bundle.itervalues():  

  run_case.submit_prep()
  run_case.submit_run()  
