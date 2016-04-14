#include"TFile.h"
#include"TH2F.h"

TFile *_file0 = 0;
TH2F* NewUnder = 0;
TH2F* NewOver = 0;
TH2F* NewUnderQCD = 0;
TH2F* NewOverQCD = 0;

bool Under(float phi, float eta){
    if(_file0==0){
        _file0 = TFile::Open("/scratch/sdonato/VHbbRun2/V21/CMSSW_7_1_5/src/Xbb/python/plot.root","r");
    }
    if(NewUnder==0){
        NewUnder = (TH2F*)_file0->Get("NewUnder");
    }
    int bin_ = NewUnder->FindBin(phi,eta);
    int bit = NewUnder->GetBinContent(bin_);
    if(bit>0) return true;
    else return false;
}
bool Over(float phi, float eta){
    if(_file0==0){
        _file0 = TFile::Open("/scratch/sdonato/VHbbRun2/V21/CMSSW_7_1_5/src/Xbb/python/plot.root","r");
    }
    if(NewOver==0){
        NewOver = (TH2F*)_file0->Get("NewOver");
    }
    int bin_ = NewOver->FindBin(phi,eta);
    int bit = NewOver->GetBinContent(bin_);
    if(bit>0) return true;
    else return false;
}
bool UnderQCD(float phi, float eta){
    if(_file0==0){
        _file0 = TFile::Open("/scratch/sdonato/VHbbRun2/V21/CMSSW_7_1_5/src/Xbb/python/plot.root","r");
    }
    if(NewUnderQCD==0){
        NewUnderQCD = (TH2F*)_file0->Get("NewUnderQCD");
    }
    int bin_ = NewUnderQCD->FindBin(phi,eta);
    int bit = NewUnderQCD->GetBinContent(bin_);
    if(bit>0) return true;
    else return false;
}
bool OverQCD(float phi, float eta){
    if(_file0==0){
        _file0 = TFile::Open("/scratch/sdonato/VHbbRun2/V21/CMSSW_7_1_5/src/Xbb/python/plot.root","r");
    }
    if(NewOverQCD==0){
        NewOverQCD = (TH2F*)_file0->Get("NewOverQCD");
    }
    int bin_ = NewOverQCD->FindBin(phi,eta);
    int bit = NewOverQCD->GetBinContent(bin_);
    if(bit>0) return true;
    else return false;
}

bool UnderAll(float phi, float eta){
    return (Under(phi,eta) || UnderQCD(phi,eta));
}

bool OverAll(float phi, float eta){
    return (Over(phi,eta) || OverQCD(phi,eta));
}

