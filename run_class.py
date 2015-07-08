import pprint
import os
import shutil
import subprocess

#####################################################################################################
# Base run class
#####################################################################################################

class Run(object):
  

  
  def __init__(self,case):
    
    self.case = case
    self.header = False
    self.sub_prep = False
    
    
  def input_file(self):      
    #self.content = [{'value':self.case['mesh']+'.grd'  ,  'comment':'! grid file \n'},
                    #{'value':self.case['mesh']+'.bfr'  ,  'comment':'! forcing file \n'},
                    #{'value':self.case['p']            ,  'comment':'! p - polynomial order \n'},
                    #{'value':self.case['ctp']          ,  'comment':'! ctp - parametric coordinate transformation order \n'},
                    #{'value':self.case['hbp']          ,  'comment':'! hbp - bathymetry order \n'},
                    #{'value':self.case['dt']           ,  'comment':'! dt - timestep (seconds) \n'},
                    #{'value':self.case['tf']           ,  'comment':'! tf - final time (days) \n'},
                    #{'value':self.case['dramp']        ,  'comment':'! dramp - ramping parameter (days) \n'},
                    #{'value':self.case['cf']           ,  'comment':'! cf - friction coefficient \n'},
                    #{'value':self.case['nlines']       ,  'comment':'! lines - lines in output files \n'},
                    #{'value':self.case['outdir']       ,  'comment':'! output directory \n'},
                    #{'value':self.case['npart']        ,  'comment':'! npart - edge blocking parameter \n'}]
                    
    self.content = [{'value':"grid_file = "+self.case['mesh']+'.grd'     ,  'comment':'! grid file \n'},
                    {'value':"forcing_file = "+self.case['mesh']+'.bfr'  ,  'comment':'! forcing file \n'},
                    {'value':"p = "+self.case['p']                       ,  'comment':'! p - polynomial order \n'},
                    {'value':"ctp = "+self.case['ctp']                   ,  'comment':'! ctp - parametric coordinate transformation order \n'},
                    {'value':"hbp = "+self.case['hbp']                   ,  'comment':'! hbp - bathymetry order \n'},
                    {'value':"rk = "+self.case['rk']                     ,  'comment':'! RK timestepping scheme \n'},                    
                    {'value':"dt = "+self.case['dt']                     ,  'comment':'! dt - timestep (seconds) \n'},
                    {'value':"tf = "+self.case['tf']                     ,  'comment':'! tf - final time (days) \n'},
                    {'value':"dramp = "+self.case['dramp']               ,  'comment':'! dramp - ramping parameter (days) \n'},
                    {'value':"cf = "+self.case['cf']                     ,  'comment':'! cf - friction coefficient \n'},
                    {'value':"lines = "+self.case['nlines']              ,  'comment':'! lines - lines in output files \n'},
                    {'value':"out_direc = "+self.case['outdir']          ,  'comment':'! output directory \n'},
                    {'value':"npart = "+self.case['npart']               ,  'comment':'! npart - edge blocking parameter \n'}]                    
                    
    self.name = self.case['input']
    
    shutil.copy(self.case['exe'], self.case['direc'])
    
    #f = open(direc + 'CPUtime.log','a+')  
    #f.write('\n')
    #f.close( )    
  
  
  
  def prep_file(self):
    pass
  
  
  
  def run_file(self):
    pass
    

               
  def write_file(self):
    
    f = open(self.name,'w')   
    for line in self.content:
      value = line['value']
      comment = line['comment']    
      spaces = 101 - len(value)    
      f.write(value + spaces*' ' + comment)
    f.close( )     
    
    self.header = False
    
    
    
  def submit_prep(self,direc):
    pass
    
    
    
  def submit_run(self,direc):
    # change to run directory
    os.chdir(direc)
  
    # run
    print "Running in: " + direc
    exe_name = self.case['exe'].split("/")[-1]
    run_cmd = ["./"+exe_name]
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
  
    print run_cmd
    print output        
    

#####################################################################################################
# Run class for Stampede
#####################################################################################################
    
