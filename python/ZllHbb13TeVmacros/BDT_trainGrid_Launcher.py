import os,sys,subprocess

# steering parameters
BDT_list = ['ZllBDT_highVpt']
max_running_processes = 8
waiting_time_before_retry = 60 # in seconds

##################################################
# use appropriate tag according to $USER
input_folder = 'GaelZllHbb13TeV'
user = subprocess.Popen("echo $USER", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
if 'perrozzi' in user:
    input_folder = 'LucaZllHbb13TeV'
    print 'ciao perrozzi'
##################################################

# create log folder if needed
if not os.path.isdir("./logs"): os.system("mkdir logs")

# loop over bdt points
for BDT_point in BDT_list:
    # get the number of running processes
    command = 'ps aux | grep '+user.strip("\n")+' | grep train | grep runAll.sh | wc -l'
    print 'before running',BDT_point,'checking running trainings with the string',command
    running_trainings = int(int(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read())/2)
    print 'running_trainings are',running_trainings
    # submit a bdt point
    subprocess.Popen('cd ..; sh runAll.sh '+BDT_point+' '+input_folder+' train 2>&1 > ZllHbb13TeVmacros/logs/'+BDT_point+'.log; cd - &', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait if too many bdt points are running
    while running_trainings > max_running_processes:
        running_trainings = int(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read())
        print 'running_trainings',running_trainings,'waiting',time,'seconds before to retry'
        os.system('sleep '+str(waiting_time_before_retry))

