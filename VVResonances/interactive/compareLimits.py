#o!/usr/bin/env python

import ROOT
import optparse
from CMGTools.VVResonances.plotting.CMS_lumi import *
from CMGTools.VVResonances.plotting.tdrstyle import *
from time import sleep
from array import array
import numpy as np
parser = optparse.OptionParser()
parser.add_option("-o","--output",dest="output",default='limit_compare.root',help="Limit plot")

parser.add_option("-x","--minX",dest="minX",type=float,help="minimum x",default=1126.0)
parser.add_option("-X","--maxX",dest="maxX",type=float,help="maximum x",default=5500.)
parser.add_option("-y","--minY",dest="minY",type=float,help="minimum y",default=0.0001)
parser.add_option("-Y","--maxY",dest="maxY",type=float,help="maximum y",default=0.14)
parser.add_option("-b","--blind",dest="blind",type=int,help="Not do observed ",default=1)
parser.add_option("-l","--log",dest="log",type=int,help="Log plot",default=1)

parser.add_option("-t","--titleX",dest="titleX",default='M_{X} (GeV)',help="title of x axis")
parser.add_option("-T","--titleY",dest="titleY",default="#sigma x BR(G_{Bulk} #rightarrow WW) (pb)  ",help="title of y axis")

parser.add_option("-p","--period",dest="period",default='2016',help="period")
parser.add_option("-f","--final",dest="final",type=int, default=1,help="Preliminary or not")



#    parser.add_option("-x","--minMVV",dest="minMVV",type=float,help="minimum MVV",default=1000.0)
#    parser.add_option("-X","--maxMVV",dest="maxMVV",type=float,help="maximum MVV",default=13000.0)


plotVV1D=False
plotVV3D2016= True
plotVV3D=False
plotVV3D2016data=False #True
plotVV3D2016pseudodata=True
plotVH2016=False


(options,args) = parser.parse_args()
#define output dictionary

scaleBR = True

setTDRStyle()

def getLegend(x1=0.650010112,y1=0.523362,x2=0.90202143,y2=0.8279833):
  legend = ROOT.TLegend(x1,y1,x2,y2)
  legend.SetTextSize(0.032)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend


#titleY = "#sigma x BR(Z^{'} #rightarrow ZH) (pb)  "
#titleY = "#sigma (Z^{'} #rightarrow ZH) (pb)  "
#oname= "ZprimeZH_VVVH_pseudo20_testvhlplp"
#oname= "ZprimeZH_VV_pseudo20_testvhlplp"
#oname= "ZprimeZH_pseudo20_tau21DDT_doubleB_0p91_0p86"
#oname= "ZprimeZH_scheme2_deepAK8_VVVH_optimizations_noBR"

titleY = "#sigma x BR(G_{Bulk} #rightarrow WW) (pb)  "
#oname= "BulkGWW_VVVH_testvhlplp"
#oname= "BulkGWW_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_VS_doubleB_0p91_0p86"
#oname= "BulkGWW_VH_testvhlplp"
#oname= "BulkGWW_tau21DDT_doubleB_0p91_0p86"
#oname= "BulkGWW_scheme2_deepAK8_VVVH_optimizations"
oname= "BulkGWW_VVinclu_tau21_vs_VVVHtau21doubleB_VVinclu_deepWDDT_VVVHdeepAK8"
#oname= "BulkGWW_VVinclu_tau21_vs_VVVHtau21doubleB_migrUnc"
#oname="BulkGWW_scheme2_deepAK8_VVVH_migrUnc"
#title = ["HPLP","HPHP","HPHP+HPLP","B2G-17-001"]
#files = ["LIMITS_DDT_latest/WW/HPLP/Limits_BulkGWW_HPLP_13TeV.root","LIMITS_DDT_latest/WW/HPHP/Limits_BulkGWW_HPHP_13TeV.root","LIMITS_DDT_latest/WW/combined/Limits_BulkGWW_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGWW_13TeV.root"]

