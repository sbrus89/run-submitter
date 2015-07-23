import pprint
import os
import shutil
import subprocess

#####################################################################################################
# Base run class
#####################################################################################################

class Run(object):
  

  
  def __init__(self):
    
    self.prep_header = False
    self.run_header = False
    self.sub_prep = False
    
    
  def input_file(self,case):      
    #self.inp_content = [{'value':case['mesh']+'.grd'  ,  'comment':'! grid file \n'},
                    #{'value':case['mesh']+'.bfr'  ,  'comment':'! forcing file \n'},
                    #{'value':case['p']            ,  'comment':'! p - polynomial order \n'},
                    #{'value':case['ctp']          ,  'comment':'! ctp - parametric coordinate transformation order \n'},
                    #{'value':case['hbp']          ,  'comment':'! hbp - bathymetry order \n'},
                    #{'value':case['dt']           ,  'comment':'! dt - timestep (seconds) \n'},
                    #{'value':case['tf']           ,  'comment':'! tf - final time (days) \n'},
                    #{'value':case['dramp']        ,  'comment':'! dramp - ramping parameter (days) \n'},
                    #{'value':case['cf']           ,  'comment':'! cf - friction coefficient \n'},
                    #{'value':case['nlines']       ,  'comment':'! lines - lines in output files \n'},
                    #{'value':case['outdir']       ,  'comment':'! output directory \n'},
                    #{'value':case['npart']        ,  'comment':'! npart - edge blocking parameter \n'}]
                    
    self.inp_content = [{'value':"grid_file = "+case['mesh']+'.grd' ,  'comment':'! grid file \n'},
                    {'value':"forcing_file = "+case['mesh']+'.bfr'  ,  'comment':'! forcing file \n'},
                    {'value':"bathy_file = "+case['bathy']          ,  'comment':'! high order bathymetry file \n'},                    
                    {'value':"p = "+case['p']                       ,  'comment':'! p - polynomial order \n'},
                    {'value':"ctp = "+case['ctp']                   ,  'comment':'! ctp - parametric coordinate transformation order \n'},
                    {'value':"hbp = "+case['hbp']                   ,  'comment':'! hbp - bathymetry order \n'},
                    {'value':"rk = "+case['rk']                     ,  'comment':'! RK timestepping scheme \n'},                    
                    {'value':"dt = "+case['dt']                     ,  'comment':'! dt - timestep (seconds) \n'},
                    {'value':"tf = "+case['tf']                     ,  'comment':'! tf - final time (days) \n'},
                    {'value':"dramp = "+case['dramp']               ,  'comment':'! dramp - ramping parameter (days) \n'},
                    {'value':"cf = "+case['cf']                     ,  'comment':'! cf - friction coefficient \n'},
                    {'value':"lines = "+case['nlines']              ,  'comment':'! lines - lines in output files \n'},
                    {'value':"out_direc = "+case['outdir']          ,  'comment':'! output directory \n'},
                    {'value':"npart = "+case['npart']               ,  'comment':'! npart - edge blocking parameter \n'}]                    
                    
    self.inp_name = case['input']
    
    shutil.copy(case['exe'], case['direc'])
    
   # if 'copy_files' in case:
   #   for cpfile in case['copy_files']:
   #     shutil.copy(cpfile, case['direc'])
    
    #f = open(direc + 'CPUtime.log','a+')  
    #f.write('\n')
    #f.close( )    
  
  
  
  def prep_file(self,case):
    self.prep_name = ''
    self.prep_content = []
  
  
  
  def run_file(self,case):
    self.run_name = ''
    self.run_content = []
    self.exe_name = case['exe'].split("/")[-1]
    self.run_direc = case['direc']
    

               
  def write_file(self,file_type):
    
    if file_type == 'input':
      name = self.inp_name
      content = self.inp_content
    elif file_type == 'run':
      name = self.run_name
      content = self.run_content
    elif file_type == 'prep':
      name = self.prep_name
      content = self.prep_content
      
      
    if name != '':
      f = open(name,'w')   
      for line in content:
        value = line['value']
        comment = line['comment']    
        spaces = 101 - len(value)    
        f.write(value + spaces*' ' + comment)
      f.close()     
    
    
    
  def submit_prep(self):
    pass
    
    
    
  def submit_run(self):

    print self.run_direc        
    
    # change to run directory
    os.chdir(self.run_direc)
  
    # run
    print "Running in: " + self.run_direc
    run_cmd = ["./"+self.exe_name]
    print run_cmd     
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE)
    
    while output.poll() is None:
      l = output.stdout.readline()
      print l.rstrip('\n')
    print output.stdout.read()
  

    

