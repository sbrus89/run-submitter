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
    self.post_header = False
    self.sub_prep = False
    self.sub_run = False
    self.sub_post = False
    #self.inp_content = []
    #self.inp_name = ''
    #self.prep_content = []
    #self.prep_name = ''
    #self.run_content = []
    #self.run_name = ''
    #self.exe_name = ''
    #self.run_direc = ''
    #self.cores = ''
    #self.exe_cmd = ''
    #self.job_id = ''
    
    
  def input_file(self,case):      
#    self.inp_content = [{'value':case['mesh']+'.grd'  ,  'comment':'! grid file \n'},
#                    {'value':case['mesh']+'.bfr'  ,  'comment':'! forcing file \n'},
#                    {'value':case['p']            ,  'comment':'! p - polynomial order \n'},
#                    #{'value':case['ctp']          ,  'comment':'! ctp - parametric coordinate transformation order \n'},
#                    #{'value':case['hbp']          ,  'comment':'! hbp - bathymetry order \n'},
#                    {'value':case['dt']           ,  'comment':'! dt - timestep (seconds) \n'},
#                    {'value':case['tf']           ,  'comment':'! tf - final time (days) \n'},
#                    {'value':case['dramp']        ,  'comment':'! dramp - ramping parameter (days) \n'},
#                    {'value':case['cf']           ,  'comment':'! cf - friction coefficient \n'},
#                    {'value':case['nlines']       ,  'comment':'! lines - lines in output files \n'},
#                    {'value':case['npart']        ,  'comment':'! npart - edge blocking parameter \n'},
#                    {'value':case['npart']        ,  'comment':'! npart - edge blocking parameter \n'}]
                    
    inputs = [['grid_file'    , True , '! grid file                                        \n'],
              ['forcing_file' , True , '! forcing file                                     \n'],
              ['bathy_file'   , False, '! high order bathymetry file                       \n'],
              ['curve_file'   , False, '! curved boundary file                             \n'],
              ['p'            , True , '! p - polynomial order                             \n'],
              ['ctp'          , False, '! ctp - parametric coordinate transformation order \n'],
              ['hbp'          , False, '! hbp - bathymetry order                           \n'],
              ['rk'           , False, '! RK timestepping scheme                           \n'],
              ['dt'           , True , '! dt - timestep (seconds)                          \n'],
              ['tf'           , True , '! tf - final time (days)                           \n'],
              ['dramp'        , True , '! dramp - ramping coefficient                      \n'],
              ['cf'           , True , '! cf - friction coefficient                        \n'],
              ['out_direc'    , False, '! out_direc - output directory                     \n'],
              ['npart'        , False, '! npart - edge blocking parameter                  \n'],
              ['h0'           , False, '! h0- minimum depth                                \n'],
              ['coord_sys'    , False, '! coord_sys - coordinate system option             \n'],
              ['slam0'        , False, '! slam0 - center of CPP projection                 \n'],
              ['sphi0'        , False, '! sphi0 - center of CPP projection                 \n'], 
              ['sol_opt'      , False, '! sol_opt - solution output option                 \n'],
              ['sol_snap'     , False, '! sol_snap - solution output interval              \n'],
              ['sta_opt'      , False, '! sta_opt - station output option                  \n'],
              ['sta_snap'     , False, '! sta_snap - station output interval               \n'], 
              ['sta_file'     , False, '! sta_file - station location file                 \n'],
              ['esl'          , False, '! esl - eddy viscosity parameter                   \n']]
              

    self.inp_content = []
    for input in inputs: 
      option = input[0]
      required = input[1]
      comment = input[2]
      if required:
        if option in case:
          self.inp_content.append({'value':option+" = "+case[option],  'comment':comment})
        else:
          print "Required option missing for input file"
          raise SystemExit(0)
      else:
        if option in case:
          self.inp_content.append({'value':option+" = "+case[option],  'comment':comment})


                    
    self.inp_name = case['input']
    
    shutil.copy(case['exe'], case['direc'])
    
    self.write_file(self.inp_name,self.inp_content)
    
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

  def post_file(self,case):
    self.post_name = ''
    self.post_content = []
    

               
  def write_file(self,name,content):
    
      
      
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


  

  def setup_extra_inputs(self,cases,code_name,run_path,code_path):

    print "writing " + code_name + " input file"

    if not os.path.exists(run_path + code_name):
      os.makedirs(run_path + code_name)

    shutil.copy(code_path + code_name, run_path + code_name+"/"+code_name)
    shutil.copy(code_path + code_name+"_run.py", run_path + code_name+"/"+code_name+"_run.py")
    self.write_file(run_path + code_name+"/"+code_name+".inp", cases)


    

