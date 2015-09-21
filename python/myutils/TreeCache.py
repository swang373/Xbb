from __future__ import print_function
import os,sys,subprocess,hashlib
import ROOT
from samplesclass import Sample


def trim_treeMT(myinput):
            ( myoptions, sample) = myinput
            (sampleList,doCache,tmpPath,cutList,hashDict,minCut,path) = myoptions
            print("myobj.__tmpPath:"+tmpPath)
            theName = sample.name
            print('Reading sample <<<< %s' %sample)
            source = '%s/%s' %( path,sample.get_path)
            checksum =  TreeCache.get_checksum(source)
            theHash = hashlib.sha224('%s_s%s_%s' %(sample,checksum, minCut)).hexdigest()
    #         myobj.__hashDict[theName] = theHash
            tmpSource = '%s/tmp_%s.root'%( tmpPath,theHash)
#            print (' doCache', doCache,' file_exists(tmpSource)', TreeCache.file_exists(tmpSource))
            if  doCache and  TreeCache.file_exists(tmpSource):
#                print('sample',theName,'skipped, filename=',tmpSource)
                return (theName,theHash)
#            print ('trying to create',tmpSource)
            output = ROOT.TFile.Open(tmpSource,'create')
#            print ('reading',source)
            input = ROOT.TFile.Open(source,'read')
            output.cd()
            tree = input.Get(sample.tree)
            if not type(tree) is ROOT.TTree:
                print("ERRORE!!")
                print(type(tree))
            # CountWithPU = input.Get("CountWithPU")
            # CountWithPU2011B = input.Get("CountWithPU2011B")
            # sample.count_with_PU = CountWithPU.GetBinContent(1) 
            # sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1) 
            try:
                CountWithPU = input.Get("CountWithPU")
                CountWithPU2011B = input.Get("CountWithPU2011B")
                sample.count_with_PU = CountWithPU.GetBinContent(1) 
                sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1)
            except:
#                print('WARNING: No Count with PU histograms available. Using 1.')
                sample.count_with_PU = 1.
                sample.count_with_PU2011B = 1.
            input.cd()
            obj = ROOT.TObject
            for key in ROOT.gDirectory.GetListOfKeys():
                input.cd()
                obj = key.ReadObj()
                if obj.GetName() == 'tree':
                    continue
                output.cd()
                obj.Write(key.GetName())
            output.cd()
            theCut = minCut
            if sample.subsample:
                theCut += '& (%s)' %(sample.subcut)
            cuttedTree=tree.CopyTree(theCut)
            cuttedTree.Write()
            output.Write()
            input.Close()
            del input
            output.Close()
    #        tmpSourceFile = ROOT.TFile.Open(tmpSource,'read')
    #        if tmpSourceFile.IsZombie():
    #            print("@ERROR: Zombie file")
            del output
            return (theName,theHash)

