float tnL1Pt1PtPt3(float x){
	return ((0.5+(0.5*erf((((x-183.802)*(((x-183.802)>14.1984)/16.6663))+((x-183.802)*(((x-183.802)<14.1984)/30.495)))+(14.1984*(((1/16.6663)-(1/30.495))*((x-183.802)<14.1984))))))*0.954405)+0.000345421 ; }

float tnCaloPt4(float x){
	return ((0.5+(0.5*erf((((x-17.6551)*(((x-17.6551)>9.81356)/12.3532))+((x-17.6551)*(((x-17.6551)<9.81356)/7.42078)))+(9.81356*(((1/12.3532)-(1/7.42078))*((x-17.6551)<9.81356))))))*0.529189)+0.468483 ; }

float tnCaloPt3(float x){
	return ((0.5+(0.5*erf((((x-54.6654)*(((x-54.6654)>-11.8674)/13.9363))+((x-54.6654)*(((x-54.6654)<-11.8674)/12.1076)))+(-11.8674*(((1/13.9363)-(1/12.1076))*((x-54.6654)<-11.8674))))))*1)-0.0126234 ; }

float tnCaloPt2(float x){
	return ((0.5+(0.5*erf((((x-61.8285)*(((x-61.8285)>12.1091)/19.9767))+((x-61.8285)*(((x-61.8285)<12.1091)/13.9962)))+(12.1091*(((1/19.9767)-(1/13.9962))*((x-61.8285)<12.1091))))))*0.919179)+0.0781509 ; }

float tnCaloPt1(float x){
	return ((0.5+(0.5*erf((((x-75.454)*(((x-75.454)>-75.6892)/17.6854))+((x-75.454)*(((x-75.454)<-75.6892)/7.55613)))+(-75.6892*(((1/17.6854)-(1/7.55613))*((x-75.454)<-75.6892))))))*1)-0.00169507 ; }

float tnCaloCSV1(float x){
	return ((0.5+(0.5*erf((((x-2.04876)*(((x-2.04876)>-31.9312)/1.43527))+((x-2.04876)*(((x-2.04876)<-31.9312)/1.66136)))+(-31.9312*(((1/1.43527)-(1/1.66136))*((x-2.04876)<-31.9312))))))*0.859108)+0.033019 ; }

float tnPFPt4(float x){
	return ((0.5+(0.5*erf((((x-11.9656)*(((x-11.9656)>-9.59782)/12.2288))+((x-11.9656)*(((x-11.9656)<-9.59782)/9.53674e-05)))+(-9.59782*(((1/12.2288)-(1/9.53674e-05))*((x-11.9656)<-9.59782))))))*0.501703)+0.491815 ; }

float tnPFPt3(float x){
	return ((0.5+(0.5*erf((((x-62.9535)*(((x-62.9535)>-7.13383)/10.7823))+((x-62.9535)*(((x-62.9535)<-7.13383)/37.1993)))+(-7.13383*(((1/10.7823)-(1/37.1993))*((x-62.9535)<-7.13383))))))*1)-0.0281894 ; }

float tnPFPt2(float x){
	return ((0.5+(0.5*erf((((x-73.8892)*(((x-73.8892)>4.1477)/8.28245))+((x-73.8892)*(((x-73.8892)<4.1477)/12.8522)))+(4.1477*(((1/8.28245)-(1/12.8522))*((x-73.8892)<4.1477))))))*0.999999)-0.00657299 ; }

float tnPFPt1(float x){
	return ((0.5+(0.5*erf((((x-89.4107)*(((x-89.4107)>-64.3916)/8.8082))+((x-89.4107)*(((x-89.4107)<-64.3916)/0.295189)))+(-64.3916*(((1/8.8082)-(1/0.295189))*((x-89.4107)<-64.3916))))))*0.807868)+0.184056 ; }

float tn2D_eta(float x, float y){
	return (((0.5+(0.5*erf((x-156.505)/25.1804)))*0.550452)+0.446837)*(((0.5+(0.5*erf((y-1.50325)/0.055298)))*0.670504)+0.257757) ; }

float tnPFCSV2_double(float x){
	return ((0.5+(0.5*erf((((x-1.79969)*(((x-1.79969)>6.00186)/1.54199))+((x-1.79969)*(((x-1.79969)<6.00186)/1.64715)))+(6.00186*(((1/1.54199)-(1/1.64715))*((x-1.79969)<6.00186))))))*0.902665)-0.0204709 ; }

float tnPFCSV1_double(float x){
	return ((0.5+(0.5*erf((((x-0.881101)*(((x-0.881101)>5.31783)/1.68703))+((x-0.881101)*(((x-0.881101)<5.31783)/1.60846)))+(5.31783*(((1/1.68703)-(1/1.60846))*((x-0.881101)<5.31783))))))*0.490322)+0.5 ; }

float tn2D_double(float x, float y){
	return (((0.5+(0.5*erf((x-1.31852)/0.0812595)))*0.512547)+0.374884)*(((0.5+(0.5*erf((y-201.504)/14.6938)))*0.292673)+0.558846) ; }

float tnPFCSV1_single(float x){
	return ((0.5+(0.5*erf((((x-0.889029)*(((x-0.889029)>53.9104)/1.23463))+((x-0.889029)*(((x-0.889029)<53.9104)/1.21341)))+(53.9104*(((1/1.23463)-(1/1.21341))*((x-0.889029)<53.9104))))))*0.551122)+0.421845 ; }

float tn2D_single(float x, float y){
	return (((0.5+(0.5*erf((x-1.65917)/-0.0468921)))*0.841835)+0.107057)*(((0.5+(0.5*erf((y-4.11464)/0.0876627)))*0.682999)+0.0591433) ; }

float SingleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float DeltaEtaqq_eta, float Mqq_eta, float DeltaPhibb_single, float DeltaEtaqq_single){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-9))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_single(-log(1-CSV1+1.e-9))*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }

float DoubleBtagVBFTriggerWeightBeta(float pt1, float pt2, float pt3, float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-9))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_double(-log(1-CSV1+1.e-9))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float DoubleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-9))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_double(-log(1-CSV1+1.e-9))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float PrescaledBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 ,float DeltaEtaqq_eta, float Mqq_eta){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tn2D_eta(Mqq_eta,DeltaEtaqq_eta) ; }

float DoubleBtagVBFTriggerWeightNoCommonPart(float CSV1, float CSV2 , float DeltaEtaqq_double, float Mqq_double){
	return tnPFCSV1_double(-log(1-CSV1+1.e-9))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float SingleBtagVBFTriggerWeightNoCommonPart(float CSV1, float DeltaPhibb_single, float DeltaEtaqq_single){
	return tnPFCSV1_single(-log(1-CSV1+1.e-9))*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }

