import os,sys
from optparse import OptionParser

dictionary = {
    'hJet_ptLeadTrack':		'Jet_leadTrackPt[hJCidx]',
    'hJet_ptRaw':			'Jet_rawPt[hJCidx]',
    'hJet_pt':				'Jet_pt[hJCidx]',
    'hJet_eta':				'Jet_eta[hJCidx]',
    'hJet_phi':				'Jet_phi[hJCidx]',
    'hJet_e':				'VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])',
#    'hJet_e':				'Jet_mass[hJCidx]',
    'hJet_genPt':			'Jet_mcPt[hJCidx]',
    'hJet_vtxMass':			'Jet_vtxMass[hJCidx]',
    'hJet_vtx3dL':			'Jet_vtx3DVal[hJCidx]',
    'hJet_vtx3deL':			'Jet_vtx3DSig[hJCidx]',
    'hJet_vtxPt':			'Jet_vtxPt[hJCidx]',
    'hJet_nconstituents':	'Jet_mult[hJCidx]',
    'hJet_JECUnc':			'Jet_mass[hJCidx]',	##FIXME: in V12, Jet_JECUnc[hJCidx]
    'hJet_csv':				'Jet_btagnew',
    'hJet_csv_nominal':		'Jet_btagnew',	##FIXME
    'hJet_csv_downBC':		'Jet_btagnew',	##FIXME
    'hJet_csv_upBC':		'Jet_btagnew',	##FIXME
    'hJet_csv_downL':		'Jet_btagnew',	##FIXME
    'hJet_csv_upL':			'Jet_btagnew',	##FIXME
    
    'hJet_cef':				'Jet_chEmEF[hJCidx]',
    'hJet_chf':				'Jet_chHEF[hJCidx]',
    'hJet_vtxPt':			'Jet_vtxPt[hJCidx]',
    'hJet_SoftLeptPt':		'Jet_leptonPt[hJCidx]',
    'hJet_SoftLeptdR':		'Jet_leptonDeltaR[hJCidx]',
    'hJet_SoftLeptptRel':	'Jet_leptonPtRel[hJCidx]',
    'hJet_SoftLeptId95':	'1',	##FIXME
    'hJet_SoftLeptIdlooseMu':'1',	##FIXME
    
    'METnoPU.et':			'met_pt',	##FIXME
    'METnoPU.phi':			'met_phi',	##FIXME
    'MET.et':				'met_pt',
    'MET.phi':				'met_phi',
    'EVENT.event':			'evt',
    
    'hJCidx][0]':			'hJCidx[0]]',
    'hJCidx][1]':			'hJCidx[1]]',
    'hJCidx][2]':			'hJCidx[2]]',

    '[hJCidx]0':			'0',
    '[hJCidx]1':			'1',
    '[hJCidx]t0':			't0',
    '[hJCidx]t1':			't1',
    'Jet_ptRaw':			'Jet_rawPt',
    'signals = ZHtest':		'signals = ZvvHbb',
    'tree.Jet_mcPt[hJCidx':	'tree.Jet_mcPt[tree.hJCidx',
    'tree.Jet_mass[hJCidx':	'tree.Jet_mass[tree.hJCidx',
    'fVHbb::HV_mass':		'fHV_mass',
    
    'hJet_flavour':			'Jet_hadronFlavour',
    'hbhe':					'Flag_HBHENoiseFilter',
    
    'hJet_puJetIdL':		'Jet_puId[hJCidx]',
    'hJet_btagCSV':			'Jet_btagnew[hJCidx]',
    'EVENT.run':			'run',
    'vLepton_':				'vLeptons_',
    'deltaPullAngle2':		'1',	##FIXME
    'deltaPullAngle':		'1',	##FIXME
    
    'VHbb::evalEt(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_phi[hJCidx],VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx]))':				'VHbb::evalEtFromPtEtaPhiM(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_phi[hJCidx],Jet_mass[hJCidx])',
    'VHbb::evalMt(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_phi[hJCidx],VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx]))':				'VHbb::evalMtFromPtEtaPhiM(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_phi[hJCidx],Jet_mass[hJCidx])',
    'VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])t0':'jetEt0',
    'VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])t1':'jetEt1',
    
    'VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])[0]':'VHbb::GetEnergy(Jet_pt[hJCidx[0]],Jet_eta[hJCidx[0]],Jet_mass[hJCidx[0]])',
    'VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])[1]':'VHbb::GetEnergy(Jet_pt[hJCidx[1]],Jet_eta[hJCidx[1]],Jet_mass[hJCidx[1]])',

}

doAtBegin = ['hJet_ptRaw','hJet_eta','hJet_ptLeadTrack','hJet_csv_downBC','hJet_csv_upBC','hJet_csv_downL','hJet_csv_upL']
doAtEnd = ['hJCidx]0','hJCidx]1','hJCidx][0]','hJCidx][1]','hJCidx][2]','VHbb::evalEt(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_phi[hJCidx],VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx]))','VHbb::evalMt(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_phi[hJCidx],VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx]))','VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])t0','VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])t1','tree.Jet_mcPt[hJCidx','VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])[0]','VHbb::GetEnergy(Jet_pt[hJCidx],Jet_eta[hJCidx],Jet_mass[hJCidx])[1]']

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
