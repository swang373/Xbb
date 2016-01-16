float tnL1Pt1PtPt3(float x){
	return ((0.5+(0.5*erf((((x-154.151)*(((x-154.151)>15.7164)/44.4823))+((x-154.151)*(((x-154.151)<15.7164)/29.7691)))+(15.7164*(((1/44.4823)-(1/29.7691))*((x-154.151)<15.7164))))))*0.9996)-0.000128188 ; }

float tnCaloPt4(float x){
	return ((0.5+(0.5*erf((((x-16.9778)*(((x-16.9778)>3.17817)/10.3723))+((x-16.9778)*(((x-16.9778)<3.17817)/47.4035)))+(3.17817*(((1/10.3723)-(1/47.4035))*((x-16.9778)<3.17817))))))*0.991455)+0.00557265 ; }

float tnCaloPt3(float x){
	return ((0.5+(0.5*erf((((x-49.5543)*(((x-49.5543)>10.3085)/18.2306))+((x-49.5543)*(((x-49.5543)<10.3085)/12.1589)))+(10.3085*(((1/18.2306)-(1/12.1589))*((x-49.5543)<10.3085))))))*0.996391)-0.00144363 ; }

float tnCaloPt2(float x){
	return ((0.5+(0.5*erf((((x-62.9825)*(((x-62.9825)>-28.2865)/15.4906))+((x-62.9825)*(((x-62.9825)<-28.2865)/10.8346)))+(-28.2865*(((1/15.4906)-(1/10.8346))*((x-62.9825)<-28.2865))))))*1)-0.00168415 ; }

float tnCaloPt1(float x){
	return ((0.5+(0.5*erf((((x-73.4465)*(((x-73.4465)>-13.1111)/18.1773))+((x-73.4465)*(((x-73.4465)<-13.1111)/1.54601)))+(-13.1111*(((1/18.1773)-(1/1.54601))*((x-73.4465)<-13.1111))))))*1)-0.000749359 ; }

float tnCaloCSV1(float x){
	return ((0.5+(0.5*erf((((x-1.91761)*(((x-1.91761)>-0.673661)/1.74892))+((x-1.91761)*(((x-1.91761)<-0.673661)/3.26724)))+(-0.673661*(((1/1.74892)-(1/3.26724))*((x-1.91761)<-0.673661))))))*1)-0.0869447 ; }

float tnPFPt4(float x){
	return ((0.5+(0.5*erf((((x-4.92849e-06)*(((x-4.92849e-06)>-1.22955)/21.7064))+((x-4.92849e-06)*(((x-4.92849e-06)<-1.22955)/2.26524)))+(-1.22955*(((1/21.7064)-(1/2.26524))*((x-4.92849e-06)<-1.22955))))))*0.996938)-0.00446654 ; }

float tnPFPt3(float x){
	return ((0.5+(0.5*erf((((x-51.703)*(((x-51.703)>22.2164)/22.8556))+((x-51.703)*(((x-51.703)<22.2164)/10.3735)))+(22.2164*(((1/22.8556)-(1/10.3735))*((x-51.703)<22.2164))))))*0.892305)+0.0800299 ; }

float tnPFPt2(float x){
	return ((0.5+(0.5*erf((((x-71.1878)*(((x-71.1878)>-1.53893)/11.8311))+((x-71.1878)*(((x-71.1878)<-1.53893)/100)))+(-1.53893*(((1/11.8311)-(1/100))*((x-71.1878)<-1.53893))))))*0.997639)-0.000425784 ; }

float tnPFPt1(float x){
	return ((0.5+(0.5*erf((((x-100.198)*(((x-100.198)>5.70873)/3.71766))+((x-100.198)*(((x-100.198)<5.70873)/12.3615)))+(5.70873*(((1/3.71766)-(1/12.3615))*((x-100.198)<5.70873))))))*0.915819)+0.0801155 ; }

float tn2D_eta(float x, float y){
	return (((0.5+(0.5*erf((x-161.49)/30.7873)))*0.419674)+0.548715)*(((0.5+(0.5*erf((y-1.50525)/0.0486336)))*0.803171)+0.185625) ; }

float tnPFCSV2_double(float x){
	return ((0.5+(0.5*erf((((x-1.55211)*(((x-1.55211)>5.56043)/1.73211))+((x-1.55211)*(((x-1.55211)<5.56043)/1.8647)))+(5.56043*(((1/1.73211)-(1/1.8647))*((x-1.55211)<5.56043))))))*1)-0.110443 ; }

float tnPFCSV1_double(float x){
	return ((0.5+(0.5*erf((((x-1.05372)*(((x-1.05372)>5.10002)/1.82154))+((x-1.05372)*(((x-1.05372)<5.10002)/1.83792)))+(5.10002*(((1/1.82154)-(1/1.83792))*((x-1.05372)<5.10002))))))*0.516394)+0.478093 ; }

float tn2D_double(float x, float y){
	return (((0.5+(0.5*erf((x-1.31489)/0.0839773)))*0.521762)+0.359789)*(((0.5+(0.5*erf((y-192.58)/20.2662)))*0.473351)+0.413715) ; }

float tnPFCSV1_single(float x){
	return ((0.5+(0.5*erf((((x-1.22245)*(((x-1.22245)>42.024)/1.5415))+((x-1.22245)*(((x-1.22245)<42.024)/1.5226)))+(42.024*(((1/1.5415)-(1/1.5226))*((x-1.22245)<42.024))))))*0.598223)+0.385035 ; }

float tn2D_single(float x, float y){
	return (((0.5+(0.5*erf((x-1.61831)/-0.11873)))*0.801715)+0.118356)*(((0.5+(0.5*erf((y-4.11527)/0.0607027)))*0.669485)+0.0543808) ; }

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

