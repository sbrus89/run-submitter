#!/usr/local/bin/python

import os
import shutil
import subprocess

sub_prep = 0
do_post = 0

prep_quene = 'serial'
#prep_quene = 'normal'
run_quene = 'normal'

prep_time = '04:00:00'
#run_time = ['04:00:00','02:30:00','01:30:00','01:00:00','00:45:00','00:30:00','00:20:00','00:20:00']
#run_time = ['09:00:00','05:00:00','03:00:00','02:00:00','01:30:00','01:30:00','01:00:00','00:45:00']
#run_time = ['00:10:00','00:10:00']
#run_time = ['24:00:00','12:00:00','08:00:00','07:00:00','06:00:00','05:00:00','04:30:00','04:30:00']
run_time = ['04:00:00','04:00:00','04:00:00']

run_names = [['dgswe_mpi','dgprep','dgpost_nc'],['dgswem_structure_mpi','adcprep','dgpost']]

p_orders = ['1','2','3']
dt = '.01d0'
final_time = '.1d0'
lines = '1d0'

grid_name = 'inlet6'


#procs = [2, 4, 8, 16, 32, 64, 128, 256]
#procs = [512,1024]
#procs = [2048]
#procs = [128, 256]
#procs = [128]
#procs = [16, 32, 64, 128, 256, 512, 1024]
#procs = [64, 128, 256, 512, 1024, 2048, 3200, 4000]
procs = [4096,8192,16384]


home_path = '/home1/01964/sbrus/'
work_path = '/work/01964/sbrus/'
code_path = home_path + 'dgswe/work/'
grid_path = home_path + 'dgswe/grids/'



allocation = 'TG-DMS080016N'

prep_sub_name = 'prep_np'
run_sub_name  = 'run_np'



######################################## 
# Setup run directories
########################################  

np = len(procs)

if np != len(run_time):
  print 'The processor and run time list are not the same length'
  raise SystemExit(0)



for pe in range(0,np):
  
  proc = str(procs[pe]) # process number as a string
  
  prep_job_name = prep_sub_name + proc
  run_job_name  = run_sub_name + proc
  
  # write the prep submission script  
  fname = work_path + prep_job_name + '.sub'
  prep_sub = open(fname,'w')
  prep_sub.write('#!/bin/bash\n')
  prep_sub.write('#SBATCH -J ' + prep_job_name +'           # job name\n')
  prep_sub.write('#SBATCH -o ' + prep_job_name + '.o%j       # output and error file name (%j expands to jobID)\n')
  prep_sub.write('#SBATCH -p ' + prep_quene + ' 	           # queue (partition) -- normal, development, etc.\n')
  prep_sub.write('#SBATCH -t ' + prep_time + '                   # run time (hh:mm:ss)\n')
  prep_sub.write('#SBATCH --mail-user=sbrus@nd.edu\n')
  prep_sub.write('#SBATCH --mail-type=begin             # email me when the job starts\n')  
  prep_sub.write('#SBATCH --mail-type=end               # email me when the job finishes\n')
  prep_sub.write('#SBATCH -n 1                          # total number of mpi tasks requested\n')  
  prep_sub.write('#SBATCH -A ' + allocation + '\n')
  prep_sub.write('\n') 


  # write the run submission script
  fname = work_path + run_job_name + '.sub'
  run_sub = open(fname,'w')
  run_sub.write('#!/bin/bash\n')
  run_sub.write('#SBATCH -J ' + run_job_name + '           # job name\n')
  run_sub.write('#SBATCH -o ' + run_job_name + '.o%j       # output and error file name (%j expands to jobID)\n')
  if procs[pe] > 4096:
    run_sub.write('#SBATCH -p ' + 'large' + ' 	           # queue (partition) -- normal, development, etc.\n')
  else:
    run_sub.write('#SBATCH -p ' + run_quene + ' 	           # queue (partition) -- normal, development, etc.\n')
  run_sub.write('#SBATCH -t ' + run_time[pe] + '                   # run time (hh:mm:ss)\n')
  run_sub.write('#SBATCH --mail-user=sbrus@nd.edu\n')
  run_sub.write('#SBATCH --mail-type=begin             # email me when the job starts\n')  
  run_sub.write('#SBATCH --mail-type=end               # email me when the job finishes\n')
  run_sub.write('#SBATCH -n ' + proc + '               # total number of mpi tasks requested\n')  
  run_sub.write('#SBATCH -A ' + allocation + '\n')
  run_sub.write('\n') 
  run_sub.write('module load netcdf\n')
  run_sub.write('export MV2_SHOW_CPU_BINDING=1\n')
  run_sub.write('\n')

      
  for run in run_names:
    
    
    prep_name = run[1] 
    run_name  = run[0]
    post_name = run[2]
   
    run_path = work_path + run_name + '_runs/'    
  
    for p in p_orders:      
  
      dirname = grid_name + '/' + 'p'+p+ '/' + 'np'+proc+'/' # name of run directory
      direc = run_path + dirname # run directory path
  
      print 'setting up directory: ' + direc  
  
      # make the directory if necessary
      if not os.path.exists(direc):
        os.makedirs(direc)  

      # check if prep directories are present
      if sub_prep != 1:
        for i in range(0,procs[pe]):
