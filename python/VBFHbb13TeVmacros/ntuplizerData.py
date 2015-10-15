import ROOT
from array import array

#maxEvents = 100000
#maxEvents = 10000
maxEvents = -1

def GetVariablesToFill(b1,b2,q1,q2):
    return ( abs(q1.Eta() - q2.Eta()), abs(b1.DeltaPhi(b2)), (q1+q2).M(), (b1+b2).M())

def SetVariable(tree,name,option='F',lenght=1):
    if option is 'F': arraytype='f'
    elif option is 'O': arraytype='i'
    elif option is 'I': arraytype='i'
    else:
        print 'option ',option,' not recognized.'
        return

    variable = array(arraytype,[0]*lenght)
    if lenght>1: name = name + '['+str(lenght)+']'
    tree.Branch(name,variable,name+'/'+option)
    return variable

def SortByEta(vect):
    vect.sort(key=lambda x: x.Eta(), reverse=True)

def SortByPt(vect):
    vect.sort(key=lambda x: x.Pt(), reverse=True)

def SortByCSV(vect):
    vect.sort(key=lambda x: x.csv, reverse=True)

def Sort(lorentzvectorswithcsv,method=''):
    (b1,b2,q1,q2) = [ROOT.TLorentzVector()]*4
    if len(lorentzvectorswithcsv)>=4:
        if method is '1BTagAndEta':

            SortByPt(lorentzvectorswithcsv)
            maxElementsPt = 4
            lorentzvectorswithcsv = lorentzvectorswithcsv[:maxElementsPt]
            SortByCSV(lorentzvectorswithcsv)
            b1 = lorentzvectorswithcsv[0]
            del lorentzvectorswithcsv[0]

            SortByEta(lorentzvectorswithcsv)
            q1 = lorentzvectorswithcsv[0]
            b2 = lorentzvectorswithcsv[1]
            q2 = lorentzvectorswithcsv[2]

        elif method is '2BTagAndPt':

            SortByPt(lorentzvectorswithcsv)
            maxElementsPt = 6
            lorentzvectorswithcsv = lorentzvectorswithcsv[:maxElementsPt]
            SortByCSV(lorentzvectorswithcsv)
            b1 = lorentzvectorswithcsv[0]
            b2 = lorentzvectorswithcsv[1]
            del lorentzvectorswithcsv[1]
            del lorentzvectorswithcsv[0]

            SortByPt(lorentzvectorswithcsv)
            q1 = lorentzvectorswithcsv[0]
            q2 = lorentzvectorswithcsv[1]

        elif method is 'Eta':

            SortByPt(lorentzvectorswithcsv)
            maxElementsPt = 4
            lorentzvectorswithcsv = lorentzvectorswithcsv[:maxElementsPt]
            SortByEta(lorentzvectorswithcsv)
            q1 = lorentzvectorswithcsv[0]
            b1 = lorentzvectorswithcsv[1]
            b2 = lorentzvectorswithcsv[2]
            q2 = lorentzvectorswithcsv[3]

        elif method is 'Gen':

            SortByPt(lorentzvectorswithcsv)
            for i,jet in enumerate(lorentzvectorswithcsv):
                if jet.mcMatchId==25 and jet.mcFlavour==5:
                    break

            b1_ = lorentzvectorswithcsv[i]
            del lorentzvectorswithcsv[i]

            for i,jet in enumerate(lorentzvectorswithcsv):
                if jet.mcMatchId==25 and jet.mcFlavour==-5:
                    break

            b2_ = lorentzvectorswithcsv[i]
            del lorentzvectorswithcsv[i]

            mjj = 0
            for i,jet in enumerate(lorentzvectorswithcsv):
                if jet.mcFlavour!=0 and jet.mcFlavour!=21 and (abs(jet.mcFlavour)<=2):
                    for j,jet2 in enumerate(lorentzvectorswithcsv):
                        if j>i and jet2.mcFlavour!=0 and jet2.mcFlavour!=21 and (abs(jet2.mcFlavour)<=2):
                            if (jet+jet2).M()>mjj:
                                mjj = (jet+jet2).M()
                                q1_ = jet
                                q2_ = jet2

            try:
                (b1,b2,q1,q2) = (b1_,b2_,q1_,q2_)
            except:
#                print "excption"
                pass

        else:
            print 'method:',method,' not found'
    else:
