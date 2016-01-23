import os
import subprocess
import glob
import sys

grid_names = ['converge1_dble','converge2_dble','converge3_dble','converge4_dble']
p_orders = ['1','2','3']
ctp_orders = ['2','2','3']
hbp_orders = ['1','2','3']
CYAN = '\033[36m'
RED = '\033[31m'
MAGENTA = '\033[35m'
ENDC = '\033[0m'

move_to_path = '/home2/sbrus/dgswe_converge_curve/'


print " "
case_number =  raw_input("Enter case number: ")

case_path  = '/scratch365/sbrus/dgswe_converge_curve/rimls' + case_number + "/"
if not os.path.exists(case_path):
  print RED + "Directory does not exist" + ENDC
  raise SystemExit(0)
else:
  print "directory exists: " + case_path
  print " "



print "determining current size... ", 
sys.stdout.flush()
total_before = subprocess.Popen('du -ch '+case_path+ ' | grep total' , stdout=subprocess.PIPE, shell=True).communicate()[0]
print "done"



for k,grid in enumerate(grid_names):
  for i,p in enumerate(p_orders):
    ctp = ctp_orders[i]
    for j in range(0,i+1):
      hbp = str(j+1)
      direc = case_path + grid+'/' + 'p'+p+'/' + 'ctp'+ctp+'/' + 'hbp'+hbp+'/'

      print " "
      print CYAN + "cleaning: " + direc + ENDC
     
      os.chdir(direc)
      if not os.path.exists('output'):
        print "  making output directory... ",
        os.makedirs('output')
        print "done"

      print "  moving solution files to temp directory... ",      
      sys.stdout.flush()
      subprocess.Popen('mv solution_*.d output'  , stdout=subprocess.PIPE, shell=True).communicate()[0]     
      print "done"

      print "  removing extra *.d files... ",
      sys.stdout.flush()
      subprocess.Popen('rm *.d'                  , stdout=subprocess.PIPE, shell=True).communicate()[0]
      print "done"

      print "  removing PE directories... ",
      sys.stdout.flush()
      subprocess.Popen('rm -r PE*'               , stdout=subprocess.PIPE, shell=True).communicate()[0]
      print "done"

      print "  moving solution files back to case directory... ",      
      sys.stdout.flush()
      subprocess.Popen('mv output/solution_*.d .', stdout=subprocess.PIPE, shell=True).communicate()[0]     
      print "done"

      print "  removing temp directory... ",       
      sys.stdout.flush()
      subprocess.Popen('rmdir output'            , stdout=subprocess.PIPE, shell=True).communicate()[0]
      print "done"	      

      if glob.glob('core.*'):
        print MAGENTA + "  run failure output found" + ENDC + ", removing... ",
        sys.stdout.flush()
        subprocess.Popen('rm core.*'             , stdout=subprocess.PIPE, shell=True).communicate()[0]
        print "done"
      


print " "

if os.path.exists(case_path+'bathy'):
  os.chdir(case_path+'bathy') 
  print "removing *.d files in bathy... ",
  sys.stdout.flush()
  subprocess.Popen('rm *.d'               , stdout=subprocess.PIPE ,shell=True)
  print "done"
else:
  print RED + "bathy directory does not exist" + ENDC


if os.path.exists(case_path+'rimls'):
  os.chdir(case_path+'rimls')
  print "removing *.d riles in rimls... ",
  sys.stdout.flush()
  subprocess.Popen('rm *.d'               , stdout=subprocess.PIPE ,shell=True)
  print "done"
else:
  print RED + "rimls directory does not exist" + ENDC


print " "
print "determining current size... ",
sys.stdout.flush()	      
total_after = subprocess.Popen('du -ch '+case_path+ ' | grep total' , stdout=subprocess.PIPE, shell=True).communicate()[0]
print "done"

print " " 
print " "
print "Size before ", total_before.split()[0]
print "Size after " , total_after.split()[0]
print " " 



print "moving case directory to home2... "
sys.stdout.flush()
subprocess.Popen('mv ' + case_path + ' ' + move_to_path  , stdout=subprocess.PIPE, shell=True).communicate()[0]
print "done"

