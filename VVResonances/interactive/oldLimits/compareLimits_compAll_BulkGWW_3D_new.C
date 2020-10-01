void compareLimits_compAll_BulkGWW_3D_new()
{
  //=========Macro generated from canvas: c/c
  //=========  (Fri May  3 16:45:39 2019) by ROOT version6.06/09
  TCanvas *c = new TCanvas("c", "c",66,78,600,600);
  gStyle->SetOptFit(1);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  c->SetHighLightColor(2);
  c->Range(353.037,-4.103815,5506.123,-0.730103);
  c->SetFillColor(0);
  c->SetBorderMode(0);
  c->SetBorderSize(2);
  c->SetLogy();
  c->SetLeftMargin(0.15);
  c->SetRightMargin(0.04);
  c->SetTopMargin(0.08);
  c->SetBottomMargin(0.12);
  c->SetFrameFillStyle(0);
  c->SetFrameBorderMode(0);
  c->SetFrameFillStyle(0);
  c->SetFrameBorderMode(0);
   
  TH1F *hframe__1 = new TH1F("hframe__1","",1000,1126,5300);
  hframe__1->SetMinimum(0.0002);
  hframe__1->SetMaximum(0.1);
  hframe__1->SetDirectory(0);
  hframe__1->SetStats(0);
  hframe__1->SetLineStyle(0);
  hframe__1->SetMarkerStyle(20);
  hframe__1->GetXaxis()->SetTitle("m_{G_{bulk}} [GeV]");
  hframe__1->GetXaxis()->SetLabelFont(42);
  hframe__1->GetXaxis()->SetLabelOffset(0.007);
  hframe__1->GetXaxis()->SetTitleSize(0.05);
  hframe__1->GetXaxis()->SetTitleOffset(0.9);
  hframe__1->GetXaxis()->SetTitleFont(42);
  hframe__1->GetYaxis()->SetTitle("#sigma x #bf{#it{#Beta}}(G_{bulk} #rightarrow WW) (pb)  ");
  hframe__1->GetYaxis()->SetLabelFont(42);
  hframe__1->GetYaxis()->SetLabelOffset(0.007);
  hframe__1->GetYaxis()->SetTitleSize(0.045);
  hframe__1->GetYaxis()->SetTitleOffset(1.5);
  hframe__1->GetYaxis()->SetTitleFont(42);
  hframe__1->GetZaxis()->SetLabelFont(42);
  hframe__1->GetZaxis()->SetLabelOffset(0.007);
  hframe__1->GetZaxis()->SetTitleFont(42);
  hframe__1->Draw("");
   
  Double_t _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_001_fx1[32] = {
    1200,
    1300,
    1400,
    1500,
    1600,
    1700,
    1800,
    1900,
    2000,
    2100,
    2200,
    2300,
    2400,
    2500,
    2600,
    2700,
    2800,
    2900,
    3000,
    3100,
    3200,
    3300,
    3400,
    3500,
    3600,
    3700,
    3800,
    3900,
    4000,
    4100,
    4200,
    4300};
  Double_t _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_001_fy1[32] = {
    0.02666016,
    0.01782227,
    0.0144043,
    0.01166992,
    0.009350586,
    0.007543945,
    0.00612793,
    0.005102539,
    0.004260254,
    0.003625488,
    0.003137207,
    0.002807617,
    0.002575684,
    0.002362061,
    0.002130127,
    0.001922607,
    0.001739502,
    0.001629639,
    0.001470947,
    0.001385498,
    0.00133667,
    0.001239014,
    0.001174927,
    0.001119995,
    0.001068115,
    0.001016235,
    0.0009674072,
    0.0009246826,
    0.0008880615,
    0.0008453369,
    0.0008270264,
    0.0007476807};
  TGraph *graph = new TGraph(32,_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_001_fx1,_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_001_fy1);
  graph->SetName("_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_001");
   graph->SetTitle("");
   graph->SetFillColor(1);
   graph->SetLineColor(42);
   graph->SetLineStyle(5);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   
   TH1F *Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011 = new TH1F("Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011","",100,890,4610);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->SetMinimum(0.0006729126);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->SetMaximum(0.0292514);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->SetDirectory(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->SetStats(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->SetLineStyle(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->SetMarkerStyle(20);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetXaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetXaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetXaxis()->SetTitleOffset(1.1);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetXaxis()->SetTitleFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetYaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetYaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetYaxis()->SetTitleOffset(1.25);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetYaxis()->SetTitleFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetZaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetZaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011->GetZaxis()->SetTitleFont(42);
   //   graph->SetHistogram(Graph_ _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_0011);
   graph->SetHistogram(Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIb2gmI17mI001dIlimits_b2g17mI0011);
   
   graph->Draw("l");
   
   Double_t _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll_fx2[41] = {
   1200,
   1300,
   1400,
   1500,
   1600,
   1700,
   1800,
   1900,
   2000,
   2100,
   2200,
   2300,
   2400,
   2500,
   2600,
   2700,
   2800,
   2900,
   3000,
   3100,
   3200,
   3300,
   3400,
   3500,
   3600,
   3700,
   3800,
   3900,
   4000,
   4100,
   4200,
   4300,
   4400,
   4500,
   4600,
   4700,
   4800,
   4900,
   5000,
   5100,
   5200};
   Double_t _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll_fy2[41] = {
     0.0198125,
     0.0133125,
     0.0104375,
     0.00778125,
     0.00640625,
     0.005390625,
     0.00446875,
     0.003765625,
     0.003234375,
     0.002796875,
     0.002492188,
     0.002234375,
     0.002007813,
     0.0018125,
     0.001648437,
     0.001515625,
     0.001402344,
     0.001304688,
     0.001207031,
     0.001117188,
     0.001042969,
     0.0009765625,
     0.00090625,
     0.00084375,
     0.0007851563,
     0.0007304687,
     0.0006816406,
     0.0006445313,
     0.0006074219,
     0.0005742187,
     0.000546875,
     0.0005214844,
     0.0005019531,
     0.0004863281,
     0.0004726562,
     0.0004648438,
     0.0004589844,
     0.0004589844,
     0.0004648438,
     0.000484375,
     0.0005175781};
   graph = new TGraph(41,_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll_fx2,_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll_fy2);
   graph->SetName("_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll");
   graph->SetTitle("");
   graph->SetFillColor(1);
   graph->SetLineColor(46);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   
   TH1F *Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2 = new TH1F("Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2","",100,800,5600);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->SetMinimum(0.0004130859);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->SetMaximum(0.02174785);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->SetDirectory(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->SetStats(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->SetLineStyle(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->SetMarkerStyle(20);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetXaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetXaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetXaxis()->SetTitleOffset(1.1);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetXaxis()->SetTitleFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetYaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetYaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetYaxis()->SetTitleOffset(1.25);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetYaxis()->SetTitleFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetZaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetZaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2->GetZaxis()->SetTitleFont(42);
   //   graph->SetHistogram(Graph__portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2);
   graph->SetHistogram(Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdI2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll2);
   
   graph->Draw("l");
   
   Double_t _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll_fx3[41] = {
     1200,
     1300,
     1400,
     1500,
     1600,
     1700,
     1800,
     1900,
     2000,
     2100,
     2200,
     2300,
     2400,
     2500,
     2600,
     2700,
     2800,
     2900,
     3000,
     3100,
     3200,
     3300,
     3400,
     3500,
     3600,
     3700,
     3800,
     3900,
     4000,
     4100,
     4200,
     4300,
     4400,
     4500,
     4600,
     4700,
     4800,
     4900,
     5000,
     5100,
     5200};
   Double_t _portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll_fy3[41] = {
     0.0176875,
     0.010875,
     0.00809375,
     0.005671875,
     0.00446875,
     0.003703125,
     0.003046875,
     0.0025625,
     0.002179688,
     0.001875,
     0.001570313,
     0.00140625,
     0.001316406,
     0.001128906,
     0.001074219,
     0.0009765625,
     0.0008945313,
     0.000828125,
     0.0007617188,
     0.0006992187,
     0.0006464844,
     0.0006015625,
     0.0005605469,
     0.0005019531,
     0.0004921875,
     0.0004589844,
     0.0004296875,
     0.0004042969,
     0.0003798828,
     0.0003574219,
     0.0003398438,
     0.0003193359,
     0.0003027344,
     0.0002871094,
     0.0002753906,
     0.000265625,
     0.0002587891,
     0.0002558594,
     0.0002568359,
     0.0002548828,
     0.0002675781};
   graph = new TGraph(41,_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll_fx3,_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll_fy3);
   graph->SetName("_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll");
   graph->SetTitle("");
   graph->SetFillColor(1);
   graph->SetLineStyle(2);
   graph->SetLineWidth(3);
   graph->SetMarkerStyle(20);
   
   TH1F *Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3 = new TH1F("Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3","",100,800,5600);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->SetMinimum(0.0002293945);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->SetMaximum(0.01943076);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->SetDirectory(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->SetStats(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->SetLineStyle(0);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->SetMarkerStyle(20);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetXaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetXaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetXaxis()->SetTitleOffset(1.1);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetXaxis()->SetTitleFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetYaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetYaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetYaxis()->SetTitleOffset(1.25);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetYaxis()->SetTitleFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetZaxis()->SetLabelFont(42);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetZaxis()->SetLabelOffset(0.007);
   Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3->GetZaxis()->SetTitleFont(42);
   //   graph->SetHistogram(Graph__portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll3);
   graph->SetHistogram(Graph_dIportaldIekpbms2dIhomedIdschaeferdIDiBoson3DdIlimitsdIlimits_BulkGWW_13TeV_CMS_jj_combAll3);
   
   graph->Draw("l");



   //New limits! VV inclu
   Double_t mean_fx3003[34] = {
     1200,
     1300,
     1400,
     1500,
     1600,
     1700,
     1800,
     1900,
     2000,
     2100,
     2200,
     2300,
     2400,
     2500,
     2600,
     2700,
     2800,
     2900,
     3000,
     3100,
     3200,
     3300,
     3400,
     3500,
     3600,
     3700,
     3800,
     3900,
     4000,
     4100,
     4200,
     4300,
     4400,
     4500};
   Double_t mean_fy3003[34] = {
     0.01752637,
     0.01344707,
     0.01037328,
     0.008099069,
     0.006567266,
     0.005427713,
     0.004608265,
     0.003939709,
     0.003368233,
     0.002970028,
     0.002625125,
     0.002341187,
     0.002107625,
     0.001923247,
     0.001765761,
     0.001606909,
     0.001478822,
     0.001353877,
     0.001236704,
     0.001127152,
     0.001020852,
     0.0009324343,
     0.0008583299,
     0.0007912444,
     0.0007310726,
     0.0006805529,
     0.0006401809,
     0.0006011335,
     0.0005449475,
     0.0005306266,
     0.0005149121,
     0.0004952167,
     0.0005102012,
     0.0004670418};

   graph = new TGraph(34,mean_fx3003,mean_fy3003); // ,mean_felx3003,mean_fehx3003,mean_fely3003,mean_fehy3003);
   graph->SetName("mean");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(5);
   graph->SetLineWidth(2);
   graph->SetMarkerStyle(20);

   TH1F *Graph_mean3003 = new TH1F("Graph_mean3003","",100,1120,2500);
   Graph_mean3003->SetMinimum(0.001952419);
   Graph_mean3003->SetMaximum(0.01894219);
   Graph_mean3003->SetDirectory(0);
   Graph_mean3003->SetStats(0);
   Graph_mean3003->SetLineStyle(0);
   Graph_mean3003->SetMarkerStyle(20);
   Graph_mean3003->GetXaxis()->SetLabelFont(42);
   Graph_mean3003->GetXaxis()->SetLabelOffset(0.007);
   Graph_mean3003->GetXaxis()->SetTitleOffset(1.1);
   Graph_mean3003->GetXaxis()->SetTitleFont(42);
   Graph_mean3003->GetYaxis()->SetLabelFont(42);
   Graph_mean3003->GetYaxis()->SetLabelOffset(0.007);
   Graph_mean3003->GetYaxis()->SetTitleOffset(1.25);
   Graph_mean3003->GetYaxis()->SetTitleFont(42);
   Graph_mean3003->GetZaxis()->SetLabelFont(42);
   Graph_mean3003->GetZaxis()->SetLabelOffset(0.007);
   Graph_mean3003->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_mean3003);

   graph->Draw("l");


   //New limits! VV+VH
   Double_t mean_fx3004[16] = {
     1200,
     1300,
     1400,
     1500,
     1600,
     1700,
     1800,
     1900,
     2000,
     2100,
     2200,
     2300,
     2400,
     2500,
     2600,
     2700};
   Double_t mean_fy3004[16] = {
     0.0197706,
     0.01452283,
     0.01000572,
     0.00804302,
     0.007249113,
     0.006641506,
     0.005798479,
     0.005045777,
     0.004476008,
     0.004179254,
     0.003773617,
     0.003395776,
     0.00311959,
     0.002904496,
     0.002765947,
     0.002560262};

   graph = new TGraph(16,mean_fx3004,mean_fy3004); // ,mean_felx3003,mean_fehx3003,mean_fely3003,mean_fehy3003);                                                                                                                                                                
   graph->SetName("meanVVVH");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(4);
   graph->SetLineColor(4);
   graph->SetLineWidth(2);
   graph->SetMarkerStyle(20);

   TH1F *Graph_mean3004 = new TH1F("Graph_mean3004","",100,1120,2500);
   Graph_mean3004->SetMinimum(0.001952419);
   Graph_mean3004->SetMaximum(0.01894219);
   Graph_mean3004->SetDirectory(0);
   Graph_mean3004->SetStats(0);
   Graph_mean3004->SetLineStyle(0);
   Graph_mean3004->SetMarkerStyle(20);
   Graph_mean3004->GetXaxis()->SetLabelFont(42);
   Graph_mean3004->GetXaxis()->SetLabelOffset(0.007);
   Graph_mean3004->GetXaxis()->SetTitleOffset(1.1);
   Graph_mean3004->GetXaxis()->SetTitleFont(42);
   Graph_mean3004->GetYaxis()->SetLabelFont(42);
   Graph_mean3004->GetYaxis()->SetLabelOffset(0.007);
   Graph_mean3004->GetYaxis()->SetTitleOffset(1.25);
   Graph_mean3004->GetYaxis()->SetTitleFont(42);
   Graph_mean3004->GetZaxis()->SetLabelFont(42);
   Graph_mean3004->GetZaxis()->SetLabelOffset(0.007);
   Graph_mean3004->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_mean3004);

   graph->Draw("l");

   //Limit VV
   Double_t mean_fx3005[31] = {
     1200,
     1300,
     1400,
     1500,
     1600,
     1700,
     1800,
     1900,
     2000,
     2100,
     2200,
     2300,
     2400,
     2500,
     2600,
     2700,
     2800,
     2900,
     3000,
     3100,
     3200,
     3300,
     3400,
     3500,
     3600,
     3700,
     3800,
     3900,
     4000,
     4100,
     4200};
   Double_t mean_fy3005[31] = {
     0.01619052,
     0.01249083,
     0.009148091,
     0.007510555,
     0.006585209,
     0.005931552,
     0.005172854,
     0.004529612,
     0.00402691,
     0.003754964,
     0.003475307,
     0.003195404,
     0.002952197,
     0.002803567,
     0.002716555,
     0.00260823,
     0.002537624,
     0.002481027,
     0.002392354,
     0.002311616,
     0.002202079,
     0.00206337,
     0.001908685,
     0.001762985,
     0.001606087,
     0.001455909,
     0.00135869,
     0.001339438,
     0.001409305,
     0.001774815,
     0.002273016};

   graph = new TGraph(31,mean_fx3005,mean_fy3005); // ,mean_felx3003,mean_fehx3003,mean_fely3003,mean_fehy3003);                                                                                                                                                               
                                                                                                                                                                                                                                                                                
   graph->SetName("meanVV");
   graph->SetTitle("");
   graph->SetFillStyle(1000);
   graph->SetLineStyle(6);
   graph->SetLineColor(6);
   graph->SetLineWidth(2);
   graph->SetMarkerStyle(20);

   TH1F *Graph_mean3005 = new TH1F("Graph_mean3005","",100,1120,2500);
   Graph_mean3005->SetMinimum(0.001952419);
   Graph_mean3005->SetMaximum(0.01894219);
   Graph_mean3005->SetDirectory(0);
   Graph_mean3005->SetStats(0);
   Graph_mean3005->SetLineStyle(0);
   Graph_mean3005->SetMarkerStyle(20);
   Graph_mean3005->GetXaxis()->SetLabelFont(42);
   Graph_mean3005->GetXaxis()->SetLabelOffset(0.007);
   Graph_mean3005->GetXaxis()->SetTitleOffset(1.1);
   Graph_mean3005->GetXaxis()->SetTitleFont(42);
   Graph_mean3005->GetYaxis()->SetLabelFont(42);
   Graph_mean3005->GetYaxis()->SetLabelOffset(0.007);
   Graph_mean3005->GetYaxis()->SetTitleOffset(1.25);
   Graph_mean3005->GetYaxis()->SetTitleFont(42);
   Graph_mean3005->GetZaxis()->SetLabelFont(42);
   Graph_mean3005->GetZaxis()->SetLabelOffset(0.007);
   Graph_mean3005->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_mean3005);

   graph->Draw("l");


   


   TH1F *hframe_copy__2 = new TH1F("hframe_copy__2","",1000,1126,5300);
   hframe_copy__2->SetMinimum(0.0002);
   hframe_copy__2->SetMaximum(0.1);
   hframe_copy__2->SetDirectory(0);
   hframe_copy__2->SetStats(0);
   hframe_copy__2->SetLineStyle(0);
   hframe_copy__2->SetMarkerStyle(20);
   hframe_copy__2->GetXaxis()->SetTitle("m_{G_{bulk}} [GeV]");
   hframe_copy__2->GetXaxis()->SetLabelFont(42);
   hframe_copy__2->GetXaxis()->SetLabelOffset(0.007);
   hframe_copy__2->GetXaxis()->SetTitleSize(0.05);
   hframe_copy__2->GetXaxis()->SetTitleOffset(0.9);
   hframe_copy__2->GetXaxis()->SetTitleFont(42);
   hframe_copy__2->GetYaxis()->SetTitle("#sigma x #bf{#it{#Beta}}(G_{bulk} #rightarrow WW) (pb)  ");
   hframe_copy__2->GetYaxis()->SetLabelFont(42);
   hframe_copy__2->GetYaxis()->SetLabelOffset(0.007);
   hframe_copy__2->GetYaxis()->SetTitleSize(0.045);
   hframe_copy__2->GetYaxis()->SetTitleOffset(1.5);
   hframe_copy__2->GetYaxis()->SetTitleFont(42);
   hframe_copy__2->GetZaxis()->SetLabelFont(42);
   hframe_copy__2->GetZaxis()->SetLabelOffset(0.007);
   hframe_copy__2->GetZaxis()->SetTitleFont(42);
   hframe_copy__2->Draw("sameaxis");
   
   TLegend *leg = new TLegend(0.3600101,0.5,0.5520214,0.75,NULL,"brNDC");
   leg->SetTextSize(0.04);
   leg->SetLineColor(0);
   leg->SetLineStyle(1);
   leg->SetLineWidth(1);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
   TLegendEntry *entry=leg->AddEntry("NULL","95% CL expected upper limits","h");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("NULL","","");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_b2g_17_001_limits_b2g17_001","Phys. Rev. D97, 072006, 35.9 fb^{-1}","L");
   entry->SetLineColor(42);
   entry->SetLineStyle(5);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_2016limits_tau21ptCorr_BulkGWW_13TeV_CMS_jj_combAll","B2G-18-002, 35.9 fb^{-1}","L");
   entry->SetLineColor(46);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("mean"," AN-19-131, 35.9 fb^{-1}","L");
   entry->SetLineColor(1);
   entry->SetLineStyle(5);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("meanVVVH"," AN-19-131 VV+VH, 35.9 fb^{-1}","L");
   entry->SetLineColor(4);
   entry->SetLineStyle(4);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(3);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("meanVV"," AN-19-131 VV, 35.9 fb^{-1}","L");
   entry->SetLineColor(6);
   entry->SetLineStyle(6);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(3);
   entry->SetMarkerStyle(20);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("_portal_ekpbms2_home_dschaefer_DiBoson3D_limits_limits_BulkGWW_13TeV_CMS_jj_combAll","B2G-18-002, 77.3 fb^{-1}","L");
   entry->SetLineColor(1);
   entry->SetLineStyle(2);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   leg->Draw();
   TLatex *   tex = new TLatex(0.96,0.936,"  (13 TeV)");
   tex->SetNDC();
   tex->SetTextAlign(31);
   tex->SetTextFont(42);
   tex->SetTextSize(0.048);
   tex->SetLineWidth(2);
   tex->Draw();
   tex = new TLatex(0.1905,0.892,"CMS");
   tex->SetNDC();
   tex->SetTextAlign(13);
   tex->SetTextFont(61);
   tex->SetTextSize(0.06);
   tex->SetLineWidth(2);
   tex->Draw();
   tex = new TLatex(0.1905,0.82," ");
   tex->SetNDC();
   tex->SetTextAlign(13);
   tex->SetTextFont(52);
   tex->SetTextSize(0.0456);
   tex->SetLineWidth(2);
   tex->Draw();
   c->Modified();
   c->cd();
   c->SetSelected(c);
}