#####################################################################################################
# Run class for Stampede
#####################################################################################################
    
class TACCRun(Run):    



  def prep_file(self,case): 
    mesh_name = case['mesh'].split("/")[-1]
    prep_name = case['prep'].split("/")[-1]
    job_name = '_'.join([prep_name,mesh_name,'p'+case['p']])
    sub_cores = '1'
    run_cores = case['proc']
    
    if self.prep_header == False:
      self.prep_content = self.sub_header(job_name,case['pqueue'],case['ptime'],sub_cores,case['alloc']) 
      self.prep_header = True
    self.prep_content.append({'value':'cd '+case['direc']           , 'comment':'\n'})
    self.prep_content.append({'value':'./'+ prep_name +' < prep.in' , 'comment':'\n'})
                    
    f = open(case['direc']+'prep.in','w')
    f.write(run_cores)
    f.close()
    
    self.prep_name = case['rdirec']+'prep_np'+run_cores+'.sub'  
    self.prep_direc = case['rdirec']   
    
    shutil.copy(case['prep'], case['direc'])
    
    
    
  def run_file(self,case):
    mesh_name = case['mesh'].split("/")[-1]
    exe_name = case['exe'].split("/")[-1]
    post_name = case['post'].split("/")[-1]
    job_name = '_'.join([exe_name,mesh_name,'p'+case['p']])
    cores = case['proc']
    
    if self.run_header == False:
      self.run_content = self.sub_header(job_name,case['rqueue'],case['rtime'],cores,case['alloc'])
      self.run_header = True
    self.run_content.append({'value':'cd '+case['direc']                                        , 'comment':'\n'})
    self.run_content.append({'value':self.exe_cmd + ' -np '+ case['proc'] + ' ./' + exe_name    , 'comment':'\n'})
    self.run_content.append({'value':'./'+post_name                                             , 'comment':'\n'})
    #self.run_content.append({'value':'echo "' + job_name + ' Complete" | mail -s "' + job_name +' Complete" sbrus@nd.edu', 'comment':'\n'})
    self.run_content.append({'value':''                                                         , 'comment':'\n'})   
    
    self.run_name = case['rdirec']+'run_np'+cores+'.sub'
    self.run_direc = case['rdirec']
    
    shutil.copy(case['post'], case['direc'])
    
    
    
  def sub_header(self,job_name,queue,time,cores,alloc):
    content = [{'value':'#!/bin/bash'                          , 'comment':'\n'},
                    {'value':'#SBATCH -J ' + job_name               , 'comment':'# job name\n'},
                    {'value':'#SBATCH -o ' + job_name + '.o%j'      , 'comment':'# output and error file name (%j expands to jobID)\n'},
                    {'value':'#SBATCH -p ' + queue                  , 'comment':'# queue (partition) -- normal, development, etc.\n' },
                    {'value':'#SBATCH -t ' + time                   , 'comment':'# run time (hh:mm:ss)\n'},
                    {'value':'#SBATCH --mail-user=sbrus@nd.edu'     , 'comment':'\n'},
                    {'value':'#SBATCH --mail-type=begin'            , 'comment':'# email me when the job starts\n' },
                    {'value':'#SBATCH --mail-type=end'              , 'comment':'# email me when the job finishes\n' },
                    {'value':'#SBATCH -n ' + cores                  , 'comment':'# total number of mpi tasks requested\n' },
                    {'value':'#SBATCH -A ' + alloc                  , 'comment':'\n\n'}]      
    self.exe_cmd = 'ibrun'
    
    return content
    
    
    
  def submit_prep(self):

    print self.prep_direc    
    os.chdir(self.prep_direc)
    
    # submit the prep job
    prep_sub = self.prep_name
    prep_cmd = ["sbatch", prep_sub]
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    output_sp = output.split()
  
    # find the prep job id
    n = len(output_sp)
    self.job_id = output_sp[n-1]
    
    self.sub_prep = True
    
    print prep_cmd
    print output  
  
    
    
  def submit_run(self):

    print self.run_direc     
    os.chdir(self.run_direc)  
        
    # submit the run job with a dependency on the prep job
    run_sub = self.run_name
    if self.sub_prep == True:
      run_cmd = ["sbatch", '--dependency=afterok:'+self.job_id, run_sub]
    else:
      run_cmd = ["sbatch", run_sub]
      
    print run_cmd
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE)
    
    while output.poll() is None:
      l = output.stdout.readline()
      print l.rstrip('\n')
    print output.stdout.read()    
      
    self.sub_prep = False
   
  
    