#title = ["VH","VV","VVVH","VH migrUnc","VV migrUnc","VVVH migrUnc"]
#files = ["results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VV_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VH_scheme2_deepAK8WZH_migrUnc.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VV_scheme2_deepAK8WZH_migrUnc.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8WZH_migrUnc.root"]
#title = ["tau21DDT","VVVH tau21DDT+doubleB","VV","VH","VVVH tau21DDT+doubleB migrUnc","VV","VH"] 
#files=["debugSensitivityBulkGWW/VVinclu/Limits_VVinclu_tau21.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_VVVH_tau21_doubleB_newTemplates.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VV_scheme2_tau21_doubleB.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VH_scheme2_tau21_doubleB.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_tau21_doubleB_migrUnc.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VV_scheme2_tau21_doubleB_migrUnc.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VH_scheme2_tau21_doubleB_migrUnc.root"]
title = ["tau21DDT","deepAKWDDT","VVVH tau21DDT+doubleB migrUnc","VV","VH","VVVH deepAK8"] 
files=["debugSensitivityBulkGWW/VVinclu/Limits_VVinclu_tau21.root","results_2016_VVinclu_deepAK8WDDT_noCutTemplates/Limits_BulkGWW_13TeV_2016_VVinclu_deepAK8WDDT_noCutTemplates.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_tau21_doubleB_migrUnc.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VV_scheme2_tau21_doubleB_migrUnc.root","debugSensitivityBulkGWW/VVVH/Limits_BulkGWW_13TeV_2016_VH_scheme2_tau21_doubleB_migrUnc.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8WZH_migrUnc.root"]


#title = ["tau_{21}^{DDT}+doubleB","deepAK8: W 5%, ZH 2%"]
#title = ["tau_{21}^{DDT}+doubleB","deepAK8: W 5%, ZH 5%","deepAK8: W 5%, ZH 2%"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_ZprimeZH_VVVH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_ZprimeZH_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_pseudo40.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_BulkGWW_VVVH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_BulkGWW_VVVH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p05_0p10_DDT_defaultMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p05_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_ZprimeZH_VVVH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p05_0p10_DDT_defaultMap/Limits_ZprimeZH_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p05_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_ZprimeZH_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_pseudo40.root"]

#title = ["VH DDT","VV DDT","VVVH DDT","VH doubleB","VV doubleB","VVVH doubleB"]
#files = ["results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VV_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_BulkGWW_VH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_BulkGWW_VV_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_BulkGWW_VVVH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root"]
#files = ["results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_ZprimeZH_13TeV_2016_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_pseudo40.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_ZprimeZH_13TeV_2016_VV_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_pseudo40.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/Limits_ZprimeZH_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_pseudo40.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_ZprimeZH_VH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_ZprimeZH_VV_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_scheme2/Limits_ZprimeZH_VVVH_13TeV_2016_scheme2_doubleB_0p91_0p86_pseudo80.root"]




#title = ["VH","VV ","VVVH"]
#files = ["results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_SDcorrMaps/Limits_BulkGWW_13TeV_2016_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_SDcorrMaps/Limits_BulkGWW_13TeV_2016_VV_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_SDcorrMaps/Limits_BulkGWW_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root"]
#files = ["results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_SDcorrMaps/Limits_ZprimeZH_13TeV_2016_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_SDcorrMaps/Limits_ZprimeZH_13TeV_2016_VV_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root","results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_SDcorrMaps/Limits_ZprimeZH_13TeV_2016_VVVH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT.root"]

#title = ["VH","VV","VVVH"]                                                                                                                                                                                                                                                  
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_ZprimeZH_VH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86_pseudo20.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_ZprimeZH_VV_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86_pseudo20.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_ZprimeZH_VVVH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86_pseudo20.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_BulkGWW_VH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_BulkGWW_VV_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_BulkGWW_VVVH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86.root"]



#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86/withoutVHLPLP/Limits_BulkGWW_VV_pseudo_5catHmed_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VV_13TeV_2016_withvhlplp_doubleB_HP0p91_LP0p86.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_BulkGWW_VV_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86/withoutVHLPLP/Limits_BulkGWW_VH_pseudo_5catHmed_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VH_13TeV_2016_withvhlplp_doubleB_HP0p91_LP0p86.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_BulkGWW_VH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86/withoutVHLPLP/Limits_BulkGWW_VVVH_pseudo_5catHmed_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VVVH_13TeV_2016_withvhlplp_doubleB_HP0p91_LP0p86.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_BulkGWW_VVVH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86.root"]

