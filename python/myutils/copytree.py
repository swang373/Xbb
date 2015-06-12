import ROOT,sys,os,subprocess
from printcolor import printc
        
def copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,Acut):

    print "##### COPY TREE - BEGIN ######"
    print "Input File : %s/%s%s.root " %(pathIN,prefix,file)
    print "Output File : %s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file)
        
    input = ROOT.TFile.Open("%s/%s%s.root" %(pathIN,prefix,file),'read')
    print ("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'recreate')
    del_protocol = pathOUT
    del_protocol = del_protocol.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    del_protocol = del_protocol.replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    del_protocol = del_protocol.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    command = 'srmrm %s/%s%s%s.root' %(del_protocol,newprefix,Aprefix,file)
    print(command)
    subprocess.call([command], shell=True)    
    output = ROOT.TFile.Open("%s/%s%s%s.root" %(pathOUT,newprefix,Aprefix,file),'create')

    input.ls()
    input.cd()
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
