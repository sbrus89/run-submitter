


#############################
## Scaling test on aegeaon
#############################

#input_name = 'dgswe.inp'

#bundle_flag = False          # bundle runs with same number of processors into same submission script
                             ## 'rdirec' needs to be the same for each bundle of runs
##processors = ['24','48','96','192','384','768']
##processors = ['96','192','384','768']
#processors = ['1536']
#prep_time = '00:20:00'
#run_time = ['01:00:00','01:00:00','01:00:00','01:00:00','01:00:00','01:00:00']
#max_proc = 2000

#allocation = 'TG-DMS080016N'

#run_queue = 'aegaeon'
#prep_queue = 'proteus'

#exe_name = 'dgswe_mpi'
#prep_name = 'dgprep'
#post_name = 'dgpost_nc'
##exe_name = 'dgswem_structure_mpi'
##prep_name = 'adcprep'
##post_name = 'dgpost_nc'


##grid_names = ['inlet3']
#grid_names = ['inlet6']
#p_orders = ['1','2','3']
#ctp_orders = ['1']
#hbp_orders = ['1']
#rk_types = ['22']
##timesteps = ['.1d0','.1d0','.1d0']
#timesteps = ['.01d0','.01d0','.01d0']


#final_time = '1d0'
#ramp_length = '.5d0'
#fric_coef = '.003d0'
##num_snaps = '10d0'
#num_snaps = '1d0'
#output_direc = './'
#num_partitions = '1'

## Run, grid, and executable paths
#run_path = '/home2/sbrus/dgswe_aegeaon_scaling/'
##run_path = '/home2/sbrus/dgswem_structure_aegeaon_scaling/'
#code_path = '/home2/sbrus/dgswe_aegeaon_scaling/'
##code_path = '/home2/sbrus/dgswem_structure_aegeaon_scaling/'
##code_path = '/home2/sbrus/dgswe/work/'
#grid_path = '/home2/sbrus/dgswe/grids/'

## set up cases list
#cases = []
#for k,cores in enumerate(processors):
#  rtime = run_time[k]  
#  for i,p in enumerate(p_orders):
#    ctp = ctp_orders[0]
#    hbp = hbp_orders[0]
#    dt = timesteps[i]
#    rk = rk_types[0]
#    grid = grid_names[0]

#    directory_name = run_path + grid+'/' + 'p'+p+'/' + 'np'+cores+'/'
#    cases.append({'input':directory_name+input_name,
#                    'mesh':grid_path+grid ,
                    
#                    'p':p,
#                    'ctp':ctp, 
#                    'hbp':hbp, 
                    
#                    'rk':rk,
#                    'dt':dt,                     
#                    'tf':final_time,
#                    'dramp':ramp_length,
                    
#                    'cf':fric_coef, 
                    
#                    'nlines':num_snaps,
#                    'outdir':output_direc,
                    
#                    'npart':num_partitions, 
                    
#                    'direc':directory_name,    
#                    'rdirec':directory_name,
#                    'proc':cores,
#                    'exe':code_path+exe_name,
#                    'rtime':rtime,
#                    'rqueue':run_queue.lower(),
                    
#                    'prep':code_path+prep_name,
#                    'ptime':prep_time,
#                    'pqueue':prep_queue.lower(),
#                    'alloc':allocation,
#                    'post':code_path+post_name})












#############################
## Inlet convergence study
#############################





## run variables

#input_name = 'dgswe.inp'

#bundle_flag = False          # bundle runs with same number of processors into same submission script
                             ## 'rdirec' needs to be the same for each bundle of runs
#processors = ['12']
#prep_time = '00:5:00'
#run_time = ['06:00:00','06:00:00','06:00:00']
#max_proc = 768

#allocation = 'TG-DMS080016N'

##run_queue = 'normal'
#run_queue = 'athos'
##prep_queue = 'serial'
#prep_queue = 'proteus'

#exe_name = 'dgswe'
##exe_name = 'pdgswe'
#prep_name = 'dgprep'
#post_name = 'dgpost'