#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86/withoutVHLPLP/Limits_ZprimeZH_VVVH_pseudo20_5catHmed_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VVVH_13TeV_2016_withvhlplp_doubleB_HP0p91_LP0p86_pseudo20.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_ZprimeZH_VVVH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86_pseudo20.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86/withoutVHLPLP/Limits_ZprimeZH_VH_pseudo20_5catHmed_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VH_13TeV_2016_withvhlplp_doubleB_HP0p91_LP0p86_pseudo20.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_ZprimeZH_VH_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86_pseudo20.root"] 
#files = ["results_2016_VV_VH_doubleB_HP0p91_LP0p86/withoutVHLPLP/Limits_ZprimeZH_VV_pseudo20_5catHmed_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VV_13TeV_2016_withvhlplp_doubleB_HP0p91_LP0p86_pseudo20.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86_novhlplp/Limits_ZprimeZH_VV_13TeV_2016_novhlplp_doubleB_HP0p91_LP0p86_pseudo20.root"] 


#title = ["5 cat, loose H LP","5 cat, medium H LP","2VV2VH, medium H LP","2VV2VH,  loose H LP"]
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_BulkGWW_VV_fixedVjest_noTT_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VV_pseudo_5catHmed_13TeV_2016.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_13TeV_2016_VV_2VV2VH.root","results_2016_2VV_2VH_doubleB_HP0p92_LP0p7/Limits_BulkGWW_VV_2VV2VH_13TeV_2016.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_BulkGWW_VH_fixedVjest_noTT_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VH_pseudo_5catHmed_13TeV_2016.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_13TeV_2016_VH_2VV2VH.root","results_2016_2VV_2VH_doubleB_HP0p92_LP0p7/Limits_BulkGWW_VH_2VV2VH_13TeV_2016.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_BulkGWW_VVVH_fixedVjest_noTT_13TeV_2016.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VVVH_pseudo_5catHmed_13TeV_2016.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_VVVH_13TeV_2016_2VV2VH.root","results_2016_2VV_2VH_doubleB_HP0p92_LP0p7/Limits_BulkGWW_VVVH_2VV2VH_13TeV_2016.root"]

#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VVVH_JenFix.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VVVH_pseudo20_5catHmed_13TeV_2016.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VVVH_JenFix_2VV2VH.root","results_2016_2VV_2VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VVVH_pseudo20_13TeV_2016.root"]                                  
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VH_JenFix.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VH_pseudo20_5catHmed_13TeV_2016.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VH_JenFix_2VV2VH.root","results_2016_2VV_2VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VH_pseudo20_13TeV_2016.root"]                                  
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VV_JenFix.root","results_2016_VV_VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VV_pseudo20_5catHmed_13TeV_2016.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VV_JenFix_2VV2VH.root","results_2016_2VV_2VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VV_pseudo20_13TeV_2016.root"]                                  





#title = ["no MVV corr","no MVV corr, 2VV2VH","Jen Fix","Jen Fix, 2VV2VH"]
#files = ["Limits_ZprimeZH_VVVH_nocorrMVV.root","Limits_ZprimeZH_VVVH_nocorrMVV_2VV2VH.root","Limits_ZprimeZH_VVVH_JenFix.root","Limits_ZprimeZH_VVVH_JenFix_2VV2VH.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VV_nocorrMVV.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VV_nocorrMVV_2VV2VH.root","results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VV_JenFix_part.root","results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_ZprimeZH_VV_JenFix_2VV2VH.root"]
#files = ["results_2016_VV_VH_doubleB_HP0p92_LP0p7/Limits_ZprimeZH_VH_nocorrMVV.root","Limits_ZprimeZH_VH_nocorrMVV_2VV2VH.root","Limits_ZprimeZH_VH_JenFix.root","Limits_ZprimeZH_VH_JenFix_2VV2VH.root"]


#title = ["2 GeV bins","4 GeV bins","8 GeV bins","16 GeV bins"]
#files = ["results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_13TeV_2016_VV_2VV2VH.root","Limits_BulkGWW_VV_13TeV_2016_2VV2VH_pseudo40.root","Limits_BulkGWW_VV_13TeV_2016_2VV2VH_pseudo20.root","Limits_BulkGWW_VV_13TeV_2016_2VV2VH_pseudo10.root"]
#files = ["results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/Limits_BulkGWW_13TeV_2016_VH_2VV2VH.root","Limits_BulkGWW_VH_13TeV_2016_2VV2VH_pseudo40.root","Limits_BulkGWW_VH_13TeV_2016_2VV2VH_pseudo20.root","Limits_BulkGWW_VH_13TeV_2016_2VV2VH_pseudo10.root"]
#files = ["Limits_BulkGWW_VVVH_13TeV_2016_2VV2VH.root","Limits_BulkGWW_VVVH_13TeV_2016_2VV2VH_pseudo40.root","Limits_BulkGWW_VVVH_13TeV_2016_2VV2VH_pseudo20.root","Limits_BulkGWW_VVVH_13TeV_2016_2VV2VH_pseudo10.root"]




