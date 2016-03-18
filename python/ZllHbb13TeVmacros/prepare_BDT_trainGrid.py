##########################################

#GOAL:  Used to set the config to start optimizing various BDT parameters

#HOW IT WORKS:  Fills the datacards.ini and cuts.ini with one datacard per point on the Grid.

#HOW TO USE IT:

class GridMaker:

    def __init__(self, dcList, mvaList, config):

        self.dcList =  dcList
        self.mvaList = mvaList
        self.config = config

    def WriteDic(self, dic):

        _dic = ''
        for key, value in dic.iteritems():
            if 'header' in key: _dic =  value + '\n' + _dic
            else: _dic = _dic + key + ' = ' + value + '\n'
        print _dic

    def WriteHeaders(self):

        #for dc in self.dcList:
        #    for key, value in dc.iteritems():
        #        if not 'header' in key: continue
        #        else: print value + '\n'

        for mva in self.mvaList:
            for key, value in mva.iteritems():
                if not 'header' in key: continue
                else: print '\'' + value + '\','

    def WriteList(self):

        #for dc in self.dcList:
        #    self.WriteDic(dc)
        for mva in self.mvaList:
            self.WriteDic(mva)

from copy import copy, deepcopy

if __name__ == "__main__":

    #List of dic. Each dic is one dc
    dcList = []
    mvaList = []


    def appendList():
        dcList.append({'header_dc':copy(_header_dc),'var':copy(_var),'wsVarName':copy(_wsVarName),'range':copy(_range), 'dcName':copy(_dcName), 'cut':_cut, 'signal':copy(_signal), 'dcBin':copy(_dcBin), 'data':copy(_data), 'type':copy(_type)})
        mvaList.append({'header_mva':copy(_header_mva), 'MVAtype':copy(_MVAtype), 'MVAsettings':copy(_MVAsettings), 'signals':copy(_signals), 'backgrounds':copy(_backgrounds), 'treeVarSet':_treeVarSet, 'treeCut':_treeCut})

    #Default CR
    _header_dc = '[dc:Scan_dc_highpt]'
    _var = 'ZllBDT_highVpt.nominal'
    _wsVarName = 'ChHighPt_13TeV'
    _range = '20,-1,1'
    _dcName = 'ZmmHighPt_13TeV'
    _cut = 'SignalBDT_highpt'
    _signal = 'ZH_HToBB_ZToLL_M125_pow'
    _dcBin = 'Vpt2'
    _data = 'data_SM_Run2015C_25ns_16Dec2015 data_SM_Run2015D-16Dec2015'
    _type = 'BDT'

    #Default Training
    _header_mva = '[BDT_SCAN_Zmm_highVpt]'
    _MVAtype = 'BDT'
    _MVAsettings = '!H:!V:NTrees=300:nEventsMin=300:MaxDepth=2:BoostType=AdaBoost:AdaBoostBeta=0.1:SeparationType=MisClassificationError:nCuts=25:PruneMethod=NoPruning'
    _signals = '[\'ZH_HToBB_ZToLL_M125_pow\']'
    _backgrounds =  '[<!Samples|TT!>,<!Samples|DY!>,<!Samples|ST!>,<!Samples|WW!>,<!Samples|WZ!>,<!Samples|ZZ!>]'
    _treeVarSet = 'ZllBDTVars'
    _treeCut =  'ZllBDThighVptcut'


    #Grid
    Gr_range = range(20, 22)
    Gr_MVAsettings = {'NTrees':[200, 300], 'nEventsMin':[200, 300]}

    for r in Gr_range:
        for n1 in Gr_MVAsettings['NTrees']:
            for n2 in Gr_MVAsettings['nEventsMin']:

                _range = '%d,-1,1' %r

                _ntrees = _MVAsettings[_MVAsettings.find('NTrees=')+7:_MVAsettings.find(':nEventsMin=')]
                _MVAsettings = _MVAsettings.replace(':NTrees='+_ntrees+':', ':NTrees=%d:' %n1)
                _nevntmin = _MVAsettings[_MVAsettings.find('nEventsMin=')+11:_MVAsettings.find(':MaxDepth')]
                _MVAsettings = _MVAsettings.replace(':nEventsMin='+_nevntmin+':', ':nEventsMin=%d:' %n2)

                #Write the headers
                #mva
                _ntrees = _MVAsettings[_MVAsettings.find('NTrees=')+7:_MVAsettings.find(':nEventsMin=')]
                _nevntmin = _MVAsettings[_MVAsettings.find('nEventsMin=')+11:_MVAsettings.find(':MaxDepth')]
                _header_mva = '[BDT_SCAN_NTrees_%s_nEventsMin_%s_Zmm_highVpt]' %(_ntrees, _nevntmin)

                #dc
                _header_dc = '[dc:Scan_NTrees_%s_nEventsMin_%s_nbins_%s_dc_highpt]' %(_ntrees, _nevntmin, r)

                appendList()

    g = GridMaker( dcList, mvaList, '')
    g.WriteList()
    #g.WriteHeaders()












