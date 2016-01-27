from ROOT import *

class Jet:
    eta =0
    phi =0

def isInside(map_,eta,phi):
    bin_ = map_.FindBin(phi,eta)
    bit = map_.GetBinContent(bin_)
    if bit>0:
        return True
    else:
        return False

filt = TFile("plot.root")

NewUnder    = filt.Get("NewUnder")
NewOver     = filt.Get("NewOver")
NewUnderQCD = filt.Get("NewUnderQCD")
NewOverQCD  = filt.Get("NewOverQCD")

rnd = TRandom3()
jet = Jet()
i = 0
hist = TH2F("hist","",128,-3.2,3.2,128,-3.2,3.2)
while i<1000000:
    i += 1
    jet.eta = (rnd.Rndm()-0.5)*2*3.1415
    jet.phi = (rnd.Rndm()-0.5)*2*3.1415
    bit = isInside(NewUnder,jet.eta,jet.phi)
    if bit:
#        print jet.phi,jet.eta, bit
        hist.Fill(jet.phi,jet.eta)

hist.Draw("COLZ")