# titleY = "#sigma x BR(G_{Bulk} #rightarrow ZZ) (pb)  "
# oname= "BulkGZZ"
# title = ["HPLP","HPHP","HPHP+HPLP","B2G-17-001"]
# files = ["LIMITS_DDT_latest/ZZ/HPLP/Limits_BulkGZZ_HPLP_13TeV.root","LIMITS_DDT_latest/ZZ/HPHP/Limits_BulkGZZ_HPHP_13TeV.root","LIMITS_DDT_latest/ZZ/combined/Limits_BulkGZZ_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGZZ_13TeV.root"]

# titleY = "#sigma x BR(W' #rightarrow WZ) (pb)  "
# oname= "WprimeWZ"
# title = ["HPLP","HPHP","HPHP+HPLP","B2G-17-001"]
# files = ["LIMITS_DDT_latest/WZ/HPLP/Limits_WprimeWZ_HPLP_13TeV.root","LIMITS_DDT_latest/WZ/HPHP/Limits_WprimeWZ_HPHP_13TeV.root","LIMITS_DDT_latest/WZ/combined/Limits_WprimeWZ_13TeV.root","limits_b2g17001/Limits_b2g17001_WZ_13TeV.root"]
# oname= "BulkGWW"
# title = ["HPHP","B2G-17-001"]
# files = ["LIMITS_DDT_latest/newSigFits/Limits_BulkGWW_HPHP_13TeV.root","limits_b2g17001/Limits_b2g17001_BulkGWW_13TeV.root"]

#titleY = "#sigma x BR(Z' #rightarrow WW) (pb)  "
#oname= "Zprime"  
#title = ["Tight (DDT<0.43)","Loose (DDT<0.49)"]
#files = ["/afs/cern.ch/user/t/thaarres/public/forJen/newDDT/limits.root","/afs/cern.ch/user/t/thaarres/public/forJen/looseDDT/limits.root"]



# title = ["3D HPHP","3D HPHP DDT"]
# files = ["Limits_BulkGWW_HPHP_13TeV.root","Limits_BulkGWW_HPHP_13TeV_ddt.root"]
#
# title = ["Expected 2017","B2G-17-001"]
# files = ["HPLP_noOPTPT2/Limits2.root","limits_b2g17001/Limits_b2g17001_WZ_13TeV.root"]
#
# title = ["Expected 2017","B2G-17-001"]
# files = ["HPLP_noOPTPT2/Limits2.root","limits_b2g17001/Limits_b2g17001_WZ_13TeV.root"]
#
# title = ["HPHP","HPLP","HPHP+HPLP"]
#
# files = ["LIMITS_DDT_latest/HPHP/HPHP.root","LIMITS_DDT_latest/LPLP/HPLP.root","LIMITS_DDT_latest/combined/combined.root"]
# title = ["Nominal","p_{T}/m_{VV}>0.4"]
# files = ["LIMITS_NOM/Limits_BulkGWW_HPHP_13TeV.root","LIMITS_VCUT/Limits_BulkGWW_HPHP_13TeV.root"]


#atlas_mps    = [1200,1500,2000,2500,3000,3500,4000,4500,5000]
#atlas_BulkZZ = [200, 18, 4.8, 2.2, 1.2, 0.83, 0.60, 0.50, 0.40]; atlas_BulkZZ = [x * 0.001 for x in atlas_BulkZZ]; print "atlas_BulkZZ",atlas_BulkZZ;
#atlas_BulkWW = [52 , 13, 4.0, 1.9, 1.2, 0.82, 0.62, 0.52, 0.50]; atlas_BulkWW = [x * 0.001 for x in atlas_BulkWW]; print "atlas_BulkWW",atlas_BulkWW;
#atlas_Wprime = [200, 12, 3.0, 1.5, 1.0, 0.79, 0.52, 0.42, 0.38]; atlas_Wprime = [x * 0.001 for x in atlas_Wprime]; print "atlas_Wprime",atlas_Wprime;
#atlas_Zprime = [180,  9, 3.1, 1.7, 1.0, 0.71, 0.52, 0.40, 0.37]; atlas_Zprime = [x * 0.001 for x in atlas_Zprime]; print "atlas_Zprime",atlas_Zprime;


