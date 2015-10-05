import ROOT,sys,os,subprocess
from printcolor import printc

def copytree(pathIN,pathOUT,prefix,newprefix,folderName,Aprefix,Acut):
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
    print (pathIN,pathOUT,prefix,newprefix,folderName,Aprefix,Acut)
    from os import walk
    dirpath = ""
    filename = ""
    filenames = []
    FOLDER = pathIN+'/'+folderName
    folder_prefix = ''
    if FOLDER.startswith('dcap://t3se01.psi.ch:22125'):
        FOLDER = FOLDER.replace('dcap://t3se01.psi.ch:22125','')
        folder_prefix = 'dcap://t3se01.psi.ch:22125'
    print "##### COPY TREE - BEGIN ######"
    print 'pathIN+foldername is', pathIN+'/'+folderName
    print 'FOLDER is', FOLDER
    for (dirpath_, dirnames, filenames_) in walk(FOLDER):
        print 'dirpath is', dirpath_
        print 'dirnames is', dirnames
        print 'filenames is', filenames_ 
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

    print 'dirpath is', dirpath
    pathIN = folder_prefix + dirpath
    print 'pathIN is', pathIN

    #pathIN = dirpath

    print 'pathIN is', pathIN

#    FileList = ROOT.TList();
    for filename in filenames:
        inputFile = '%s/%s ' %(pathIN,filename)
        input = ROOT.TFile.Open(inputFile,'read')
        outputFolder = "%s/%s/" %(pathOUT,folderName)
        outputFile = "%s/%s/%s" %(pathOUT,folderName,filename)
        print 'outputFile is', outputFile
        #Create the ouput folder if not existing
        print 'outputFolder is', outputFolder
        #mkdir_protocol = outputFolder.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch/')
        mkdir_protocol = outputFolder.replace('root://t3dcachedb03.psi.ch:1094/','')
        _output_folder = ''
        print 'split is', mkdir_protocol.split('/') 
        for _folder in mkdir_protocol.split('/'):
            print '_folder is', _folder
            #if mkdir_protocol.split('/').index(_folder) < 3: continue
            _output_folder += '/'+_folder
            print '_output_folder is', _output_folder
            if os.path.exists(_output_folder): print 'exists'
            else: 
                print 'Folder', _output_folder, 'doesn\'t exist\n. Creating it now'
                command = 'srmmkdir srm://t3se01.psi.ch/' + _output_folder
                subprocess.call([command], shell = True)
            if os.path.exists(_output_folder): print 'Folder', _output_folder, 'sucessfully created'


        try:
            os.mkdir(outputFolder)
        except:
            pass
        del_protocol = outputFile 
        print 'del_protocol is', del_protocol 
        del_protocol = del_protocol.replace('gsidcap://t3se01.psi.ch:22128/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        del_protocol = del_protocol.replace('dcap://t3se01.psi.ch:22125/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        del_protocol = del_protocol.replace('root://t3dcachedb03.psi.ch:1094/','srm://t3se01.psi.ch:8443/srm/managerv2?SFN=')
        print 'del_protocol is', del_protocol 
        print "cutting ",inputFile," ---> ",outputFile
        print 'path used to check if the file exists', del_protocol.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=','')
        if os.path.isfile(del_protocol.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=','')): 
            print 'File', del_protocol.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=',''), 'already exists.\n Gonna delete it.'
            #command = 'rm %s' %(outputFile)
            command = 'srmrm %s' %(del_protocol)
            print(command)
            subprocess.call([command], shell=True)
        else: print 'FALSE'
        print 'DEBUG1'
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

    print "##### COPY TREE - END ######"
    merged = pathOUT+'/'+newprefix+folderName+".root "

    #if os.path.exists(merged.replace('root://t3dcachedb03.psi.ch:1094/','')): 
        #if os.path.exists('/pnfs/psi.ch/cms/trivcat/store/user/gaperrin/VHbb/ZllHbb13TeV_V13/prep/ZmmH.BestCSV.heppy.DYJetsToLL_M-50_HT-100to200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8.root'):
    print merged, 'exists'
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
