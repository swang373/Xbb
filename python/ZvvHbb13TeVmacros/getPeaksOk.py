from ROOT import *
from array import array
from math import *

def getSignificance(x,y,maxX,band,plot2D,clusterMap,Xveto):
    sum_  = 25 ## to avoid 1/0
    count = 0
    for i in range(maxX):
        for j in range(y-band,y+band+1):
#            print New.GetBinContent(i,j),Under.GetBinContent(i,j),x,y,i,j
            if clusterMap.GetBinContent(i,j)==0 and not ((i>=x-Xveto and i<=x+Xveto) and (j>=y-band and j<=y+band)):
#                print "XXX"
                sum_  += plot2D.GetBinContent(i,j)
                count += 1
    value = plot2D.GetBinContent(x,y)
    sig = 0
    mean = 1E-9
    if count > 0:
        mean = sum_/count
        sig = (value-mean)/(sqrt(mean))
#    if mean  > 0:
#        sig = (value-mean)/(1+sqrt(mean))
#    else:
#        sig = 1E9
#    print x,y,sum_,value,count,sig
    return sig,value,sum_,count
#    print sum_,count
#    return sum_/count

def getClusters(plot2D,clusterMap,Nxaxis,Nyaxis,Xveto):
    touch = True
    it =0
    skipLine = []
    while touch is True:
        print "iteration ",it
        it+=1
        touch = False
        for y in range(Nyaxis):
            for x in range(Nxaxis):
                band = 0
                sig = 0
                if clusterMap.GetBinContent(x,y)==0:
                    sig,value,sum_,count = getSignificance(x,y,Nxaxis,band,plot2D,clusterMap,Xveto)
                if sig > 5:
                    touch = True
#                    plot2D.SetBinContent(x,y,0)
                    clusterMap.SetBinContent(x,y,1.)
                    print x,y,sig,sum_,value,count,sum_/count
                elif sig > 2 and (clusterMap.GetBinContent((x+1)%Nxaxis,y)==1 or clusterMap.GetBinContent((x-1)%Nxaxis,y)==1 or clusterMap.GetBinContent(x,y+1)==1 or clusterMap.GetBinContent(x,y-1)==1):
                    touch = True
#                    plot2D.SetBinContent(x,y,0)
                    clusterMap.SetBinContent(x,y,1.)
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

value = 99999.
ratio = 9999.
xaxis = Under.GetXaxis()
Nxaxis = xaxis.GetNbins()
yaxis = Under.GetYaxis()
Nyaxis = yaxis.GetNbins()

for x in range(Nxaxis):
    for y in range(Nyaxis):
        NewUnder.SetBinContent(x,y,0.)
        NewOver.SetBinContent(x,y,0.)
        NewUnderQCD.SetBinContent(x,y,0.)
        NewOverQCD.SetBinContent(x,y,0.)

Xveto = 2

getClusters(Under,NewUnder,Nxaxis,Nyaxis,Xveto)
getClusters(Over,NewOver,Nxaxis,Nyaxis,Xveto)
getClusters(UnderQCD,NewUnderQCD,Nxaxis,Nyaxis,Xveto)
getClusters(OverQCD,NewOverQCD,Nxaxis,Nyaxis,Xveto)

UnderQCD.Write()
OverQCD.Write()
Under.Write()
Over.Write()
NewUnder.Write()
NewOver.Write()
NewUnderQCD.Write()
NewOverQCD.Write()
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

