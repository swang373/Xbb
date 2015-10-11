import os,sys
from optparse import OptionParser

dictionary = {
    'hJet_ptLeadTrack':    'Jet_leadTrackPt[hJidx]',
    'hJet_ptRaw':      'Jet_rawPt[hJidx]',
    'hJet_pt':        'Jet_pt[hJidx]',
    'hJet_eta':        'Jet_eta[hJidx]',
    'hJet_phi':        'Jet_phi[hJidx]',
    'hJet_e':        'VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])',
#    'hJet_e':        'Jet_mass[hJidx]',
    'hJet_genPt':      'Jet_mcPt[hJidx]',
    'hJet_vtxMass':      'Jet_vtxMass[hJidx]',
    'hJet_vtx3dL':      'Jet_vtx3DVal[hJidx]',
    'hJet_vtx3deL':      'Jet_vtx3DSig[hJidx]',
    'hJet_vtxPt':      'Jet_vtxPt[hJidx]',
    'hJet_nconstituents':  'Jet_mult[hJidx]',
    'hJet_JECUnc':      'Jet_mass[hJidx]',  ##FIXME: in V12, Jet_JECUnc[hJidx]
    'hJet_csv':        'Jet_btagnew[hJidx]',
    'hJet_csv_nominal':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_downBC4p':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_upBC4p':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_downL4p':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_upL4p':      'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_downBC':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_upBC':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_downL':    'Jet_btagnew[hJidx]',  ##FIXME
    'hJet_csv_upL':      'Jet_btagnew[hJidx]',  ##FIXME
    
    'hJet_cef':        'Jet_chEmEF[hJidx]',
    'hJet_chf':        'Jet_chHEF[hJidx]',
    'hJet_vtxPt':      'Jet_vtxPt[hJidx]',
    'hJet_SoftLeptPt':    'Jet_leptonPt[hJidx]',
    'hJet_SoftLeptdR':    'Jet_leptonDeltaR[hJidx]',
    'hJet_SoftLeptptRel':  'Jet_leptonPtRel[hJidx]',
    'hJet_SoftLeptId95':  '1',  ##FIXME
    'hJet_SoftLeptIdlooseMu':'1',  ##FIXME
    
    'aJet_pt':        'Jet_pt[aJidx]',
    'aJet_eta':        'Jet_eta[aJidx]',
    'aJet_phi':        'Jet_phi[aJidx]',
    'aJet_e':        'VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])',

    'METnoPU.et':      'met_pt',  ##FIXME
    'METnoPU.phi':      'met_phi',  ##FIXME
    'MET.et':        'met_pt',
    'MET.phi':        'met_phi',
    'EVENT.event':      'evt',
    
    'hJidx][0]':      'hJidx[0]]',
    'hJidx][1]':      'hJidx[1]]',
    'hJidx][2]':      'hJidx[2]]',

    '[hJidx]0':      '0',
    '[hJidx]1':      '1',
    '[hJidx]t0':      't0',
    '[hJidx]t1':      't1',
    'Jet_ptRaw':      'Jet_rawPt',
    'signals = ZHtest':    'signals = ZvvHbb',
    'tree.Jet_mcPt[hJidx':  'tree.Jet_mcPt[tree.hJidx',
    'tree.Jet_mass[hJidx':  'tree.Jet_mass[tree.hJidx',
    'fVHbb::HV_mass':    'fHV_mass',
    
    'hJet_flavour':      'Jet_hadronFlavour',
    'hbhe':          'Flag_HBHENoiseFilter',
    
    'hJet_puJetIdL':    'Jet_puId[hJidx]',
    'hJet_btagCSV':      'Jet_btagnew[hJidx]',
    'EVENT.run':      'run',
    'vLepton_':        'vLeptons_',
    'deltaPullAngle2':    '1',  ##FIXME
    'deltaPullAngle':    '1',  ##FIXME
    
    'VHbb::evalEt(Jet_pt[hJidx],Jet_eta[hJidx],Jet_phi[hJidx],VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx]))':        'VHbb::evalEtFromPtEtaPhiM(Jet_pt[hJidx],Jet_eta[hJidx],Jet_phi[hJidx],Jet_mass[hJidx])',
    'VHbb::evalMt(Jet_pt[hJidx],Jet_eta[hJidx],Jet_phi[hJidx],VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx]))':        'VHbb::evalMtFromPtEtaPhiM(Jet_pt[hJidx],Jet_eta[hJidx],Jet_phi[hJidx],Jet_mass[hJidx])',
    'VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])t0':'jetEt0',
    'VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])t1':'jetEt1',
    
    'VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])[0]':'VHbb::GetEnergy(Jet_pt[hJidx[0]],Jet_eta[hJidx[0]],Jet_mass[hJidx[0]])',
    'VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])[1]':'VHbb::GetEnergy(Jet_pt[hJidx[1]],Jet_eta[hJidx[1]],Jet_mass[hJidx[1]])',

    'VHbb::evalEt(Jet_pt[aJidx],Jet_eta[aJidx],Jet_phi[aJidx],VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx]))':        'VHbb::evalEtFromPtEtaPhiM(Jet_pt[aJidx],Jet_eta[aJidx],Jet_phi[aJidx],Jet_mass[aJidx])',
    'VHbb::evalMt(Jet_pt[aJidx],Jet_eta[aJidx],Jet_phi[aJidx],VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx]))':        'VHbb::evalMtFromPtEtaPhiM(Jet_pt[aJidx],Jet_eta[aJidx],Jet_phi[aJidx],Jet_mass[aJidx])',
    'VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])t0':'jetEt0',
    'VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])t1':'jetEt1',
    
    'VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])[0]':'VHbb::GetEnergy(Jet_pt[aJidx[0]],Jet_eta[aJidx[0]],Jet_mass[aJidx[0]])',
    'VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])[1]':'VHbb::GetEnergy(Jet_pt[aJidx[1]],Jet_eta[aJidx[1]],Jet_mass[aJidx[1]])',
    
    'Jet_btagnew[hJidx]4p':'Jet_btagnew[hJidx]',
}

doAtBegin = ['hJet_ptRaw','hJet_eta','hJet_ptLeadTrack','hJet_csv_downBC','hJet_csv_upBC','hJet_csv_downL','hJet_csv_upL','aJet_ptRaw','aJet_eta','aJet_ptLeadTrack','aJet_csv_downBC','aJet_csv_upBC','aJet_csv_downL','aJet_csv_upL']
doAtEnd = ['hJidx]0','hJidx]1','hJidx][0]','hJidx][1]','hJidx][2]','VHbb::evalEt(Jet_pt[hJidx],Jet_eta[hJidx],Jet_phi[hJidx],VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx]))','VHbb::evalMt(Jet_pt[hJidx],Jet_eta[hJidx],Jet_phi[hJidx],VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx]))','VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])t0','VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])t1','tree.Jet_mcPt[hJidx','VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])[0]','VHbb::GetEnergy(Jet_pt[hJidx],Jet_eta[hJidx],Jet_mass[hJidx])[1]','aJidx]0','aJidx]1','aJidx][0]','aJidx][1]','aJidx][2]','VHbb::evalEt(Jet_pt[aJidx],Jet_eta[aJidx],Jet_phi[aJidx],VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx]))','VHbb::evalMt(Jet_pt[aJidx],Jet_eta[aJidx],Jet_phi[aJidx],VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx]))','VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])t0','VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])t1','tree.Jet_mcPt[aJidx','VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])[0]','VHbb::GetEnergy(Jet_pt[aJidx],Jet_eta[aJidx],Jet_mass[aJidx])[1]'
]

#Jet_btagnew[hJidx]4p[0]
#print doAtBegin+dictionary.keys()+doAtEnd

argv = sys.argv
parser = OptionParser()
(opts, args) = parser.parse_args(argv)

def translate(line):
    for var in doAtBegin+dictionary.keys()+doAtEnd:
        while var in line: line=line.replace(var,dictionary[var])
    return line

print
print "Translating ",args[1]," ..."

filename = args[1]
open(filename)
if os.access(filename+".bak",0):
    print
    print filename+".bak is already existing."
    print "Using "+filename+".bak as input."
else:
    print
    print "Creating "+filename+".bak"
    command = "cp "+filename+" "+filename+".bak"
    os.popen(command,'r').read()

tmp = open(filename+".bak","r")
fileOut = open(filename,"w")
for line in tmp:
    line = translate(line)
    fileOut.write(line)
print
