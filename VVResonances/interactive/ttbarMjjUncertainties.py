# Script to evaluate systematic uncertainties for the fit of the mjj ttbar distributions
import ROOT
from optparse import OptionParser
import sys,os
import cuts 
import json

def getParameterFromJson(jsonFile,variablename):
    #open json                                                                                                                                                                                                                                                              
    f=open(jsonFile)
    info=json.load(f)
    print variablename
    param=info[variablename]
    print param 
    return param

def CalculateUnc(p1,p2):
    if p1 !=0:
        unc = abs(p1-p2)/p1
    else: 
        print " cannot divide by 0!! "
        unc = 0

    print unc
    return unc

if __name__=="__main__":

    year='2016'
    directory='results_'+year
    ttbarComponents=['nonresT','resT','resTnonresT','resTresW','resW','resWnonresT']
    unc = {}
    for t in ttbarComponents:
        c3w = getParameterFromJson(directory+'/JJ_'+t+year+'_TTJets_MVV_NP.json',"c3")
        c3 = getParameterFromJson(directory+'/noreweight_JJ_'+t+year+'_TTJets_MVV_NP.json',"c3")
        unc.update({t:CalculateUnc(c3w,c3)})

    print unc

    f=open(directory+'/JJ_'+year+'_TTJets_MjjUnc_NP.json',"w")
    json.dump(unc,f)