class TACCRun(Run):    



  def prep_file(self): 
    mesh_name = self.case['mesh'].split("/")[-1]
    prep_name = self.case['prep'].split("/")[-1]
    job_name = '_'.join([prep_name,mesh_name,'p'+self.case['p']])
    cores = '1'
    
    if self.header == False:
      self.sub_header(job_name,self.case['pqueue'],self.case['ptime'],cores,self.case['alloc'])    
    self.content.append({'value':'./'+ prep_name +' < prep.in' , 'comment':'\n'})
                    
    f = open(self.case['direc']+'prep.in','w')
    f.write(self.case['proc'])
    f.close()
    
    self.name = self.case['direc']+'prep.sub'  
    
    shutil.copy(self.case['prep'], self.case['direc'])
    
    
    
  def run_file(self):
    mesh_name = self.case['mesh'].split("/")[-1]
    exe_name = self.case['exe'].split("/")[-1]
    post_name = self.case['post'].split("/")[-1]
    job_name = '_'.join([exe_name,mesh_name,'p'+self.case['p']])
    cores = self.case['proc']
    
    if self.header == False:
      self.sub_header(job_name,self.case['rqueue'],self.case['rtime'],cores,self.case['alloc'])
    self.content.append({'value':'cd '+self.case['direc']                                        , 'comment':'\n'})
    self.content.append({'value':self.exe_cmd + ' -np '+ self.case['proc'] + ' ./' + exe_name    , 'comment':'\n'})
    self.content.append({'value':'./'+post_name                                                  , 'comment':'\n'})
    #self.content.append({'value':'echo "' + job_name + ' Complete" | mail -s "' + job_name +' Complete" sbrus@nd.edu', 'comment':'\n'})
    self.content.append({'value':''                                                              , 'comment':'\n'})   
    
    self.name = self.case['direc']+'run.sub'
    
    shutil.copy(self.case['post'], self.case['direc'])
    
    
    
  def sub_header(self,job_name,queue,time,cores,alloc):
    self.content = [{'value':'#!/bin/bash'                          , 'comment':'\n'},
                    {'value':'#SBATCH -J ' + job_name               , 'comment':'# job name\n'},
                    {'value':'#SBATCH -o ' + job_name + '.o%j'      , 'comment':'# output and error file name (%j expands to jobID)\n'},
                    {'value':'#SBATCH -p ' + queue                  , 'comment':'# queue (partition) -- normal, development, etc.\n' },
                    {'value':'#SBATCH -t ' + time                   , 'comment':'# run time (hh:mm:ss)\n'},
                    {'value':'#SBATCH --mail-user=sbrus@nd.edu'     , 'comment':'\n'},
                    {'value':'#SBATCH --mail-type=begin'            , 'comment':'# email me when the job starts\n' },
                    {'value':'#SBATCH --mail-type=end'              , 'comment':'# email me when the job finishes\n' },
                    {'value':'#SBATCH -n ' + cores                  , 'comment':'# total number of mpi tasks requested\n' },
                    {'value':'#SBATCH -A ' + alloc                  , 'comment':'\n\n'}]      
    self.header == True
    self.exe_cmd = 'ibrun'
    
    
    
  def submit_prep(self,direc):
    # change to run directory
    os.chdir(direc)
    
    # submit the prep job
    prep_sub = 'prep.sub'
    prep_cmd = ["sbatch", prep_sub]
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    output_sp = output.split()
  
    # find the prep job id
    n = len(output_sp)
    self.job_id = output_sp[n-1]
    
    self.sub_prep = True
    
    print prep_cmd
    print output  
  
    
    
  def submit_run(self,direc):
    # change to run directory
    os.chdir(direc)    
        
    # submit the run job with a dependency on the prep job
    run_sub = 'run.sub'
    if self.sub_prep == True:
      run_cmd = ["sbatch", '--dependency=afterok:'+self.job_id, run_sub]
    else:
      run_cmd = ["sbatch", run_sub]

    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
      
    self.sub_prep = False
  
    print run_cmd
    print output
  
  
  
    
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

    self.content = [{'value':'#!/bin/csh'              , 'comment':'\n\n'},
                    {'value':'#$ -N ' + job_name       , 'comment':'# job name\n'},
                    {'value':'#$ -q ' + queue_name     , 'comment':'# queue \n' },
                    {'value':'#$ -M sbrus@nd.edu'      , 'comment':'\n'},
                    {'value':'#$ -m abe'               , 'comment':'# email me when the job aborts/begins/ends \n' }]
    if ncores > 1:
      self.content.append({'value':'#$ -pe mpi-' + cores_node + ' ' + cores, 'comment':'\n\n'})
      self.content.append({'value':'module load mvapich2/1.9-intel'        , 'comment':'\n\n'})
    else:
      self.content.append({'value':''                                      , 'comment':'\n'})
      self.content.append({'value':'module load intel'                     , 'comment':'\n\n'})
                    
    self.header == True
    self.exe_cmd = 'mpirun'  
    
    
            
  def submit_prep(self,direc):
    # change to run directory
    os.chdir(direc)
    
    # submit the prep job
    prep_sub = 'prep.sub'
    prep_cmd = ["qsub", prep_sub]
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    output_sp = output.split()
  
    # find the prep job id
    n = len(output_sp)
    self.job_id = output_sp[2]
    
    self.sub_prep = True
    
    print prep_cmd
    print output  
  
    
    
  def submit_run(self,direc):
    # change to run directory
    os.chdir(direc)    
        
    # submit the run job with a dependency on the prep job
    run_sub = 'run.sub'
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
    
