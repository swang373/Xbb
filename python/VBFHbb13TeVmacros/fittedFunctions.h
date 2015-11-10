float tnL1Pt1PtPt3(float x){
	return ((0.5+(0.5*erf((((x-172.533)*(((x-172.533)>-26.9238)/31.8433))+((x-172.533)*(((x-172.533)<-26.9238)/29.1124)))+(-26.9238*(((1/31.8433)-(1/29.1124))*((x-172.533)<-26.9238))))))*0.971473)-6.05072e-15 ; }

float tnCaloPt4(float x){
	return ((0.5+(0.5*erf((((x-15.8288)*(((x-15.8288)>0.551315)/11.236))+((x-15.8288)*(((x-15.8288)<0.551315)/10)))+(0.551315*(((1/11.236)-(1/10))*((x-15.8288)<0.551315))))))*0.999337)-0.0160922 ; }

float tnCaloPt3(float x){
	return ((0.5+(0.5*erf((((x-45.5047)*(((x-45.5047)>85.8464)/14.7699))+((x-45.5047)*(((x-45.5047)<85.8464)/13.1236)))+(85.8464*(((1/14.7699)-(1/13.1236))*((x-45.5047)<85.8464))))))*0.986615)-5.55112e-17 ; }

float tnCaloPt2(float x){
	return ((0.5+(0.5*erf((((x-64.074)*(((x-64.074)>-17.7396)/16.8499))+((x-64.074)*(((x-64.074)<-17.7396)/100)))+(-17.7396*(((1/16.8499)-(1/100))*((x-64.074)<-17.7396))))))*1)-0.00290236 ; }

float tnCaloPt1(float x){
	return ((0.5+(0.5*erf((((x-75.3677)*(((x-75.3677)>-9.37514)/17.9133))+((x-75.3677)*(((x-75.3677)<-9.37514)/29.9207)))+(-9.37514*(((1/17.9133)-(1/29.9207))*((x-75.3677)<-9.37514))))))*1)-0.00152428 ; }

float tnCaloCSV1(float x){
	return (0.5+(0.5*erf((-(log(1.00001-x))-2.0399)/1.99998)))-0.0541937 ; }

float tnPFPt4(float x){
	return ((0.5+(0.5*erf((((x-7.53983)*(((x-7.53983)>-10.4496)/13.557))+((x-7.53983)*(((x-7.53983)<-10.4496)/9.53674e-05)))+(-10.4496*(((1/13.557)-(1/9.53674e-05))*((x-7.53983)<-10.4496))))))*0.994992)-0.000535414 ; }

float tnPFPt3(float x){
	return ((0.5+(0.5*erf((((x-63.3443)*(((x-63.3443)>-8.4695)/10.7624))+((x-63.3443)*(((x-63.3443)<-8.4695)/44.3442)))+(-8.4695*(((1/10.7624)-(1/44.3442))*((x-63.3443)<-8.4695))))))*0.974373)-1.24545e-09 ; }

float tnPFPt2(float x){
	return ((0.5+(0.5*erf((((x-73.0416)*(((x-73.0416)>2.98059)/9.75536))+((x-73.0416)*(((x-73.0416)<2.98059)/15.218)))+(2.98059*(((1/9.75536)-(1/15.218))*((x-73.0416)<2.98059))))))*0.996033)-6.696e-09 ; }

float tnPFPt1(float x){
	return ((0.5+(0.5*erf((((x-87.6235)*(((x-87.6235)>-3.77097)/10.1247))+((x-87.6235)*(((x-87.6235)<-3.77097)/100)))+(-3.77097*(((1/10.1247)-(1/100))*((x-87.6235)<-3.77097))))))*0.995017)-3.01948e-07 ; }

float tn2D_eta(float x, float y){
	return (((0.5+(0.5*erf((x-1.25747)/0.049284)))*0.502937)+0.355341)*(((0.5+(0.5*erf((y-197.984)/21.0805)))*0.478819)+0.378706) ; }

float tnPFCSV2_double(float x){
	return (0.5+(0.5*erf((-(log(1.00001-x))-1.23032)/1.88512)))-0.112975 ; }

float tnPFCSV1_double(float x){
	return (0.5+(0.5*erf((-(log(1.00001-x))+0.25909)/2.66782)))+0.000889071 ; }

float tn2D_double(float x, float y){
	return (((0.5+(0.5*erf((x-1.25747)/0.049284)))*0.502937)+0.355341)*(((0.5+(0.5*erf((y-197.984)/21.0805)))*0.478819)+0.378706) ; }

float tnPFCSV1_single(float x){
	return (0.5+(0.5*erf((-(log(1.00001-x))-0.799271)/2.34988)))-0.00911299 ; }

float tn2D_single(float x, float y){
	return (((0.5+(0.5*erf((x-1.60994)/-0.0821751)))*0.762443)+0.165781)*(((0.5+(0.5*erf((y-4.101)/0.09318)))*0.631483)+0.0829281) ; }

float SingleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float DeltaEtaqq_eta, float Mqq_eta, float DeltaPhibb_single, float DeltaEtaqq_single){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(CSV1)*tn2D_eta(DeltaEtaqq_eta,Mqq_eta)*tnPFCSV1_single(CSV1)*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }

float DoubleBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 , float CSV1, float CSV2 , float DeltaEtaqq_eta, float Mqq_eta, float DeltaEtaqq_double, float Mqq_double){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tnCaloCSV1(CSV1)*tn2D_eta(DeltaEtaqq_eta,Mqq_eta)*tnPFCSV1_double(CSV1)*tnPFCSV2_double(CSV2)*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float PrescaledBtagVBFTriggerWeight(float pt1, float pt2, float pt3, float pt4 ,float DeltaEtaqq_eta, float Mqq_eta){
	return tnL1Pt1PtPt3(pt1+pt2+pt3)*tnCaloPt4(pt4)*tnPFPt4(pt4)*tnCaloPt3(pt3)*tnPFPt3(pt3)*tnCaloPt2(pt2)*tnPFPt2(pt2)*tnCaloPt1(pt1)*tn2D_eta(DeltaEtaqq_eta,Mqq_eta) ; }

float DoubleBtagVBFTriggerWeightNoCommonPart(float CSV1, float CSV2 , float DeltaEtaqq_double, float Mqq_double){
	return tnCaloCSV1(CSV1)*tnPFCSV1_double(CSV1)*tnPFCSV2_double(CSV2)*tn2D_double(DeltaEtaqq_double,Mqq_double) ; }

float SingleBtagVBFTriggerWeightNoCommonPart(float CSV1, float DeltaPhibb_single, float DeltaEtaqq_single){
	return tnCaloCSV1(CSV1)*tnPFCSV1_single(CSV1)*tn2D_single(DeltaPhibb_single,DeltaEtaqq_single) ; }