#          num = "%04d" % i
          num = "%05d" % i
          pe_path = direc + 'PE' + num
          if not os.path.exists(pe_path):
            print 'error: job must be prepped for the correct number of cores before submitting'
            print '       resubmit with sub_prep = 1'
            raise SystemExit(0)

    
      # write the prep.in file    
      fname = direc + 'prep.in'
      f = open(fname,'w')
      f.write(proc)
      f.close()

      # create the input file
      input_direc = direc + 'dgswe.inp'
      f = open(input_direc,'w')
      f.write(grid_path + grid_name + '.grd                                             ! grid file                        \n')
      f.write(grid_path + grid_name + '.bfr                                             ! forcing file                     \n')
      f.write(p  + '                                                                                      ! p - polynomial order             \n')
      f.write(dt + '                                                                                      ! dt - timestep                    \n')
      f.write(final_time + '                                                                                    ! tf - final time                  \n')
      f.write('.5d0                                                                                   ! dramp - ramping parameter        \n')
      f.write('.003d0                                                                                 ! cf - friction coefficient        \n')
      f.write(lines + '                                                                                       ! lines - lines in ouput files     \n')
      f.write('1                                                                                      ! nsp - loop blocking paramenter   \n')
      f.write('1                                                                                      ! npart - loop blocking paramenter \n')
      f.close( )

    
      # write the prep submission script  
      prep_sub.write('cd '+ direc + '\n')
      prep_sub.write('./make_dirs.py\n')
      prep_sub.write('./' + prep_name + ' < prep.in\n\n')

      # write the run submission script
      run_sub.write('cd '+ direc + '\n')
      run_sub.write('ibrun -np ' + proc + ' ./' + run_name + '\n')
      if do_post == 1:
	run_sub.write('./' + post_name + '\n')
      run_sub.write('\n')
 

  
      # copy the prep executable 
      if sub_prep == 1:
	prep_src = code_path + prep_name
	prep_dst = direc + prep_name
	shutil.copy(prep_src,prep_dst)
	shutil.copy(home_path+'make_dirs.py', direc+'make_dirs.py')
      
      # copy the run executable
      run_src = code_path + run_name
      run_dst = direc + run_name
      shutil.copy(run_src,run_dst)
      
      # copy the post executable
      if do_post == 1:
	post_src = code_path + post_name
	post_dst = direc + post_name
	shutil.copy(post_src,post_dst)
	
  prep_sub.close()
  run_sub.close()
      
raise SystemExit(0)  





# change to run directory
os.chdir(work_path)
print work_path

########################################
# Submit Jobs
########################################  
for pe in range(0,np):  

  proc = str(procs[pe])

  prep_job_name = prep_sub_name + proc
  run_job_name  = run_sub_name + proc  
  
  if sub_prep:
    
    # submit the prep job
    prep_sub = prep_job_name + '.sub'
    prep_cmd = ["sbatch", prep_sub]
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    output_sp = output.split()
  
    # find the prep job id
    n = len(output_sp)
    job_id = output_sp[n-1]
    
    print prep_cmd
    print output  
  
    # submit the run job with a dependency on the prep job
    run_sub = run_job_name + '.sub'
    run_cmd = ["sbatch", '--dependency=afterok:'+job_id, run_sub]
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
  
    print run_cmd
    print output
    
  else:
    
    # submit the run job with a dependency on the prep job
    run_sub = run_job_name + '.sub'
    run_cmd = ["sbatch", run_sub]
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
  
    print run_cmd
    print output    
