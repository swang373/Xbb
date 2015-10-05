import ROOT,sys,os,subprocess
from printcolor import printc

def copytree(pathIN,pathOUT,prefix,newprefix,folderName,Aprefix,Acut,whereToLaunch):
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
    print 'start copytree.py'
    print (pathIN,pathOUT,prefix,newprefix,folderName,Aprefix,Acut)
    from os import walk
    dirpath = ""
    filename = ""
    filenames = []
    folder_prefix = ''
    print "##### COPY TREE - BEGIN ######"
    if('pisa' in whereToLaunch):
      for (dirpath_, dirnames, filenames_) in walk(pathIN+'/'+folderName):
    else:
      FOLDER = pathIN+'/'+folderName
      if FOLDER.startswith('dcap://t3se01.psi.ch:22125'):
          FOLDER = FOLDER.replace('dcap://t3se01.psi.ch:22125','')
          folder_prefix = 'dcap://t3se01.psi.ch:22125'
      for (dirpath_, dirnames, filenames_) in walk(FOLDER):
        for filename_ in filenames_:
            if 'root' in filename_ and not 'failed' in dirpath_:
                dirpath = dirpath_
                filename = filename_
                filenames = filenames_
                break
        if len(filenames)>0: break

    if dirpath == "":
        print "No .root files found in ",pathIN+'/'+folderName
        return

    if('pisa' in whereToLaunch):
      pathIN = dirpath
    else:
      pathIN = folder_prefix + dirpath

    #pathIN = dirpath

#    FileList = ROOT.TList();
    for filename in filenames:
        inputFile = '%s/%s ' %(pathIN,filename)
        input = ROOT.TFile.Open(inputFile,'read')
        outputFolder = "%s/%s/" %(pathOUT,folderName)
        outputFile = "%s/%s/%s" %(pathOUT,folderName,filename)
        #Create the ouput folder if not existing
        mkdir_protocol = outputFolder.replace('root://t3dcachedb03.psi.ch:1094/','')
        _output_folder = ''
        for _folder in mkdir_protocol.split('/'):
            #if mkdir_protocol.split('/').index(_folder) < 3: continue
            _output_folder += '/'+_folder
            if os.path.exists(_output_folder): print 'exists'
            else: 
                command = 'srmmkdir srm://t3se01.psi.ch/' + _output_folder
                subprocess.call([command], shell = True)
            if os.path.exists(_output_folder): print 'Folder', _output_folder, 'sucessfully created'


        try:
            os.mkdir(outputFolder)
        except:
            pass
        del_protocol = outputFile 
        del_protocol = del_protocol.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        del_protocol = del_protocol.replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        del_protocol = del_protocol.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        print "cutting ",inputFile," ---> ",outputFile
        if os.path.isfile(del_protocol.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=','')): 
            print 'File', del_protocol.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=',''), 'already exists.\n Gonna delete it.'
            #command = 'rm %s' %(outputFile)
            command = 'srmrm %s' %(del_protocol)
            print(command)
            subprocess.call([command], shell=True)
        else: print 'FALSE'
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
        print '\n\t copy file: %s with cut: %s' %(folderName,Acut)
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

    merged = pathOUT+'/'+newprefix+folderName+".root "

    del_merged = merged
    del_merged = del_merged.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    del_merged = del_merged.replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    del_merged = del_merged.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
    command = 'srmrm %s' %(del_merged)
    print command
    subprocess.call([command], shell = True)
    #else: print 'Does not exist'
    t = ROOT.TFileMerger()
    t.OutputFile(pathOUT+'/'+newprefix+folderName+".root ", "CREATE")
    print 'outputFolder is', outputFolder 
    for file in os.listdir(outputFolder.replace('root://t3dcachedb03.psi.ch:1094','')):
        print 'file is', outputFolder+file
        if file.startswith('tree'):
            t.AddFile(outputFolder+file)
    t.Merge()
    print "##### COPY TREE - END ######"