#####################################################################################################
# Run class for CRC machines
#####################################################################################################    
    
    
class CRCRun(TACCRun):
  
  def sub_header(self,job_name,queue,time,cores,alloc):
    
    if queue != "zas" and queue != "athos" and queue != "proteus":
      print "  Invalid machine name"
      raise SystemExit(0)
        
    if queue == 'zas':
      queue_name = '*@@westerink_dqcopt'
      cores_node = '8'
      max_cores = '512'
    elif queue == 'athos':
      queue_name = '*@@westerink_d6cneh'
      cores_node = '12'
      max_cores = '996'
    elif queue == 'proteus':
      queue_name = '*@@westerink_graphics'
      cores_node = '12'
      max_cores = 24
    
    ncores = int(cores)
    
    if ncores > 1:  
      if ncores % int(cores_node) != 0:
        print "  Number of cores must be a multiple of " + cores_node
        raise SystemExit(0)
      if ncores > max_cores:
	print "  Number of cores must be less than " + str(max_cores)
	raise SystemExit(0)

    content = [{'value':'#!/bin/csh'              , 'comment':'\n\n'},
                    {'value':'#$ -N ' + job_name       , 'comment':'# job name\n'},
                    {'value':'#$ -q ' + queue_name     , 'comment':'# queue \n' },
                    {'value':'#$ -M sbrus@nd.edu'      , 'comment':'\n'},
                    {'value':'#$ -m abe'               , 'comment':'# email me when the job aborts/begins/ends \n' }]
    if ncores > 1:
      content.append({'value':'#$ -pe mpi-' + cores_node + ' ' + cores, 'comment':'\n\n'})
      content.append({'value':'module load mvapich2/1.9-intel'        , 'comment':'\n\n'})
    else:
      content.append({'value':''                                      , 'comment':'\n'})
      content.append({'value':'module load intel'                     , 'comment':'\n\n'})
      
    return content
                    
    self.header == True
    self.exe_cmd = 'mpirun'  
    
    
            
  def submit_prep(self):
    
    print self.prep_direc
    os.chdir(self.prep_direc)

    # submit the prep job
    prep_sub = self.prep_name
    prep_cmd = ["qsub", prep_sub]
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    output_sp = output.split()
  
    # find the prep job id
    n = len(output_sp)
    self.job_id = output_sp[2]
    
    self.sub_prep = True
    
    print prep_cmd
    print output  
  
    
    
  def submit_run(self):
   
    print self.run_direc    
    os.chdir(self.run_direc)
    
    # submit the run job with a dependency on the prep job
    run_sub = self.run_name
    if self.sub_prep == True:
      run_cmd = ["qsub", '-hold_jid '+self.job_id, run_sub]
    else:
      run_cmd = ["qsub", run_sub]

    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
      
    self.sub_prep = False
  
    print run_cmd
    print output    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  # Lonestar submission script
  
  #fname = direc + run_name +'.sub'
  #f = open(fname,'w')
  #f.write('#!/bin/bash                \n')
  #f.write('#$ -V                      \n')
  #f.write('#$ -cwd                    \n')
  #f.write('#$ -N '+ run_job + proc +'        \n')
  #f.write('#$ -pe 1way 12             \n')
  #f.write('#$ -q '+ run_quene +'      \n')
  #f.write('#$ -l h_rt='+ run_time  +' \n')
  #f.write('#$ -M sbrus@nd.edu         \n')
  #f.write('#$ -m abe                  \n')
  #f.write('\n')
  #f.write('./' + run_name + '\n')
  #f.write('\n')
  #f.close( )
    
