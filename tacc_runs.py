
#!/usr/local/bin/python

import os
import shutil
import subprocess

sub_prep = 1
do_post = 0

prep_job = 'prep_inlet3_p3'
run_job = 'inlet3_p3'

prep_quene = 'serial'
run_quene = 'normal'

prep_time = '00:30:00'
run_time = ['02:00:00','01:00:00','00:30:00','00:30:00','00:30:00','00:30:00','00:30:00']
#run_time = ['00:45:00','01:30:00','03:00:00','06:00:00','12:00:00','24:00:00' ]

prep_name = 'adcprep'
run_name = 'dgswe'
post_name = 'dgpost_nc'
input_name = 'dgswe.inp'

#prep_name = 'adcprep'
#run_name = 'padcirc'
#post_name = 'adcpost'

code_path = '/home1/01964/sbrus/dgswe/work/'
input_path = '/home1/01964/sbrus/dgswe/work/'

#code_path = '/home1/01964/sbrus/dg-adcirc/work/'
#input_path = '/work/01964/sbrus/dgadcirc_runs/'

path = '/work/01964/sbrus/dgswe_runs/inlet3/'
#path = '/work/01964/sbrus/dgadcirc_runs/inlet6p2/'

allocation = 'TG-DMS080016N'
procs = [16, 32, 64, 128, 256, 512, 1024]
#procs = [256, 512, 1024, 2048, 3200, 4000]

np = len(procs)

if np != len(run_time):
  print 'The processor and run time list are not the same length'
  raise SystemExit(0)

for pe in range(0,np):
  
  proc = str(procs[pe]) # process number as a string
  dirname = 'np'+proc+'/' # name of run directory
  direc = path + dirname # run directory path
  
  print 'setting up directory: ' + direc  
  
  # make the directory if necessary
  if not os.path.exists(direc):
    os.makedirs(direc)  
    
  if run_name == 'padcirc':  
    # write the prep.in file    
    fname = direc + 'prep.in'
    f = open(fname,'w')
    f.write(proc+'\n')
    f.write('prep\n')
    f.write('fort.14\n')
    f.write('fort.15\n')
    f.write('skip')
    f.close()    
    
    #write the post.in file
    fname = direc + 'post.in'
    f = open(fname,'w')
    f.write('post\n')    
    f.write('N\n') 
    f.write('quit\n')     
  else:
    # write the prep.in file    
    fname = direc + 'prep.in'
    f = open(fname,'w')
    f.write(proc)
    f.close()
    
  # write the prep submission script  
  fname = direc + prep_name + '.sub'
  f = open(fname,'w')
  f.write('#!/bin/bash\n')
  f.write('#SBATCH -J ' + prep_job + proc + '           # job name\n')
  f.write('#SBATCH -o ' + prep_job + '.o%j       # output and error file name (%j expands to jobID)\n')
  f.write('#SBATCH -p ' + prep_quene + '         # queue (partition) -- normal, development, etc.\n')
  f.write('#SBATCH -t ' + prep_time + '          # run time (hh:mm:ss)\n')
  f.write('#SBATCH --mail-user=sbrus@nd.edu\n')
  f.write('#SBATCH --mail-type=begin             # email me when the job starts\n')  
  f.write('#SBATCH --mail-type=end               # email me when the job finishes\n')
  f.write('#SBATCH -n 1                          # total number of mpi tasks requested\n')  
  f.write('#SBATCH -A ' + allocation + '\n')
  f.write('\n') 
  f.write("sed -i '1 c " + proc + "' prep.in\n")
  f.write('./' + prep_name + ' < prep.in\n')
  f.write('\n')  
  f.close( )
  
  # write the run submission script
  fname = direc + run_name +'.sub'
  f = open(fname,'w')
  f.write('#!/bin/bash\n')
  f.write('#SBATCH -J ' + run_job + proc + '           # job name\n')
  f.write('#SBATCH -o ' + run_job + '.o%j       # output and error file name (%j expands to jobID)\n')
  f.write('#SBATCH -p ' + run_quene + '         # queue (partition) -- normal, development, etc.\n')
  f.write('#SBATCH -t ' + run_time[pe] + '          # run time (hh:mm:ss)\n')
  f.write('#SBATCH --mail-user=sbrus@nd.edu\n')
  f.write('#SBATCH --mail-type=begin             # email me when the job starts\n')  
  f.write('#SBATCH --mail-type=end               # email me when the job finishes\n')
  f.write('#SBATCH -n ' + proc + '               # total number of mpi tasks requested\n')  
  f.write('#SBATCH -A ' + allocation + '\n')
  f.write('\n') 
  f.write('module load netcdf\n')
  f.write('ibrun -np ' + proc + ' ./' + run_name + '\n')
  if do_post == 1:
    if run_name == 'padcirc':
      f.write('./' + post_name + ' < post.in\n')    
    else:
      f.write('./' + post_name + '\n')
  f.write('\n')    
  f.close( )
  
  # copy the prep executable 
  if sub_prep == 1:
   prep_src = code_path + prep_name
   prep_dst = direc + prep_name
   shutil.copy(prep_src,prep_dst)
   
  # copy the run executable
  run_src = code_path + run_name
  run_dst = direc + run_name
  shutil.copy(run_src,run_dst)
  
  # copy the post executable
  if do_post == 1:
    post_src = code_path + post_name
    post_dst = direc + post_name
    shutil.copy(post_src,post_dst)
  
  if run_name == 'padcirc':
    #copy the fort.14 file
    input_src = input_path + 'fort.14'
    input_dst = direc + 'fort.14'
    shutil.copy(input_src,input_dst)    
    
    #copy the fort.15 file
    input_src = input_path + 'fort.15'
    input_dst = direc + 'fort.15'
    shutil.copy(input_src,input_dst)    
    
    #copy the fort.dg file
    input_src = input_path + 'fort.dg'
    input_dst = direc + 'fort.dg'
    shutil.copy(input_src,input_dst)     
  else:  
    #copy the input file
    input_src = input_path + input_name
    input_dst = direc + input_name
    shutil.copy(input_src,input_dst)
  
  
  
  
  
for pe in range(0,np):  

  proc = str(procs[pe])
  dirname = 'np'+proc+'/'
  direc = path + dirname
  
  # change to run directory
  os.chdir(direc)
  
  if sub_prep:
    
    # submit the prep job
    prep_sub = prep_name + '.sub'
    prep_cmd = ["sbatch", prep_sub]
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    output_sp = output.split()
  
    # find the prep job id
    n = len(output_sp)
    job_id = output_sp[n-1]
    
    print prep_cmd
    print output  
  
    # submit the run job with a dependency on the prep job
    run_sub = run_name + '.sub'
    run_cmd = ["sbatch", '--dependency=afterok:'+job_id, run_sub]
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
  
    print run_cmd
    print output
    
  else:
    
    # submit the run job with a dependency on the prep job
    run_sub = run_name + '.sub'
    run_cmd = ["sbatch", run_sub]
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
  
    print run_cmd
    print output    