class TreeCache:
    def __init__(self, cutList, sampleList, path, config):
        ROOT.gROOT.SetBatch(True)
        self.path = path
        print("Init path",path," sampleList",sampleList)
        self._cutList = []
        for cut in cutList:
            self._cutList.append('(%s)'%cut.replace(' ',''))
        try:
            self.__tmpPath = os.environ["TMPDIR"]
        except KeyError:
            print("\x1b[32;5m %s \x1b[0m" %open('%s/data/vhbb.txt' %config.get('Directories','vhbbpath')).read())
            print("\x1b[31;5;1m\n\t>>> %s: Please set your TMPDIR and try again... <<<\n\x1b[0m" %os.getlogin())
            sys.exit(-1)

        self.__doCache = True
        if config.has_option('Directories','tmpSamples'):
            self.__tmpPath = config.get('Directories','tmpSamples')
        self.__hashDict = {}
        self.minCut = None
        self.__find_min_cut()
        self.__sampleList = sampleList
        print('\n\t>>> Caching FILES <<<\n')
        self.__cache_samples()
        
    def putOptions(self):
        return (self.__sampleList,self.__doCache,self.__tmpPath,self._cutList,self.__hashDict,self.minCut,self.path)
    
    def _mkdir_recursive(self, path):
        sub_path = os.path.dirname(path)
        if not os.path.exists(sub_path):
            self._mkdir_recursive(sub_path)
        if not os.path.exists(path):
            os.mkdir(path)

    def __find_min_cut(self):
        effective_cuts = []
        for cut in self._cutList:
            if not cut in effective_cuts:
                effective_cuts.append(cut)
        self._cutList = effective_cuts
        self.minCut = '||'.join(self._cutList)

    def __trim_tree(self, sample):
        theName = sample.name
        print('Reading sample <<<< %s' %sample)
        source = '%s/%s' %(self.path,sample.get_path)
        checksum = self.get_checksum(source)
        theHash = hashlib.sha224('%s_s%s_%s' %(sample,checksum,self.minCut)).hexdigest()
        self.__hashDict[theName] = theHash
        tmpSource = '%s/tmp_%s.root'%(self.__tmpPath,theHash)
        print ('self.__doCache',self.__doCache,'self.file_exists(tmpSource)',self.file_exists(tmpSource))
        if self.__doCache and self.file_exists(tmpSource):
            print('sample',theName,'skipped, filename=',tmpSource)
            return
        print ('trying to create',tmpSource)
        output = ROOT.TFile.Open(tmpSource,'create')
        print ('reading',source)
        input = ROOT.TFile.Open(source,'read')
        output.cd()
        tree = input.Get(sample.tree)
        # CountWithPU = input.Get("CountWithPU")
        # CountWithPU2011B = input.Get("CountWithPU2011B")
        # sample.count_with_PU = CountWithPU.GetBinContent(1) 
        # sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1) 
        try:
            CountWithPU = input.Get("CountWithPU")
            CountWithPU2011B = input.Get("CountWithPU2011B")
            sample.count_with_PU = CountWithPU.GetBinContent(1) 
            sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1)
        except:
            print('WARNING: No Count with PU histograms available. Using 1.')
            sample.count_with_PU = 1.
            sample.count_with_PU2011B = 1.
        input.cd()
        obj = ROOT.TObject
        for key in ROOT.gDirectory.GetListOfKeys():
            input.cd()
            obj = key.ReadObj()
            if obj.GetName() == 'tree':
                continue
            output.cd()
            obj.Write(key.GetName())
        output.cd()
        theCut = self.minCut
        if sample.subsample:
            theCut += '& (%s)' %(sample.subcut)
        cuttedTree=tree.CopyTree(theCut)
        cuttedTree.Write()
        output.Write()
        input.Close()
        del input
        output.Close()
#        tmpSourceFile = ROOT.TFile.Open(tmpSource,'read')
#        if tmpSourceFile.IsZombie():
#            print("@ERROR: Zombie file")
        del output


    ### OLD VERSION ###
#    def __cache_samples(self):
#        for job in self.__sampleList:
#            self.__trim_tree(job)

    ### MULTI-THREADING VERSION ###
    def __cache_samples(self):
        import copy
        multiprocess=16
        if multiprocess>0:
            from multiprocessing import Pool
            p = Pool(multiprocess)