#        print 'less than 4 jets!'
        pass

    if b2.Pt()>b1.Pt(): (b1,b2) = (b2,b1)
    if q2.Pt()>q1.Pt(): (q1,q2) = (q2,q1)
    return (b1,b2,q1,q2)

tree = ROOT.TChain("tree")
tree.Add('/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV13/JetHT/VHBB_HEPPY_V13_JetHT__Run2015C-PromptReco-v1/151002_100932/0000/tree_*.root')
output = ROOT.TFile.Open('mytreeData.root','recreate')
output.cd()
nEntries = tree.GetEntries()
tree.SetBranchStatus('*',0)
tree.SetBranchStatus('nJet',1)
tree.SetBranchStatus('Jet_pt',1)
tree.SetBranchStatus('Jet_eta',1)
tree.SetBranchStatus('Jet_phi',1)
tree.SetBranchStatus('Jet_mass',1)
tree.SetBranchStatus('Jet_btagCSV',1)
#tree.SetBranchStatus('Jet_mcPt',1)
#tree.SetBranchStatus('Jet_mcFlavour',1)
#tree.SetBranchStatus('Jet_mcMatchId',1)
tree.SetBranchStatus('HLT_*VBF*',1)
tree.SetBranchStatus('HLT_*Jet*',1)
tree.SetBranchStatus('*json*',1)
newtree = tree.CloneTree(0)

Detaqq_eta = SetVariable(newtree,'Detaqq_eta')
Dphibb_eta = SetVariable(newtree,'Dphibb_eta')
Mqq_eta = SetVariable(newtree,'Mqq_eta')
Mbb_eta = SetVariable(newtree,'Mbb_eta')

Detaqq_1b = SetVariable(newtree,'Detaqq_1b')
Dphibb_1b = SetVariable(newtree,'Dphibb_1b')
Mqq_1b = SetVariable(newtree,'Mqq_1b')
Mbb_1b = SetVariable(newtree,'Mbb_1b')

Detaqq_2b = SetVariable(newtree,'Detaqq_2b')
Dphibb_2b = SetVariable(newtree,'Dphibb_2b')
Mqq_2b = SetVariable(newtree,'Mqq_2b')
Mbb_2b = SetVariable(newtree,'Mbb_2b')

Detaqq_gen = SetVariable(newtree,'Detaqq_gen')
Dphibb_gen = SetVariable(newtree,'Dphibb_gen')
Mqq_gen = SetVariable(newtree,'Mqq_gen')
Mbb_gen = SetVariable(newtree,'Mbb_gen')

arrayMax = 10
CSV = SetVariable(newtree,'CSV','F',arrayMax)

if maxEvents<0: maxEvents = nEntries
nEntries = min(nEntries,maxEvents)
for entry in range(0,nEntries):
    tree.GetEntry(entry)

    if entry%1000==0: print "entry: ",entry

    lorentzvectorswithcsv = []
    for i in range(tree.nJet):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(tree.Jet_pt[i],tree.Jet_eta[i],tree.Jet_phi[i],tree.Jet_mass[i])
        jet.csv = tree.Jet_btagCSV[i]
        if tree.Jet_pt[i]>30:
            lorentzvectorswithcsv.append(jet)

    SortByCSV(lorentzvectorswithcsv)
    for i,jet in enumerate(lorentzvectorswithcsv):
        if i>=arrayMax: break
        CSV[i]=jet.csv

    (b1,b2,q1,q2) = Sort(lorentzvectorswithcsv,'Eta')
    (Detaqq_eta[0],Dphibb_eta[0],Mqq_eta[0],Mbb_eta[0]) = GetVariablesToFill(b1,b2,q1,q2)

    (b1,b2,q1,q2) = Sort(lorentzvectorswithcsv,'1BTagAndEta')
    (Detaqq_1b[0],Dphibb_1b[0],Mqq_1b[0],Mbb_1b[0]) = GetVariablesToFill(b1,b2,q1,q2)

    (b1,b2,q1,q2) = Sort(lorentzvectorswithcsv,'2BTagAndPt')
    (Detaqq_2b[0],Dphibb_2b[0],Mqq_2b[0],Mbb_2b[0]) = GetVariablesToFill(b1,b2,q1,q2)


    newtree.Fill()

newtree.AutoSave()
output.Write()
output.Close()

