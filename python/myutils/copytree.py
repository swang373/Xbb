import ROOT,sys,os,subprocess
from printcolor import printc
import os 

def copytree(pathIN,pathOUT,prefix,newprefix,file,Aprefix,Acut):
    from os import walk
    dirpath = ""
    filename = ""
    filenames = []
    print "##### COPY TREE - BEGIN ######"
    for (dirpath_, dirnames, filenames_) in walk(pathIN+'/'+file):
        for filename_ in filenames_:
            if 'root' in filename_ and not 'failed' in dirpath_:
                dirpath = dirpath_
                filename = filename_
                filenames = filenames_
                break
        if len(filenames)>0: break
    
    if dirpath == "":
        print "No .root files found in ",pathIN+'/'+file
        return
    
    pathIN = dirpath
    
    FileList = ROOT.TList();
    for filename in filenames:
        inputFile = '%s/%s ' %(pathIN,filename)
        input = ROOT.TFile.Open(inputFile,'read')
        outputFolder = "%s/%s/" %(pathOUT,file)
        outputFile = "%s/%s/%s" %(pathOUT,file,filename)
        try:
            os.mkdir(outputFolder)
        except:
            pass
        del_protocol = pathOUT
        del_protocol = del_protocol.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        del_protocol = del_protocol.replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        del_protocol = del_protocol.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        print("cutting ",inputFile," ---> ",outputFile)
        if os.path.isfile(outputFile): 
            command = 'rm %s' %(outputFile)
            print(command)
            subprocess.call([command], shell=True)
        
        output = ROOT.TFile.Open(outputFile,'create')
        print "Writing file:",outputFile

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
