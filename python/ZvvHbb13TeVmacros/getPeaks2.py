from ROOT import *
from array import array
from math import *

rangeX = 1.0
rangeY = 0.25
vetoX = 0.05
vetoY = 0.05

significance = 5
significanceBorder = 2

def fromTH2ToDict(hist2D,dict_):
    for x in range(hist2D.GetXaxis().GetNbins()):
        for y in range(hist2D.GetYaxis().GetNbins()):
            dict_[(x,y)]=hist2D.GetBinContent(x,y)

def fromDictToTH2(dict_,hist2D):
    for x in range(hist2D.GetXaxis().GetNbins()):
        for y in range(hist2D.GetYaxis().GetNbins()):
            hist2D.SetBinContent(x,y,dict_[(x,y)])


def getSignificance(x,y,maxX,maxY,plot2D,clusterMap,rangeXbins,rangeYbins,vetoXbins,vetoYbins):
    sum_  = 25 ## to avoid 1/0
    count = 0
    for i in range(x-rangeXbins,x+rangeXbins+1):
        i = i%maxX
        for j in range(y-rangeYbins,y+rangeYbins+1):
            j = j%maxY
            if clusterMap[(i,j)]==0:
                sum_  += plot2D[(i,j)]
                count += 1
    value = plot2D[(x,y)]
    sig = 0
    mean = 1E-9
    if count > 0:
        mean = sum_/count
        sig = (value-mean)/(sqrt(mean))
    return sig,value,sum_,count

def getClusters(plot2D,clusterMap,Nxaxis,Nyaxis,rangeXbins,rangeYbins,vetoXbins,vetoYbins):
    touch = True
    it =0
    skipLine = []
    while touch is True:
        print "iteration ",it
        it+=1
        touch = False
        for y in range(Nyaxis):
            for x in range(Nxaxis):
                if clusterMap[(x,y)]==0:
                    sig,value,sum_,count = getSignificance(x,y,Nxaxis,Nyaxis,plot2D,clusterMap,rangeXbins,rangeYbins,vetoXbins,vetoYbins)
                if sig > significance:
                    touch = True
#                    plot2D.SetBinContent(x,y,0)
                    clusterMap[(x,y)]=1
                    print x,y,sig,sum_,value,count,sum_/count
                elif sig > significanceBorder and (clusterMap[((x+1)%Nxaxis,y)]==1 or clusterMap[((x-1)%Nxaxis,y)]==1 or clusterMap[(x,(y+1)%Nyaxis)]==1 or clusterMap[(x,(y-1)%Nxaxis)]==1):
                    touch = True
#                    plot2D.SetBinContent(x,y,0)
                    clusterMap[(x,y)]=1.
                    print x,y,sig,sum_,value,count,sum_/count," border"

fil = TFile.Open("newfile.root")
newfile = TFile("plot.root","recreate")
Under = fil.Get("Under")
gDirectory.cd()
Under = Under.Clone("Under")
Over = fil.Get("Over")
UnderQCD = fil.Get("UnderQCD")
OverQCD = fil.Get("OverQCD")

NewUnder = Under.Clone("NewUnder")
NewOver = Over.Clone("NewOver")
NewUnderQCD = UnderQCD.Clone("NewUnderQCD")
NewOverQCD = OverQCD.Clone("NewOverQCD")
NewUnder.Reset()
NewOver.Reset()
NewUnderQCD.Reset()
NewOverQCD.Reset()

FiltUnder = Under.Clone("FiltUnder")
FiltOver = Over.Clone("FiltOver")
FiltUnderQCD = UnderQCD.Clone("FiltUnderQCD")
FiltOverQCD = OverQCD.Clone("FiltOverQCD")

value = 99999.
ratio = 9999.
xaxis = Under.GetXaxis()
Nxaxis = xaxis.GetNbins()
xMax = xaxis.GetXmax()
xMin = xaxis.GetXmin()
yaxis = Under.GetYaxis()
Nyaxis = yaxis.GetNbins()
yMax = yaxis.GetXmax()
yMin = yaxis.GetXmin()

