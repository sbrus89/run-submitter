#!/usr/local/bin/python

import os
import sys
import pprint
import getopt
import socket
import run_class
import run_check
import subprocess
import time

try:
  opts,args = getopt.getopt(sys.argv[1:],"dw",["dry","write","chl","crc","tacc","no-prep","queue"])
except getopt.GetoptError:
  print "Incorrect command line arguments"
  raise SystemExit(0)

dry_run = False
write_only = False
prep = True
queue = False

hostname = socket.gethostname()
hostname_sp = hostname.split(".")
if len(hostname_sp) > 1:
  host = ".".join(hostname_sp[1:])
else:
  host = hostname

for opt,arg in opts:  
  if opt in ["-d","--dry"]:
    dry_run = True
  elif opt in ["-w","--write"]:
    write_only = True
  elif opt == "--chl":
    host = "chl-tilos"
  elif opt == "--crc":
    host = "crc.nd.edu"
  elif opt == "--tacc":
    host = "stampede.tacc.utexas.edu"
  elif opt == "--no-prep":
    prep = False
  elif opt == "--queue":
    queue = True
  
  


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

run_check.check_cases(cases)
      
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
    
    if host == 'chl-tilos':
      run_case = run_class.Run()
    elif host == 'stampede.tacc.utexas.edu':
      run_case = run_class.TACCRun()
    elif host == 'crc.nd.edu':
      run_case = run_class.CRCRun() 
    
    bundle[proc] = run_case
    
  else:
    
    run_case = bundle[proc]
    
    
  run_case.input_file(case) # Create and write input file
  run_case.prep_file(case)  # Create/build prep file 
  run_case.run_file(case)   # Create/build run file
  
for run_case in bundle.itervalues():
  
  run_case.write_file(run_case.prep_name,run_case.prep_content)  
  run_case.write_file(run_case.run_name, run_case.run_content)
                 
  
if write_only == True:  
  raise SystemExit(0)

#####################################################
# Run cases
#####################################################

ncases = len(bundle)
nsub = 0
delay = 60

if queue:

  while 1:
  
#    user = 'zcobell' 
    user = 'sbrus'
    qstat_cmd = ['qstat','-u',user]
    output = subprocess.Popen(qstat_cmd, stdout=subprocess.PIPE).communicate()[0]
    user_jobs = [x.split() for x in output.splitlines()[2:]]
    pprint.pprint(user_jobs)

    total_cores = 0 
    for job in user_jobs:
      cores = int(job[-1])
      total_cores = total_cores + cores

    if total_cores <= max_proc:
      proj_cores = total_cores

      for run_case in bundle.itervalues():
        if run_case.sub_run == False:
          proj_cores = proj_cores + int(run_case.cores)

          if proj_cores <= max_proc: 
            if prep:
              run_case.submit_prep()
            run_case.submit_run()
            nsub = nsub + 1
            print "nsub = ", nsub

    if nsub == ncases:
      break

    time.sleep(delay)

else:      

  for run_case in bundle.itervalues():  

    print run_case.cores
    if prep:
      run_case.submit_prep()  
    run_case.submit_run()  
