import os,sys,subprocess

#BDT_list = ['ZllBDT_highVpt']
BDT_list = ['BDT_SCAN_NTrees_200_nEventsMin_200_Zmm_highVpt',
    'BDT_SCAN_NTrees_200_nEventsMin_300_Zmm_highVpt',
    'BDT_SCAN_NTrees_300_nEventsMin_200_Zmm_highVpt',
    'BDT_SCAN_NTrees_300_nEventsMin_300_Zmm_highVpt',
    'BDT_SCAN_NTrees_200_nEventsMin_200_Zmm_highVpt',
    'BDT_SCAN_NTrees_200_nEventsMin_300_Zmm_highVpt',
    'BDT_SCAN_NTrees_300_nEventsMin_200_Zmm_highVpt',
    'BDT_SCAN_NTrees_300_nEventsMin_300_Zmm_highVpt']


max_running_processes = 6
waiting_time_before_retry = 60 # in seconds

##################################################
input_folder = 'GaelZllHbb13TeV'
user = subprocess.Popen("echo $USER", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
if 'perrozzi' in user:
    input_folder = 'LucaZllHbb13TeV'
    print 'ciao perrozzi'
##################################################

for BDT_point in BDT_list:
    command = 'ps aux | grep '+user.strip("\n")+' | grep train | grep runAll.sh | wc -l'
    print 'before running',BDT_point,'checking running trainings with the string',command
    running_trainings = int(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read())
    print 'running_trainings are',running_trainings
    subprocess.Popen('cd ..; sh runAll.sh '+BDT_point+' '+input_folder+' train 2>&1 > /dev/null; cd - &', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while running_trainings > max_running_processes:
        running_trainings = int(subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read())
        print 'running_trainings',running_trainings,'waiting',waiting_time_before_retry,'seconds before to retry'
        os.system('sleep '+str(waiting_time_before_retry))

