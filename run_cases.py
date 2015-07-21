# run variables

input_name = 'dgswe.inp'

bundle_flag = False          # bundle runs with same number of processors into same submission script
                             # 'rdirec' needs to be the same for each bundle of runs
processors = ['32']
prep_time = '00:20:00'
run_time = ['06:00:00','06:00:00','06:00:00']

allocation = 'TG-DMS080016N'

run_queue = 'normal'
#run_queue = 'athos'
prep_queue = 'serial'
#prep_queue = 'proteus'

exe_name = 'dgswe'
#exe_name = 'pdgswe'
prep_name = 'dgprep'
post_name = 'dgpost'

grid_names = ['converge']
p_orders = ['1','2','3']
ctp_orders = ['2','2','3']
hbp_orders = ['1','2','3']
rk_types = ['22','33','45']
timesteps = ['.5d0','.25d0','.125d0']
#timesteps = ['.25d0','.125d0','.0625d0']
#timesteps = ['.125d0','.0625d0','.03125d0']
#timesteps = ['.0625d0','.03125d0','.015625d0']

final_time = '1d0'
ramp_length = '.08d0'
fric_coef = '.0025d0'
num_snaps = '10d0'
output_direc = './'
num_partitions = '1'

# Run, grid, and executable paths
run_path = '/home/sbrus/SmallProjects/run_script/test/'
code_path = '/home/sbrus/Codes/dgswe/work/'
grid_path = '/home/sbrus/Codes/dgswe/grids/'
#run_path = '/work/01964/sbrus/dgswe_converge_bath_dt2/'
#code_path = '/home1/01964/sbrus/dgswe/work/'
#grid_path = '/home1/01964/sbrus/dgswe/grids/'

# set up cases list
cases = []
for k,grid in enumerate(grid_names):
  for i,p in enumerate(p_orders):
    ctp = ctp_orders[i]
    dt = timesteps[i]
    rk = rk_types[i]
    rtime = run_time[i]
    for j in range(0,i+1):
      hbp = str(j+1)
      directory_name = run_path + grid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/' + 'hbp'+hbp+'/'
      cases.append({'input':directory_name+input_name,
	            'mesh':grid_path+grid ,
	            
                    'p':p,
                    'ctp':ctp, 
                    'hbp':hbp, 
                    
                    'rk':rk,
                    'dt':dt,                     
                    'tf':final_time,
                    'dramp':ramp_length,
                    
                    'cf':fric_coef, 
                    
                    'nlines':num_snaps,
                    'outdir':output_direc,
                    
                    'npart':num_partitions, 
                    
                    'direc':directory_name,    
                    #'rdirec':run_path,
                    'rdirec':directory_name,
                    'proc':processors[0],
                    'exe':code_path+exe_name,
                    'rtime':rtime,
                    'rqueue':run_queue.lower(),
                    
                    'prep':code_path+prep_name,
                    'ptime':prep_time,
                    'pqueue':prep_queue.lower(),
                    'alloc':allocation,
                    'post':code_path+post_name})

                    
                    
                    
#for k,grid in enumerate(grid_names):
#  for i,p in enumerate(p_orders):
#    ctp = ctp_orders[i]
#    hbp = hbp_orders[0]
#    dt = timesteps[i]
#    rk = rk_types[i]
#    rtime = run_time[i]
#    directory_name = run_path + grid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/'
#    cases.append({'input':directory_name+input_name,
#                    'mesh':grid_path+grid ,
#
#                    'p':p,
#                    'ctp':ctp,
#                    'hbp':hbp,
#
#                    'rk':rk,
#                    'dt':dt,
#                    'tf':final_time,
#                    'dramp':ramp_length,
#
#                    'cf':fric_coef,
#
#                    'nlines':num_snaps,
#                    'outdir':output_direc,
#
#                    'npart':num_partitions,
#
#                    'direc':directory_name,
#                    'rdirec':directory_name,
#                    'proc':processors[0],
#                    'exe':code_path+exe_name,
#                    'rtime':rtime,
#                    'rqueue':run_queue.lower(),
#
#                    'prep':code_path+prep_name,
#                    'ptime':prep_time,
#                    'pqueue':prep_queue.lower(),
#                    'alloc':allocation,
#                    'post':code_path+post_name})










## run variables

#input_name = 'dgswe.inp'

#bundle_flag = True          # bundle runs with same number of processors into same submission script
                             ## 'rdirec' needs to be the same for each bundle of runs
#processors = ['32','64','128']
#prep_time = '00:20:00'
#run_time = ['06:00:00','03:00:00','01:30:00']

#allocation = 'TG-DMS080016N'

#run_queue = 'normal'
##run_queue = 'athos'
#prep_queue = 'serial'
##prep_queue = 'proteus'

#exe_name = 'dgswe'
#prep_name = 'dgprep'
#post_name = 'dgpost'

#grid_names = ['inlet6']
#p_orders = ['1','2','3']
#ctp_orders = ['1']
#hbp_orders = ['1']
#rk_types = ['22']
#timesteps = ['.01d0','.01d0','.01d0']

#final_time = '.1d0'
#ramp_length = '.5d0'
#fric_coef = '.003d0'
#num_snaps = '1d0'
#output_direc = './'
#num_partitions = '1'

## Run, grid, and executable paths
#run_path = '/home/sbrus/SmallProjects/run_script/test/'
#code_path = '/home/sbrus/Codes/dgswe/work/'
#grid_path = '/home/sbrus/Codes/dgswe/grids/'
##run_path = '/work/01964/sbrus/dgswe_converge_bath_dt2/'
##code_path = '/home1/01964/sbrus/dgswe/work/'
##grid_path = '/home1/01964/sbrus/dgswe/grids/'

## set up cases list
#cases = []
#for k,cores in enumerate(processors):
  #rtime = run_time[k]  
  #for i,p in enumerate(p_orders):
    #ctp = ctp_orders[0]
    #hbp = hbp_orders[0]
    #dt = timesteps[i]
    #rk = rk_types[0]
    #grid = grid_names[0]

    #directory_name = run_path + grid+'/' + 'p'+p+'/' + 'np'+cores+'/'
    #cases.append({'input':directory_name+input_name,
                    #'mesh':grid_path+grid ,
                    
                    #'p':p,
                    #'ctp':ctp, 
                    #'hbp':hbp, 
                    
                    #'rk':rk,
                    #'dt':dt,                     
                    #'tf':final_time,
                    #'dramp':ramp_length,
                    
                    #'cf':fric_coef, 
                    
                    #'nlines':num_snaps,
                    #'outdir':output_direc,
                    
                    #'npart':num_partitions, 
                    
                    #'direc':directory_name,    
                    #'rdirec':run_path,
                    #'proc':cores,
                    #'exe':code_path+exe_name,
                    #'rtime':rtime,
                    #'rqueue':run_queue.lower(),
                    
                    #'prep':code_path+prep_name,
                    #'ptime':prep_time,
                    #'pqueue':prep_queue.lower(),
                    #'alloc':allocation,
                    #'post':code_path+post_name})