rangeXbins = int(rangeX/(xMax-xMin)*Nxaxis)
rangeYbins = int(rangeY/(yMax-yMin)*Nyaxis)
vetoXbins = int(vetoX/(xMax-xMin)*Nxaxis)
vetoYbins = int(vetoY/(yMax-yMin)*Nyaxis)
rangeXbins = min(Nxaxis,rangeXbins)
rangeYbins = min(Nyaxis,rangeYbins)

for x in range(Nxaxis):
    for y in range(Nyaxis):
        NewUnder.SetBinContent(x,y,0.)
        NewOver.SetBinContent(x,y,0.)
        NewUnderQCD.SetBinContent(x,y,0.)
        NewOverQCD.SetBinContent(x,y,0.)

Dict = {}
NewDict = {}

fromTH2ToDict (Under,Dict)
fromTH2ToDict (NewUnder,NewDict)
getClusters(Dict,NewDict,Nxaxis,Nyaxis,rangeXbins,rangeYbins,vetoXbins,vetoYbins)
fromDictToTH2 (Dict,Under)
fromDictToTH2 (NewDict,NewUnder)

fromTH2ToDict (UnderQCD,Dict)
fromTH2ToDict (NewUnderQCD,NewDict)
getClusters(Dict,NewDict,Nxaxis,Nyaxis,rangeXbins,rangeYbins,vetoXbins,vetoYbins)
fromDictToTH2 (Dict,UnderQCD)
fromDictToTH2 (NewDict,NewUnderQCD)

fromTH2ToDict (Over,Dict)
fromTH2ToDict (NewOver,NewDict)
getClusters(Dict,NewDict,Nxaxis,Nyaxis,rangeXbins,rangeYbins,vetoXbins,vetoYbins)
fromDictToTH2 (Dict,Over)
fromDictToTH2 (NewDict,NewOver)

fromTH2ToDict (OverQCD,Dict)
fromTH2ToDict (NewOverQCD,NewDict)
getClusters(Dict,NewDict,Nxaxis,Nyaxis,rangeXbins,rangeYbins,vetoXbins,vetoYbins)
fromDictToTH2 (Dict,OverQCD)
fromDictToTH2 (NewDict,NewOverQCD)

for x in range(Nxaxis):
    for y in range(Nyaxis):
        if NewUnder.GetBinContent(x,y)==1    : FiltUnder.SetBinContent(x,y,0.)
        if NewOver.GetBinContent(x,y)==1    : FiltOver.SetBinContent(x,y,0.)
        if NewUnderQCD.GetBinContent(x,y)==1: FiltUnderQCD.SetBinContent(x,y,0.)
        if NewOverQCD.GetBinContent(x,y)==1 : FiltOverQCD.SetBinContent(x,y,0.)

UnderQCD.Write()
OverQCD.Write()
Under.Write()
Over.Write()
NewUnder.Write()
NewOver.Write()
NewUnderQCD.Write()
NewOverQCD.Write()
FiltUnder.Write()
FiltOver.Write()
FiltUnderQCD.Write()
FiltOverQCD.Write()
c1 = TCanvas("c1")
NewUnder.Draw("COLZ")
Under.Draw("same")
c1.SaveAs("Check_Under.png")
NewOver.Draw("COLZ")
Over.Draw("same")
c1.SaveAs("Check_Over.png")
NewUnderQCD.Draw("COLZ")
UnderQCD.Draw("same")
c1.SaveAs("Check_UnderQCD.png")
NewOverQCD.Draw("COLZ")
OverQCD.Draw("same")
c1.SaveAs("Check_OverQCD.png")
#c2 = TCanvas("c2")
#New.Draw("COLZ")
newfile.Close()
#Under.GetXAxis().GetBinCenter()
#print x[0],y[0],z[0]

