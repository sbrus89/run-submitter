import run_cases

def check_cases(cases):
  
  for case in cases:
    if int(case['proc']) > run_cases.max_proc:
      print 'Error number of processors exceeds max allowed'
      SystemExit(0) 


  