#            import pathos.multiprocessing as mp
#            p = mp.ProcessingPool(multiprocess)
            myinputs = []
            for job in self.__sampleList:
                myoptions = self.putOptions()
                myinputs.append((myoptions,job))
                
            outputs = p.map(trim_treeMT, myinputs)
            for output in outputs:
                (theName,theHash) = output
                self.__hashDict[theName]=theHash
        else:
            for job in self.__sampleList:
                self.__trim_tree(job)

    def get_tree(self, sample, cut):
        input = ROOT.TFile.Open('%s/tmp_%s.root'%(self.__tmpPath,self.__hashDict[sample.name]),'read')
        print ('Opening %s/tmp_%s.root'%(self.__tmpPath,self.__hashDict[sample.name]))
        tree = input.Get(sample.tree)
        # CountWithPU = input.Get("CountWithPU")
        # CountWithPU2011B = input.Get("CountWithPU2011B")
        # sample.count_with_PU = CountWithPU.GetBinContent(1) 
        # sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1) 
        try:
            CountWithPU = input.Get("CountWithPU")
            CountWithPU2011B = input.Get("CountWithPU2011B")
            sample.count_with_PU = CountWithPU.GetBinContent(1) 
            sample.count_with_PU2011B = CountWithPU2011B.GetBinContent(1) 
        except:
            print('WARNING: No Count with PU histograms available. Using 1.')
            sample.count_with_PU = 1.
            sample.count_with_PU2011B = 1.
        if sample.subsample:
            cut += '& (%s)' %(sample.subcut)
        ROOT.gROOT.cd()
        cuttedTree=tree.CopyTree(cut)
        # cuttedTree.SetDirectory(0)
        input.Close()
        del input
        del tree
        return cuttedTree

    @staticmethod
    def get_slc_version():
        command = 'uname -a'
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
        lines = p.stdout.readlines()
        line = lines[0].split()[2]
        if 'el5' in line:
            return 'SLC5'
        elif 'el6' in line:
            return 'SLC6'
        else:
            sys.exit(-1)

    @staticmethod
    def get_scale(sample, config, lumi = None):
#        print float(sample.lumi)
        anaTag=config.get('Analysis','tag')
        theScale = 1. ##FIXME
#        if not lumi:
#            lumi = float(sample.lumi)
#        if anaTag == '7TeV':
#            theScale = lumi*sample.xsec*sample.sf/(0.46502*sample.count_with_PU+0.53498*sample.count_with_PU2011B)
#        elif anaTag == '8TeV':
#            theScale = lumi*sample.xsec*sample.sf/(sample.count_with_PU)
        return theScale

    @staticmethod
    def get_checksum(file):
        if 'gsidcap://t3se01.psi.ch:22128' in file:
            srmPath = 'srm://t3se01.psi.ch:8443/srm/managerv2?SFN='
            if TreeCache.get_slc_version() == 'SLC5':
                command = 'lcg-ls -b -D srmv2 -l %s' %file.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
                lines = p.stdout.readlines()
                if any('No such' in line for line in lines):
                    print('File not found')
                    print(command)
                line = lines[1].replace('\t* Checksum: ','')
                checksum = line.replace(' (adler32)\n','')
            elif TreeCache.get_slc_version() == 'SLC6':
                command = 'srmls -l %s' %file.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
                lines = p.stdout.readlines()
                if any('does not exist' in line for line in lines):
                    print('File not found')
                    print(command)
                checksum = lines[6].replace('- Checksum value:','')
                checksum = checksum.strip()
                #srmPath = 'srm://t3se01.psi.ch'
                #command = 'gfal-sum %s ADLER32' %file.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
                #print(command)
                #p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
                #lines = p.stdout.readlines()
                #if any('No such' in line for line in lines):
                #    print('File not found')
                #    print(command)
                #checksum = lines[0].split()[1]

        else:
            command = 'md5sumi %s' %file
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
            lines = p.stdout.readlines()
            checksum = lines[0]
        return checksum
    
    @staticmethod
    def file_exists(file):
        file_dummy = file
        srmPath = 'srm://t3se01.psi.ch:8443/srm/managerv2?SFN='
        file_dummy = file_dummy.replace('root://t3dcachedb03.psi.ch:1094/','')
        file_dummy = file_dummy.replace('srm://t3se01.psi.ch:8443/srm/managerv2?SFN=','')
        print('trying to check if exists:',file_dummy)
        # if 'gsidcap' or 'srm' in file_dummy:
            # if TreeCache.get_slc_version() == 'SLC5':
              # command = 'lcg-ls %s' %file_dummy.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
              # error_msg = 'No such file or directory'
            # elif TreeCache.get_slc_version() == 'SLC6':
              # command = 'lcg-ls %s' %file_dummy.replace('gsidcap://t3se01.psi.ch:22128/','%s/'%srmPath)
              # # print ('using command',command)
              # error_msg = 'does not exists'
              
            # p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True)
            # line = p.stdout.readline()
            # return not error_msg in line
              
        # else:
        print('os.path.exists(',file_dummy,')',os.path.exists(file_dummy))
        return os.path.exists(file_dummy)