#vatlas_mps   = array("f",atlas_mps   )
 
#if   oname.find("BulkGZZ")!=-1: lims  = array("f",atlas_BulkZZ)
#elif oname.find("BulkGWW") !=-1: lims = array("f",atlas_BulkWW)
#elif oname.find("Zprime") !=-1: lims  = array("f",atlas_Zprime)
#elif oname.find("Wprime") !=-1: lims  = array("f",atlas_Wprime)
#atlas_lim = ROOT.TGraph( 9 , vatlas_mps, lims)

scaleLimits = {}
masses = array('d',[i*100. for i in range(8,60)])

if scaleBR:
  x, y = array( 'd' ), array( 'd' )
  fin = ROOT.TFile.Open("results_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMap/workspace_JJ_BulkGWW_VV_13TeV_2016_VV_VH_scheme2_deepAK8_W_0p05_0p10_ZHbb_0p02_0p10_DDT_nominalMaps_fullStats_pseudo80.root","READ")
  #fin = ROOT.TFile.Open("results_2016_2VV_2VH_doubleB_HP0p91_LP0p86/workspace_JJ_BulkGWW_VV_13TeV_2016_2VV2VH.root","READ")
  w = fin.Get("w")


  for m in masses:
    scaleLimits[str(int(m))] =0.001 
    argset = ROOT.RooArgSet()
    MH=w.var("MH")
    argset.add(MH)
    MH.setVal(m)

    func = w.function('BulkGWW_JJ_VV_HPHP_13TeV_2016_sigma')
    scaleLimits[str(int(m))] = func.getVal(argset)
else:
  for m in masses:
    #scaleLimits[str(int(m))] = 1.*0.001 #NB this is a quick fix for ZprimeZH!
    scaleLimits[str(int(m))] = 1.*0.001*0.584 #multiply by H BR

leg = getLegend()
leg.AddEntry(0,"Exp. limits","")
leg.AddEntry(0,"","")
tgraphs = []
for t,fname in zip(title,files):
	f=ROOT.TFile(fname)
        print fname
	limit=f.Get("limit")
	data={}
	for event in limit:
		if float(event.mh)<options.minX or float(event.mh)>options.maxX:
		    continue
		
		if not (event.mh in data.keys()):
		    data[event.mh]={}

                print "event.mh ",event.mh

                lim = event.limit*scaleLimits[str(int(event.mh))]
#		lim = event.limit*0.001
		#if fname.find("b2g17001")!=-1: lim = event.limit*0.01
		#if fname.find("b2g17001")!=-1 and oname.find("BulkGZZ")!=-1: lim = event.limit*0.01/(0.6991*0.6991)
		#if fname.find("b2g17001")!=-1 and oname.find("Wprime")!=-1: lim = event.limit*0.01/(0.6991*0.676)
		if event.quantileExpected>0.49 and event.quantileExpected<0.51:            
                  print "event.limit ",event.limit
                  print "scaleLimits[str(int(event.mh))]  ",scaleLimits[str(int(event.mh))]  
 
                  print "lim ",lim
                  data[event.mh]['exp']=lim
		
		
		
	line_plus1=ROOT.TGraph()
	line_plus1.SetName(f.GetName().replace(".root",""))



	N=0
	for mass,info in data.iteritems():
	    print 'Setting mass',mass,info

	    if not ('exp' in info.keys()):
	        print 'Incomplete file'
	        continue
    

	    line_plus1.SetPoint(N,mass,info['exp'])
	    N=N+1
	
	line_plus1.Sort()    
	tgraphs.append(line_plus1)  
	leg.AddEntry(line_plus1,t,"L")