#grid_names = ['inlet1']
#p_orders = ['1','2','3']
#ctp_orders = ['1']
#hbp_orders = ['1','2','3']
#rk_types = ['22','33','45']
#timesteps = ['.5d0','.25d0','.125d0']
##timesteps = ['.25d0','.125d0','.0625d0']
##timesteps = ['.125d0','.0625d0','.03125d0']
##timesteps = ['.0625d0','.03125d0','.015625d0']

#final_time = '1d0'
#ramp_length = '.5d0'
#fric_coef = '.003d0'
#num_snaps = '10d0'
#output_direc = './'
#num_partitions = '1'

## Run, grid, and executable paths
#run_path = '/home/sbrus/SmallProjects/run_script/test/'
#code_path = '/home/sbrus/Codes/dgswe/work/'
#grid_path = '/home/sbrus/Codes/dgswe/grids/'
##run_path = '/work/01964/sbrus/dgswe_inlet_bath/'
##code_path = '/home1/01964/sbrus/dgswe/work/'
##grid_path = '/work/01964/sbrus/dgswe_inlet_bath/grids/'

## set up cases list
#cases = []
#for k,grid in enumerate(grid_names):
  #for i,p in enumerate(p_orders):
    #dt = timesteps[i]
    #rk = rk_types[i]
    #rtime = run_time[i]
    #for j in range(0,i+1):
      #hbp = str(j+1)
      #directory_name = run_path + grid+'/' + 'p'+p+'/' + 'hbp'+hbp+'/'
      #cases.append({'input':directory_name+input_name,
                    #'mesh':grid_path+grid ,
                    #'bathy':grid_path+grid+'_hbp'+hbp+'.d',
                    
                    #'p':p,
                    #'ctp':ctp_orders[0], 
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
                    ##'rdirec':run_path,
                    #'rdirec':directory_name,
                    #'proc':processors[0],
                    #'exe':code_path+exe_name,
                    #'rtime':rtime,
                    #'rqueue':run_queue.lower(),
                    
                    #'prep':code_path+prep_name,
                    #'ptime':prep_time,
                    #'pqueue':prep_queue.lower(),
                    #'alloc':allocation,
                    #'post':code_path+post_name})




####################################################################
## Converging channel (with high-order bathymetry) convergence study
####################################################################

# run variables

input_name = 'dgswe.inp'

bundle_flag = False          # bundle runs with same number of processors into same submission script
                             # 'rdirec' needs to be the same for each bundle of runs
processors = ['24','24','48','96']
prep_time = '00:20:00'
run_time = ['06:00:00','06:00:00','06:00:00','06:00:00']
max_proc = 500

allocation = 'TG-DMS080016N'

run_queue = 'zas'
prep_queue = 'zas'


exe_name = 'dgswe_mpi'
prep_name = 'dgprep'
post_name = 'dgpost'

grid_names = ['converge1_dble','converge2_dble','converge3_dble','converge4_dble']
p_orders = ['1','2','3']
ctp_orders = ['2','2','3']
hbp_orders = ['1','2','3']
rk_types = ['22','33','45']
timesteps = [['.5d0'   ,'.25d0'   ,'.125d0'],
             ['.25d0'  ,'.125d0'  ,'.0625d0'],
             ['.125d0' ,'.0625d0' ,'.03125d0'],
             ['.0625d0','.03125d0','.015625d0']]
#timesteps = ['.5d0','.25d0','.125d0']
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
run_path = '/home2/sbrus/dgswe_converge_curve_rimls9/'
code_path = '/home2/sbrus/dgswe_converge_curve_rimls9/code/'
grid_path = '/home2/sbrus/dgswe_converge_curve_rimls9/grids/'