#####################################################################################################
# Run class for Stampede
#####################################################################################################
    
class TACCRun(Run):    



  def prep_file(self,case): 
    mesh_name = case['mesh'].split("/")[-1]
    prep_name = case['prep'].split("/")[-1]
    job_name = '_'.join([prep_name,mesh_name,'p'+case['p'],'np'+case['proc']])
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
    job_name = '_'.join([exe_name,mesh_name,'p'+case['p'],'np'+case['proc']])

    self.cores = case['proc']
    
    if self.run_header == False:
      self.run_content = self.sub_header(job_name,case['rqueue'],case['rtime'],self.cores,case['alloc'])

      self.run_header = True
    self.run_content.append({'value':'cd '+case['direc']                                          , 'comment':'\n'})

    if int(self.cores) > 1:
      self.run_content.append({'value':self.exe_cmd + ' -np '+ case['proc'] + ' ./' + exe_name    , 'comment':'\n'})
    else:
      self.run_content.append({'value':'./' + exe_name                                            , 'comment':'\n'})
      
    #self.run_content.append({'value':'echo "' + job_name + ' Complete" | mail -s "' + job_name +' Complete" sbrus@nd.edu', 'comment':'\n'})
    self.run_content.append({'value':''                                                           , 'comment':'\n'})   
    
    self.run_name = case['rdirec']+'run_np'+self.cores+'.sub'
    self.run_direc = case['rdirec']   


  def post_file(self,case):

    mesh_name = case['mesh'].split("/")[-1]
    post_name = case['post'].split("/")[-1]
    job_name = '_'.join([post_name,mesh_name,'p'+case['p'],'np'+case['proc']])
    sub_cores = '1'
    run_cores = case['proc']

    if self.post_header == False:
      self.post_content = self.sub_header(job_name,case['pqueue'],case['ptime'],sub_cores,case['alloc'])
      self.post_header == True
    self.post_content.append({'value':'cd '+case['direc']  , 'comment':'\n'})
    self.post_content.append({'value':'./'+ post_name      , 'comment':'\n'})

    self.post_name = case['rdirec']+'post_np'+run_cores+'.sub'
    self.post_direc = case['rdirec']

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
    print prep_cmd
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    print output
  
    # find the prep job id
    output_sp = output.split()
    n = len(output_sp)
    self.job_id = output_sp[n-1]
    
    self.sub_prep = True
      
    
    
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
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
    print output
   
    self.sub_prep = False # not sure why this is needed
    self.sub_run = True


    if self.cores > 1:
      # find the run job id
      output_sp = output.split()
      n = len(output_sp)
      self.job_id = output_sp[n-1]
   
      post_sub = self.post_name
      post_cmd = ["sbatch", '--dependency=afterok:'+self.job_id, post_sub]
      print post_cmd
      output = subprocess.Popen(post_cmd, stdout=subprocess.PIPE).communicate()[0]
      print output
      
      self.post_sub = True


#    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE)
#    
#    while output.poll() is None:
#      l = output.stdout.readline()
##      print l.rstrip('\n')
#    print output.stdout.read()    
      
  
    
#####################################################################################################
# Run class for CRC machines
#####################################################################################################    
    
    
class CRCRun(TACCRun):
  
  def sub_header(self,job_name,queue,time,cores,alloc):

    import math
    
    ncores = int(cores)

    info = self.machine_info(queue)
    
    queue_name = info['queue_name']
    node_name = info['node_name']
    node_size = info['node_size']
    node_limit = info['node_limit']
    max_cores = info['max_cores']
    mpi_module = info['mpi_module']
    
    req_cores = int(math.ceil(float(cores)/float(node_size))*float(node_size))

    if ncores > 1:  
      if int(req_cores) % int(node_size) != 0:
        print "  Number of cores must be a multiple of " + node_size
        raise SystemExit(0)
      if ncores > max_cores:
	print "  Number of cores must be less than " + str(max_cores)
	raise SystemExit(0)

    content = [{'value':'#!/bin/csh'              , 'comment':'\n\n'},
                    {'value':'#$ -N ' + job_name       , 'comment':'# job name\n'},
                    {'value':'#$ -q ' + queue_name     , 'comment':'# queue \n' },
                    {'value':'#$ -M sbrus@nd.edu'      , 'comment':'# email address \n'},
                    {'value':'#$ -m abe'               , 'comment':'# email me when the job aborts/begins/ends \n' }]
    if ncores > 1:
      content.append({'value':'#$ -pe mpi-' + node_size + ' ' + str(req_cores), 'comment':'\n\n'})
      content.append({'value':'module load ' + mpi_module             , 'comment':'\n'})