MASS, limits_b2g17_001 = array( 'd' ), array( 'd' )
MASS=[    
  1200.,
  1300.,
  1400.,
  1500.,
  1600.,
  1700.,
  1800.,
  1900.,
  2000.,
  2100.,
  2200.,
  2300.,
  2400.,
  2500.,
  2600.,
  2700.,
  2800.,
  2900.,
  3000.,
  3100.,
  3200.,
  3300.,
  3400.,
  3500.,
  3600.,
  3700.,
  3800.,
  3900.,
  4000.,
  4100.,
  4200.,
  4300.]
print MASS
limits_b2g17_001 = [
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
  0.0007476807]
print limits_b2g17_001
VV16= ROOT.TGraph(32,np.array(MASS),np.array(limits_b2g17_001))
VV16.SetName("VV16")
VV16.SetTitle("");
#VV16.SetFillColor(1);
VV16.SetLineColor(600);
VV16.SetLineStyle(5);
VV16.SetLineWidth(3);
VV16.SetMarkerStyle(20);
if(plotVV1D): leg.AddEntry(VV16,"B2G-17-001","L")


MASSLONG, limits_b2g18_001_2016 = array( 'd' ), array( 'd' )
MASSLONG=[
   1200.,
   1300.,
   1400.,
   1500.,
   1600.,
   1700.,
   1800.,
   1900.,
   2000.,
   2100.,
   2200.,
   2300.,
   2400.,
   2500.,
   2600.,
   2700.,
   2800.,
   2900.,
   3000.,
   3100.,
   3200.,
   3300.,
   3400.,
   3500.,
   3600.,
   3700.,
   3800.,
   3900.,
   4000.,
   4100.,
   4200.,
   4300.,
   4400.,
   4500.,
   4600.,
   4700.,
   4800.,
   4900.,
   5000.,
   5100.,
   5200.]
limits_b2g18_001_2016=[
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
     0.0005175781]
VV3D16= ROOT.TGraph(41,np.array(MASSLONG),np.array(limits_b2g18_001_2016))
VV3D16.SetName("VV3D16")
VV3D16.SetTitle("");
#VV3D16.SetFillColor(1);
VV3D16.SetLineColor(9);
VV3D16.SetLineStyle(2);
VV3D16.SetLineWidth(3);
VV3D16.SetMarkerStyle(20);
if(plotVV3D2016): leg.AddEntry(VV3D16,"B2G-18-002 2016","L")

limits_b2g18_001=[
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
     0.0002675781]
VV3D= ROOT.TGraph(41,np.array(MASSLONG),np.array(limits_b2g18_001))
VV3D.SetName("VV3D")
VV3D.SetTitle("");
#VV3D.SetFillColor(1);
VV3D.SetLineColor(429);
VV3D.SetLineStyle(1);
VV3D.SetLineWidth(3);
VV3D.SetMarkerStyle(20);
if plotVV3D: leg.AddEntry(VV3D,"B2G-18-001","L")


limits_VVinclu_2016_data=[
     0.01993091,
     0.01577789,
     0.01192519,
     0.009051901,
     0.007213227,
     0.00590865,
     0.005050781,
     0.004361068,
     0.003757451,
     0.003298853,
     0.002893604,
     0.002552105,
     0.002275018,
     0.002052211,
     0.001864545,
     0.001690853,
     0.001548826,
     0.001425133,
     0.001311619,
     0.001203569,
     0.001094871,
     0.0009964248,
     0.0009057579,
     0.0008164299,
     0.0007329666,
     0.0006602379,
     0.0006070422,
     0.0005742371,
     0.0005510431,
     0.0005533515,
     0.0005693425]
VVinclu3D2016= ROOT.TGraph(31,np.array(MASSLONG),np.array(limits_VVinclu_2016_data))
VVinclu3D2016.SetName("VVinclu3D2016")
VVinclu3D2016.SetTitle("");
#VVinclu3D2016.SetFillColor(1);
VVinclu3D2016.SetLineColor(429);
VVinclu3D2016.SetLineStyle(5);
VVinclu3D2016.SetLineWidth(3);
VVinclu3D2016.SetMarkerStyle(20);
if plotVV3D2016data: leg.AddEntry(VVinclu3D2016,"VV inclu data 2016","L")

