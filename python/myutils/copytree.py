import ROOT,sys,os,subprocess
from printcolor import printc

        
def copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,Acut):
    ''' 
    List of variables
    pathIN: path of the input file containing the data
    pathOUT: path of the output files 
    prefix: "prefix" variable from "samples_nosplit.cfg" 
    newprefix: "newprefix" variable from "samples_nosplit.cfg" 
    file: sample header (as DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball)
    Aprefix: empty string ''
    Acut: the sample cut as defined in "samples_nosplit.cfg"
    '''

    #!!print input parameters
    print "##### COPY TREE - BEGIN ######"
    print "Input File : %s/%s%s.root " %(pathIN,prefix,file)
    print "Output File : %s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file)
        
    #!! get the input file, remove the previous output files 
    input = ROOT.TFile.Open("%s/%s%s.root" %(pathIN,prefix,file),'read')
    print ("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'recreate')
    del_protocol = pathOUT
    del_protocol = del_protocol.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    del_protocol = del_protocol.replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    del_protocol = del_protocol.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    # RECURSIVELY CREATE REMOTE FOLDER ON PSI SE, but only up to 3 new levels
    mkdir_command = del_protocol.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=','srm://t3se01.psi.ch/')
    mkdir_command1 = mkdir_command.rsplit('/',1)[0]
    mkdir_command2 = mkdir_command1.rsplit('/',1)[0]
    mkdir_command3 = mkdir_command2.rsplit('/',1)[0]
    my_user = os.popen("whoami").read().strip('\n').strip('\r')+'/'
    if my_user in mkdir_command3:
      print 'mkdir_command3',mkdir_command3
      subprocess.call([mkdir_command3], shell=True)# delete the files already created ?     
    if my_user in mkdir_command2:
      print 'mkdir_command2',mkdir_command2
      subprocess.call([mkdir_command2], shell=True)# delete the files already created ?     
    if my_user in mkdir_command1:
      print 'mkdir_command1',mkdir_command1
      subprocess.call([mkdir_command1], shell=True)# delete the files already created ?     
    if my_user in mkdir_command:
      print 'mkdir_command',mkdir_command
      subprocess.call([mkdir_command], shell=True)# delete the files already created ?     
    
    command = 'srmrm %s/%s%s%s.root' %(del_protocol,newprefix,Aprefix,file)# command to delete previous files ?
    print(command)
    subprocess.call([command], shell=True)# delete the files already created ?     
    output = ROOT.TFile.Open("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'create')
    input.ls()
    input.cd()

    #read the content of the ROOT file 
    #copy the directorys of the tree
    obj = ROOT.TObject
    for key in ROOT.gDirectory.GetListOfKeys():
        input.cd()
        obj = key.ReadObj()
        #print obj.GetName()
        if obj.GetName() == 'tree':
            continue
        output.cd()
        #print key.GetName()
        obj.Write(key.GetName())

    #copy the tree with the additional cuts
    inputTree = input.Get("tree")
    nEntries = inputTree.GetEntries()
    output.cd()
    print '\n\t copy file: %s with cut: %s' %(file,Acut)
    outputTree = inputTree.CopyTree(Acut)
    kEntries = outputTree.GetEntries()
    printc('blue','',"\t before cuts\t %s" %nEntries)
    printc('green','',"\t survived\t %s" %kEntries)
    outputTree.AutoSave()
    output.ls()
    print "Writing output file"
    output.Write()
    print "Closing output file"
    output.Close()
    print "Closing input file"
    input.Close()

    print "##### COPY TREE - END ######"
