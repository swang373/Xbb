float tnL1Pt1PtPt3(float x){
	return ((0.5+(0.5*erf((((x-130.091)*(((x-130.091)>9.43099)/64.5789))+((x-130.091)*(((x-130.091)<9.43099)/105.153)))+(9.43099*(((1/64.5789)-(1/105.153))*((x-130.091)<9.43099))))))*1.37915)-0.380174 ; }

float tnCaloPt4(float x){
	return ((0.5+(0.5*erf((((x-4.05382)*(((x-4.05382)>-54.1253)/18.3868))+((x-4.05382)*(((x-4.05382)<-54.1253)/160)))+(-54.1253*(((1/18.3868)-(1/160))*((x-4.05382)<-54.1253))))))*0.999999)-0.00132981 ; }

float tnCaloPt3(float x){
	return ((0.5+(0.5*erf((((x-56.9219)*(((x-56.9219)>-16.3512)/14.347))+((x-56.9219)*(((x-56.9219)<-16.3512)/31.7253)))+(-16.3512*(((1/14.347)-(1/31.7253))*((x-56.9219)<-16.3512))))))*0.895022)+0.0995038 ; }

float tnCaloPt2(float x){
	return ((0.5+(0.5*erf((((x-66.9205)*(((x-66.9205)>-0.176716)/19.1222))+((x-66.9205)*(((x-66.9205)<-0.176716)/67.0135)))+(-0.176716*(((1/19.1222)-(1/67.0135))*((x-66.9205)<-0.176716))))))*1.0074)-0.00836209 ; }

float tnCaloPt1(float x){
	return ((0.5+(0.5*erf((((x-79.7089)*(((x-79.7089)>3.96948)/22.0789))+((x-79.7089)*(((x-79.7089)<3.96948)/75.5626)))+(3.96948*(((1/22.0789)-(1/75.5626))*((x-79.7089)<3.96948))))))*0.999794)-0.000252001 ; }

float tnCaloCSV1(float x){
	return ((0.5+(0.5*erf((((x+0.0360641)*(((x+0.0360641)>1.43972)/2.68341))+((x+0.0360641)*(((x+0.0360641)<1.43972)/9.68397)))+(1.43972*(((1/2.68341)-(1/9.68397))*((x+0.0360641)<1.43972))))))*3.02954)-2.08655 ; }

float tnPFPt4(float x){
	return ((0.5+(0.5*erf((((x+149.212)*(((x+149.212)>-54.1253)/101.826))+((x+149.212)*(((x+149.212)<-54.1253)/-151183)))+(-54.1253*(((1/101.826)-(1/-151183))*((x+149.212)<-54.1253))))))*0.999329)-0.00191075 ; }

float tnPFPt3(float x){
	return ((0.5+(0.5*erf((((x-20.6671)*(((x-20.6671)>66.7429)/52.2549))+((x-20.6671)*(((x-20.6671)<66.7429)/16.8348)))+(66.7429*(((1/52.2549)-(1/16.8348))*((x-20.6671)<66.7429))))))*0.951666)+0.0378135 ; }

float tnPFPt2(float x){
	return ((0.5+(0.5*erf((((x-72.3655)*(((x-72.3655)>6.35906)/19.4599))+((x-72.3655)*(((x-72.3655)<6.35906)/97.4124)))+(6.35906*(((1/19.4599)-(1/97.4124))*((x-72.3655)<6.35906))))))*0.899408)+0.0993979 ; }

float tnPFPt1(float x){
	return ((0.5+(0.5*erf((((x-72.3976)*(((x-72.3976)>21.5329)/27.6847))+((x-72.3976)*(((x-72.3976)<21.5329)/2.13411e+07)))+(21.5329*(((1/27.6847)-(1/2.13411e+07))*((x-72.3976)<21.5329))))))*2.84062)-1.84124 ; }