# set up cases list
cases = []
for k,grid in enumerate(grid_names):
  procs = processors[k]
  for i,p in enumerate(p_orders):
    ctp = ctp_orders[i]
    dt = timesteps[k][i]
    rk = rk_types[i]
    rtime = run_time[i]
    for j in range(0,i+1):
      hbp = str(j+1)
      directory_name = run_path + grid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/' + 'hbp'+hbp+'/'
      cases.append({'input':directory_name+input_name,
	            'mesh':grid_path+grid,
                    'bathy':grid_path+grid+'_hbp'+hbp+'.hb',  
	            
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
                    'proc':procs,
                    'exe':code_path+exe_name,
                    'rtime':rtime,
                    'rqueue':run_queue.lower(),
                    
                    'prep':code_path+prep_name,
                    'ptime':prep_time,
                    'pqueue':prep_queue.lower(),
                    'alloc':allocation,
                    'post':code_path+post_name})

# Set up error input file
error = []
for i,p in enumerate(p_orders):
  ctp = ctp_orders[i]
  for j in range(0,i+1):
    hbp = str(j+1)
    for k in range(0,len(grid_names)-1):
      cgrid = grid_names[k]
      fgrid = grid_names[k+1]
      cdt = timesteps[k][i]
      fdt = timesteps[k+1][i]

      csol_direc = run_path + cgrid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/' + 'hbp'+hbp+'/'
      fsol_direc = run_path + fgrid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/' + 'hbp'+hbp+'/'

      error.append({'value':'!'+grid_path+cgrid+'.grd'         , 'comment':'! coarse grid file                                       \n'})
      error.append({'value':'!'+csol_direc                     , 'comment':'! coarse output directory                                \n'})
      error.append({'value':'!'+p                              , 'comment':'! p - coarse polynomial order                            \n'})
      error.append({'value':'!'+ctp                            , 'comment':'! ctp - coarse parametric coordinate transformation order\n'})
      error.append({'value':'!'+cdt                            , 'comment':'! dt - coarse timestep                                   \n'})
      error.append({'value':'!'+grid_path+fgrid+'.grd'         , 'comment':'! fine grid file                                         \n'})
      error.append({'value':'!'+fsol_direc                     , 'comment':'! fine output directory                                  \n'})
      error.append({'value':'!'+p                              , 'comment':'! p - fine polynomial order                              \n'})
      error.append({'value':'!'+ctp                            , 'comment':'! ctp - fine parametric coordinate transformation order  \n'})
      error.append({'value':'!'+fdt                            , 'comment':'! dt - fine timestep                                     \n'})
      error.append({'value':'!'+final_time                     , 'comment':'! tf - final time (days)                                 \n'})
      error.append({'value':'!'+num_snaps                      , 'comment':'! lines - lines in output file                           \n'})
      error.append({'value':'!'+grid_path+grid_names[0]+'.grd' , 'comment':'! coarsest grid file                                     \n'})
      error.append({'value':'!'+ctp                            , 'comment':'! coarsest grid ctp                                      \n'})
      error.append({'value':''                                 , 'comment':'                                                         \n'})

# Set up rimls imput file
rimls = []
r = '1.5d0'
sigma_n = '1.5d0'
for i,p in enumerate(p_orders):
  for k,grid in enumerate(grid_names):
    dt = timesteps[k][i]

    rimls.append({'value':'!'+grid_path+'converge4_bath_dble.grd' , 'comment':'! base grid - used to determine the rimls surface               \n'})
    rimls.append({'value':'!'+grid_path+grid+'.grd'               , 'comment':'! eval grid - used to determine rimls surface evaluation points \n'})
    rimls.append({'value':'!'+p                                   , 'comment':'! ctp - parametric coordinate transformation order              \n'})
    rimls.append({'value':'!'+'1d0'                               , 'comment':'! Erad - radius of Earth                                        \n'})
    rimls.append({'value':'!'+'0d0,0d0'                           , 'comment':'! lambda0,phi0 - center of CPP coordinate system                \n'})
    rimls.append({'value':'!'+r                                   , 'comment':'! r - muliplier for search radius (1.5 - 4.0)                   \n'})
    rimls.append({'value':'!'+sigma_n                             , 'comment':'! sigma_n - smoothing parameter (0.5 - 1.5)                     \n'})
    rimls.append({'value':'!'+'./'                                , 'comment':'! output directory                                              \n'})
    rimls.append({'value':''                                      , 'comment':'                                                                \n'})



                    
                    
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