#      content.append({'value':'module load netcdf'                    , 'comment':'\n'})      
      content.append({'value':''                                      , 'comment':'\n'})
    else:
      content.append({'value':''                                      , 'comment':'\n'})
      content.append({'value':'module load intel/15.0'                , 'comment':'\n\n'})
      
    self.exe_cmd = 'mpirun'        
      
    return content




                    
  def machine_info(self,queue):

    if queue != "zas" and queue != "athos" and queue != "proteus" and queue != "aegaeon":
      print "  Invalid machine name"
      raise SystemExit(0)

    info = {}
    if queue == 'zas':
      info['queue_name'] = '*@@westerink_dqcopt'
      info['node_name'] = 'dqcopt'
      info['node_size'] = '8'
      info['node_limit'] = (1,64)
      info['max_cores'] = 512
      info['mpi_module'] = 'mvapich2/2.1-intel-15.0-qlc'
    elif queue == 'athos':
      info['queue_name'] = '*@@westerink_d6cneh'
      info['node_name'] = 'd6cneh'
      info['node_size'] = '12'
      info['node_limit'] = (1,83)
      info['max_cores'] = 996
      info['mpi_module'] = 'mvapich2/2.1-intel-15.0-qlc'
    elif queue == 'proteus':
      info['queue_name'] = '*@@westerink_graphics'
      info['node_name'] = 'proteus'
      info['node_size'] = '12'
      info['node_limit'] = (1,2)
      info['max_cores'] = 24
      info['mpi_module'] = 'mvapich2/2.1-intel-15.0-qlc'
    elif queue == 'aegaeon':
#      info['queue_name'] = '*@@westerink_d12chas'
#      info['queue_name'] = '*@@westerink_d12chas_1992'
#      info['queue_name'] = '*@@westerink_d12chas_1488'
#      info['queue_name'] = '*@@westerink_d12chas_984'      
      info['queue_name'] = '*@@westerink_d12chas_1008'
#      info['queue_name'] = '*@@westerink_d12chas_504'
     #info['queue_name'] = '*@@d12chaswell'
      info['node_name'] = 'd12chas'
      info['node_size'] = '24'
      info['node_limit'] = (20,81)
      info['max_cores']  = 1944
      info['mpi_module'] = 'mvapich2/2.1-intel-15.0-mlx'

    return info

    
    
            
  def submit_prep(self,hold=False):
    
    print self.prep_direc
    os.chdir(self.prep_direc)

    # submit the prep job
    prep_sub = self.prep_name
    if not hold:
      prep_cmd = ["qsub", prep_sub]
    else:
      prep_cmd = ["qsub", "-hold_jid "+hold, prep_sub] 
    print prep_cmd
    output = subprocess.Popen(prep_cmd, stdout=subprocess.PIPE).communicate()[0]
    print output    

    # find the prep job id
    output_sp = output.split()
    n = len(output_sp)
    self.job_id = output_sp[2]
    
    self.sub_prep = True
    
    
    
  def submit_run(self):
   
    print self.run_direc    
    os.chdir(self.run_direc)
    
    # submit the run job with a dependency on the prep job
    run_sub = self.run_name
    if self.sub_prep == True:
      run_cmd = ["qsub", '-hold_jid '+self.job_id, run_sub]
    else:
      run_cmd = ["qsub", run_sub]

    print run_cmd
    output = subprocess.Popen(run_cmd, stdout=subprocess.PIPE).communicate()[0]
    print output

    self.sub_prep = False # not sure why this is needed
    self.sub_run = True

    if int(self.cores) > 1:
      # find the run job id
      output_sp = output.split()
      n = len(output_sp)
      self.job_id = output_sp[2]

      # submit the post job
      post_sub = self.post_name
      post_cmd = ["qsub", '-hold_jid '+self.job_id, post_sub]
      print post_cmd
      output = subprocess.Popen(post_cmd, stdout=subprocess.PIPE).communicate()[0]
      print output
      
      self.sub_post = True
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
    