float tn2D_eta(float x, float y){
	return (((0.5+(0.5*erf((x-83.488)/132.789)))*0.987824)-0.264747)*(((0.5+(0.5*erf((y-1.49579)/0.0742704)))*0.999273)+0.365991) ; }

float tnPFCSV2_double(float x){
	return ((0.5+(0.5*erf((((x-4.20004)*(((x-4.20004)>18.7559)/1.6168))+((x-4.20004)*(((x-4.20004)<18.7559)/1.88346)))+(18.7559*(((1/1.6168)-(1/1.88346))*((x-4.20004)<18.7559))))))*1.06856)-0.124119 ; }

float tnPFCSV1_double(float x){
	return ((0.5+(0.5*erf((((x+3.6134)*(((x+3.6134)>4.88841)/3.19571))+((x+3.6134)*(((x+3.6134)<4.88841)/12804.4)))+(4.88841*(((1/3.19571)-(1/12804.4))*((x+3.6134)<4.88841))))))*18.8679)-17.8708 ; }

float tn2D_double(float x, float y){
	return (((0.5+(0.5*erf((x-1.24276)/0.00789051)))*0.697653)+0.211805)*(((0.5+(0.5*erf((y-218.593)/30.868)))*0.705041)+0.176503) ; }

float tnPFCSV1_single(float x){
	return ((0.5+(0.5*erf((((x-1.02316)*(((x-1.02316)>1.47992)/2.39975))+((x-1.02316)*(((x-1.02316)<1.47992)/1.05828)))+(1.47992*(((1/2.39975)-(1/1.05828))*((x-1.02316)<1.47992))))))*0.548033)+0.442153 ; }

float tn2D_single(float x, float y){
	return (((0.5+(0.5*erf((x-1.57946)/-0.0303802)))*0.952378)+0.018705)*(((0.5+(0.5*erf((y-4.12041)/0.0724854)))*0.84985)+0.00279775) ; }

float SingleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float DeltaEtaqq_eta, float Mqq_eta, float DeltaPhibb_single, float DeltaEtaqq_single){
	if(isnan(CSV1)) CSV1=0;
	CSV1=CSV1>1?1:CSV1;CSV1=CSV1<0?0:CSV1;
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-7))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_single(-log(1-CSV1+1.e-7))*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }

float DoubleBtagVBFTriggerWeightBeta(float pt1, float pt2, float pt3, float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){
	if(isnan(CSV2)) CSV2=0;
	CSV2=CSV2>1?1:CSV2;CSV2=CSV2<0?0:CSV2;
	if(isnan(CSV1)) CSV1=0;
	CSV1=CSV1>1?1:CSV1;CSV1=CSV1<0?0:CSV1;
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-7))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_double(-log(1-CSV1+1.e-7))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float DoubleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){
	if(isnan(CSV2)) CSV2=0;
	CSV2=CSV2>1?1:CSV2;CSV2=CSV2<0?0:CSV2;
	if(isnan(CSV1)) CSV1=0;
	CSV1=CSV1>1?1:CSV1;CSV1=CSV1<0?0:CSV1;
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tnCaloCSV1(-log(1-CSV1+1.e-7))*tn2D_eta(Mqq_eta,DeltaEtaqq_eta)*tnPFCSV1_double(-log(1-CSV1+1.e-7))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float PrescaledBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 ,float DeltaEtaqq_eta, float Mqq_eta){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnPFPt1(pt1)*tn2D_eta(Mqq_eta,DeltaEtaqq_eta) ; }

float DoubleBtagVBFTriggerWeightNoCommonPart(float CSV1, float CSV2 , float DeltaEtaqq_double, float Mqq_double){
	return tnPFCSV1_double(-log(1-CSV1+1.e-7))*tnPFCSV2_double(-log(1-CSV2))*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float SingleBtagVBFTriggerWeightNoCommonPart(float CSV1, float DeltaPhibb_single, float DeltaEtaqq_single){
	return tnPFCSV1_single(-log(1-CSV1+1.e-7))*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }

