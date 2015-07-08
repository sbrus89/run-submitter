# run variables

input_name = 'dgswe.inp'

processors = '32'
prep_time = '00:20:00'
run_time = ['06:00:00','06:00:00','06:00:00']

allocation = 'TG-DMS080016N'

run_queue = 'normal'
#run_queue = 'athos'
prep_queue = 'serial'
#prep_queue = 'proteus'

exe_name = ['pdgswe_rk22','pdgswe_rk33','pdgswe_rk45']
prep_name = 'dgprep'
post_name = 'dgpost'

grid_names = ['converge3']
p_orders = ['1','2','3']
ctp_orders = ['2','2','3']
hpb_orders = ['1','2','3']
#timesteps = ['.5d0','.25d0','.125d0']
#timesteps = ['.25d0','.125d0','.0625d0']
#timesteps = ['.125d0','.0625d0','.03125d0']
timesteps = ['.0625d0','.03125d0','.015625d0']

final_time = '1d0'
ramp_length = '.08d0'
fric_coef = '.0025d0'
num_snaps = '10d0'
output_direc = './'
num_partitions = '1'

# Run, grid, and executable paths
run_path = '/work/01964/sbrus/dgswe_converge_bath_dt2/'
code_path = '/home1/01964/sbrus/dgswe/work/'
grid_path = '/home1/01964/sbrus/dgswe/grids/'

# set up cases list
cases = []
for k,grid in enumerate(grid_names):
  for i,p in enumerate(p_orders):
    ctp = ctp_orders[i]
    dt = timesteps[i]
    exe = exe_name[i]
    rtime = run_time[i]
    for j in range(0,i+1):
      hbp = str(j+1)
      directory_name = run_path + grid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/' + 'hbp'+hbp+'/'
      cases.append({'input':directory_name+input_name,
	            'mesh':grid_path+grid ,
                    'p':p,
                    'ctp':ctp, 
                    'dt':dt, 
                    'hbp':hbp, 
                    'tf':final_time,
                    'dramp':ramp_length,
                    'cf':fric_coef, 
                    'nlines':num_snaps,
                    'outdir':output_direc,
                    'npart':num_partitions, 
                    
                    'direc':directory_name,                    
                    'proc':processors,
                    'exe':code_path+exe,
                    'rtime':rtime,
                    'rqueue':run_queue.lower(),
                    
                    'prep':code_path+prep_name,
                    'ptime':prep_time,
                    'pqueue':prep_queue.lower(),
                    'alloc':allocation,
                    'post':code_path+post_name})