limits_VVinclu_2016_pseudodata=[
     0.01822102,
     0.0144033,
     0.0109042,
     0.008351289,
     0.006710813,
     0.005565124,
     0.004776116,
     0.00412932,
     0.003570327,
     0.003150351,
     0.002766822,
     0.002446646,
     0.002191322,
     0.00199614,
     0.001819269,
     0.001648881,
     0.001513824,
     0.001392744,
     0.001287057,
     0.001188285,
     0.001084077,
     0.0009872833,
     0.0008976604,
     0.0008090841,
     0.0007234968,
     0.0006534662,
     0.0006025232,
     0.0005769268,
     0.0005632343,
     0.0005681227,
     0.000584583]
VVinclu3D2016pseudo= ROOT.TGraph(31,np.array(MASSLONG),np.array(limits_VVinclu_2016_pseudodata))
VVinclu3D2016pseudo.SetName("VVinclu3D2016pseudo")
VVinclu3D2016pseudo.SetTitle("");
#VVinclu3D2016pseudo.SetFillColor(1);
VVinclu3D2016pseudo.SetLineColor(427);
VVinclu3D2016pseudo.SetLineStyle(5);
VVinclu3D2016pseudo.SetLineWidth(3);
VVinclu3D2016pseudo.SetMarkerStyle(20);
if plotVV3D2016pseudodata: leg.AddEntry(VVinclu3D2016pseudo,"VV inclu pseudodata 2016","L")


MASSSHORT=[1500.,2000.,4000.]
limits_VH_2016=[0.03,0.005,0.001]
VH2016=ROOT.TGraph(3,np.array(MASSSHORT),np.array(limits_VH_2016))
VH2016.SetName("VH2016")
VH2016.SetTitle("");
#VH2016.SetFillColor(1);                                                                                                                                                                                                         
VH2016.SetLineColor(427);
VH2016.SetLineStyle(5);
VH2016.SetLineWidth(3);
VH2016.SetMarkerStyle(20);
if plotVH2016: leg.AddEntry(VH2016,"B2G-17-002","L")




#plotting information
H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref
c=ROOT.TCanvas("c","c",50,50,W,H)
c.SetFillColor(0)
c.SetBorderMode(0)
c.SetFrameFillStyle(0)
c.SetFrameBorderMode(0)
c.SetLeftMargin( L/W )
c.SetRightMargin( R/W )
c.SetTopMargin( T/H )
c.SetBottomMargin( B/H )
c.SetTickx(0)
c.SetTicky(0)
c.GetWindowHeight()
c.GetWindowWidth()
c.SetLogy()
c.SetGrid()
c.SetLogy()
	
frame=c.DrawFrame(options.minX,options.minY,options.maxX,options.maxY)
	
ROOT.gPad.SetTopMargin(0.08)
frame.GetXaxis().SetTitle(options.titleX)
frame.GetXaxis().SetTitleOffset(0.9)
frame.GetXaxis().SetTitleSize(0.05)

frame.GetYaxis().SetTitle(titleY)
frame.GetYaxis().SetTitleSize(0.05)
frame.GetYaxis().SetTitleOffset(1.15)





c.cd()
frame.Draw()
#cols  = [42,46,49,32,36,39]*3
#tline = [10,9,1,10,9,1]*3
cols  = [432,636,632,627,610,615,608]*3
tline = [1,1,1,1,2,2,2]*3
#cols  = [42,46,49,1]*3
#tline = [10,9,1,2]*3

if plotVV1D : VV16.Draw("Lsame")
if plotVV3D2016 : VV3D16.Draw("Lsame")
if plotVV3D: VV3D.Draw("Lsame")
if plotVV3D2016data: VVinclu3D2016.Draw("Lsame")
if plotVV3D2016pseudodata: VVinclu3D2016pseudo.Draw("Lsame")
if plotVH2016: VH2016.Draw("Lsame")

for i,g in enumerate(tgraphs):
	g.SetLineStyle(tline[i])
	g.SetLineColor(cols[i])
	g.SetLineWidth(2)
	g.Draw("Lsame")
# atlas_lim.Draw("P same")
c.SetLogy(options.log)
#c.Draw()
leg.Draw("same")
cmslabel_prelim(c,options.period,11)

#c.Update()
#c.RedrawAxis()

c.SaveAs("compareLimits_"+oname+".png")
c.SaveAs("compareLimits_"+oname+".pdf")
c.SaveAs("compareLimits_"+oname+".root")
# c.SaveAs(options.output.replace(".root","")+".pdf")
# c.SaveAs(options.output.replace(".root","")+".C")
sleep(2)
f.Close()


