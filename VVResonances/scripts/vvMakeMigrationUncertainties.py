#!/usr/bin/env python
############# script to estimate migration uncertainties for the full hadronic VV/VH -> 4q analysis ###############
############# base calculation on measuremnt of sf uncertainties for the W/H-tagging scale factors  ###############

# for the moment there are the same scale factors for W-tagging and H-tagging, for 2018 i put the same as for 2017 for now!
import ROOT
import optparse
import sys,os,time
import json
from array import array
ROOT.gROOT.ProcessLine("struct rootint { Int_t ri;};")
from ROOT import rootint
ROOT.gROOT.ProcessLine("struct rootfloat { Float_t rf;};")
from ROOT import rootfloat
ROOT.gROOT.ProcessLine("struct rootlong { Long_t li;};")
from ROOT import rootlong
sys.path.insert(0, "../interactive/")
import cuts
from rootpy.tree import CharArrayCol

parser = optparse.OptionParser()
parser.add_option("-y","--year",dest="year",default='2016',help="year of data taking")
parser.add_option("-s","--samples",dest="samples",help="sample to calculate the migration unc.",default='ZprimeToZh')
parser.add_option("-d","--directory",dest="directory",help="directory with signal samples",default="migrationunc/")
parser.add_option("-m","--minMX",dest="minMX",type=float,help="mVV variable",default=1200)
parser.add_option("-M","--maxMX",dest="maxMX",type=float, help="mVV variable",default=8000)
parser.add_option("-c","--categories",dest="categories",help="list of considered categories",default='VH_HPHP,VV_HPHP,VH_LPHP,VH_HPLP,VV_HPLP')
parser.add_option("-t","--tags",dest="tags",help="list of tags",default='H_tag,V_tag,top_tag')
parser.add_option("--isSignal",dest="isSignal",action="store_true", help="is signal?")
parser.add_option("-o","--output",dest="output",help="Output",default='ZprimeZH')
(options,args) = parser.parse_args()



def calculateMigration(tree,uncertainty_var,category):
    print " CAT ",category
    events   = 0
    events_wup = 0
    events_wdown = 0
    # calculate effect of sf uncertainty for one particular category 
    # loop through tree
    for e in tree:
        # apply category cuts to the tree
        if e.category.find(category)==-1: continue
        events += e.genWeight*e.puWeight*e.SF
        # apply weight of uncertainty up/down variation to events with real W or H boson and top mistag correction
        # apply also weight for up/down variation of the SF
        # count overall weighted events in the category
        if uncertainty_var == "V_tag":
            events_wup +=e.genWeight*e.puWeight*e.CMS_eff_vtag_sf_up
        elif uncertainty_var == "H_tag":
            events_wup +=e.genWeight*e.puWeight*e.CMS_eff_htag_sf_up
        elif uncertainty_var == "top_tag":
            events_wup +=e.genWeight*e.puWeight*e.CMS_mistag_top_sf_up
        else:
            print " ATTENTION! unknown uncertainty_var ",uncertainty_var
        if uncertainty_var == "V_tag":
            events_wdown +=e.genWeight*e.puWeight*e.CMS_eff_vtag_sf_down
        elif uncertainty_var == "H_tag":
            events_wdown +=e.genWeight*e.puWeight*e.CMS_eff_htag_sf_down
        elif uncertainty_var == "top_tag":
            events_wdown +=e.genWeight*e.puWeight*e.CMS_mistag_top_sf_down
        else:
            print " ATTENTION! unknown uncertainty_var ",uncertainty_var
    # return list with number of weighted, weighted up and down events in the category given by category cuts
    print " event ",events
    print "up ",events_wup
    print " down ", events_wdown
    return [events, events_wup,events_wdown]


def printresult(res,cats):
    masses=[]
    for key in res.keys():
        if (key.split('.')[1]).find(cats[0])!=-1:
            masses.append(int(key.split('.')[0]))

    c = 'Sample '
    for cat in cats:
        c+='              '
        c+=cat 
    print c
    for m in sorted(masses):
        tmp =str(m)+'  '
        for cat in cats:
            if res[str(m)+'.'+cat][0]!=0 :
                nom = res[str(m)+'.'+cat][0]
                up = res[str(m)+'.'+cat][1]
                down = res[str(m)+'.'+cat][2]
                tmp+= str(down/float(nom))+' / '+str(up/nom)
            #print up
            #print nom
            tmp+='   '
        print tmp

def printresultbkg(res,cats):
    masses = []
    for key in res.keys():
        if (key.split('.')[1]).find(cats[0])!=-1:
            masses.append(key.split('.')[0])

    c = 'mass '
    for cat in cats:
        c+='              '
        c+=cat
    print c
    for m in sorted(masses):
        tmp =str(m)+'  '
        for cat in cats:
            if res[str(m)+'.'+cat][0]!=0 :
                nom = res[str(m)+'.'+cat][0]
                up = res[str(m)+'.'+cat][1]
                down = res[str(m)+'.'+cat][2]
                tmp+= str(down/float(nom))+' / '+str(up/nom)
            #print up
            #print nom
            tmp+='   '
        print tmp

        
def calcfinalUnc(final,tag,cats):
    data={}
    savekeys=[]
    for k in final.keys():
        if k.find(tag)==-1: continue
        savekeys.append(k)
    masses=[]
    res=final[savekeys[0]]
    for key in res.keys():
        if (key.split('.')[1]).find(cats[0])!=-1:
            masses.append(key.split('.')[0])
    tmplistu = []
    tmplistd = []
    ratiodown ={}
    ratioup ={}
    c = 'Sample '
    for cat in cats:
        c+='              '
        c+=cat 
        tmplistd.append(0.)
        tmplistu.append(0.)
    print c



    print " sorted(masses) ",sorted(masses)
    for m in sorted(masses):
        tmp =str(m)+'  '
        i=0
        for cat in cats:
            if res[str(m)+'.'+cat][0]!=0 :
                nom= res[str(m)+'.'+cat][0]
                upvar = res[str(m)+'.'+cat][1]
                downvar = res[str(m)+'.'+cat][2]
                ratiodown.update({m:float(downvar)/float(nom)})
                ratioup.update({m :float(upvar)/float(nom)})
                tmp+= str(round(float(ratiodown[m]),2))+' / '+str(round(float(ratioup[m]),2))
                if options.isSignal==True:
                    tmplistu[i]+= ratioup[m]
                    tmplistd[i]+= ratiodown[m]
                i+=1
            tmp+='   '
            
        print tmp
    i=0
    for c in cats:
        if c == "VV_NPHP":c="VV_NPHP_control_region"
        if options.isSignal==True:
            #print " averaging on masses for signal???"
            data[c+'_up']= round(tmplistu[i]/float(len(masses)),2)
            data[c+'_down']= round(tmplistd[i]/float(len(masses)),2)
        else:
            for m in masses:
                #print " is it working ? ", str(m)
                #print " ratioup[m]  ",ratioup[m] 
                data[str(m)+'.'+c+'_up']= round(ratioup[m],2)
                data[str(m)+'.'+c+'_down']= round(ratiodown[m],2)
        i+=1

    return data



if __name__=="__main__":
    # calculate migration uncertainty for all categories
    # up variation of W-Tag HP Sf -> down variation of W-tag LP sf, down variation of anti W-tag HP category
    # do it for all the categories and for W-tag HP up/down, W-tag LP up/down, H-tag HP up/down, H-tag LP up/down
    # and for the combination of: W-tag + H-tag HP up/down and LP up/down
    
    ######### first apply the usual acceptance cuts to the trees ####################
    data ={}
    years = options.year.split(",")
    directory = options.directory
    categories=options.categories.split(",")
    tags=options.tags.split(",")
    sampleTypes = options.samples.split(",")
    total = {}
    contrib =["resT","resW","nonresT","resTnonresT","resWnonresT","resTresW"]
    mappdf = {"resT":"TTJetsTop","resW":"TTJetsW","nonresT":"TTJetsNonRes","resTnonresT":"TTJetsTNonResT","resWnonresT":"TTJetsWNonResT","resTresW":"TTJetsResWResT"}


    print " Doing migration uncertainties! DID YOU EVALUTE THE SF BEFORE?"
    jsonfilename = {}
    for year in years:
        chain = ROOT.TChain('signalregion')
        print "************     year ",year
        ctx  = cuts.cuts("init_VV_VH.json",year,"random_dijetbins")
        for filename in os.listdir(directory):
            for sampleType in sampleTypes:
                if filename.find(sampleType)!=-1 and filename.find(year)!=-1:
                    if filename.find(".")==-1: continue
                    if filename.find("VBF")!=-1 and options.sample.find("VBF")==-1: continue
                    fnameParts=filename.split('.')
                    fname=fnameParts[0]
                    print "fname ",fname
                    ext=fnameParts[1]
                    if ext.find("root") ==-1: continue
                    if options.isSignal == True:
                        print " is signal !"
                        mass = float(fname.split('_')[-1])
                        if mass <options.minMX or mass > options.maxMX: continue
                        else: sampleType=sampleType+"narrow_"+fname.split('_')[-2]
                    completename=directory+sampleType+"_"+year+".root"
                    FileIn = ROOT.TFile(completename,"READ")
                    chain.Add(completename)
                    print " entries ",chain.GetEntries()
        print " total Entries ",chain.GetEntries()


        final = {}
        splitstr = options.output
        for tag in tags:
            result = {}
            #print finaltree.Print()
            for cat in categories:
                if splitstr.find("TT") == -1:
                    result[splitstr+'.'+cat] = calculateMigration(chain,tag,cat)
                else:
                    for con in contrib:
                        tmpname = "tmp_"+time.strftime("%Y%m%d-%H%M%S")
                        outfile = ROOT.TFile(tmpname+'.root','RECREATE')
                        print " %%%%%%%    "+con+"     %%%%%%%%%"
                        ttcomp = chain.CopyTree(ctx.cuts[con])
                        print ttcomp.GetEntries()
                        ttcomp.Write()
                        result[mappdf[con]+'.'+cat] = calculateMigration(ttcomp,tag,cat)
                        os.system("rm "+tmpname+".root")
            print '###################   '+tag+'    ######################'

            #if splitstr.find("Jets")!=-1 or splitstr.find("TT")!=-1 : printresultbkg(result,categories)
            #else: printresult(result,categories)
            printresultbkg(result,categories)
            final[tag]=result
            print "************** FINAL ",final
        total[year]=final

        print 'CMS_VV_JJ_DeepJet_Htag_eff'
        data[year] = {splitstr+'_'+'CMS_VV_JJ_DeepJet_Htag_eff' : calcfinalUnc(final,'H_tag',categories)}
        print 'CMS_VV_JJ_DeepJet_Vtag_eff'
        data[year].update( {splitstr+'_'+'CMS_VV_JJ_DeepJet_Vtag_eff' : calcfinalUnc(final,'V_tag',categories)})
        print 'CMS_VV_JJ_DeepJet_TOPtag_mistag'
        data[year].update({splitstr+'_'+'CMS_VV_JJ_DeepJet_TOPtag_mistag' : calcfinalUnc(final,'top_tag',categories)})

        jsonfilename[year] = 'migrationunc_'+splitstr+'_'+year+'.json'
        with open(jsonfilename[year], 'w') as outfile:
            json.dump(data[year], outfile)


    if len(years) == 3:
        print "#######################################      Making Run2 combination by average weighted by lumi      ##############################"
        print " All years uncertainties "
        print total
        unc_Run2 = {}
        for tag in tags:
            unc_Run2[tag]={}
            for cat in categories:
                n = 0
                u = 0
                d = 0
                for year in years:
                    if splitstr.find("TT") == -1:
                        n += total[year][tag][splitstr+'.'+cat][0]*ctx.lumi[year]
                        u += total[year][tag][splitstr+'.'+cat][1]*ctx.lumi[year]
                        d += total[year][tag][splitstr+'.'+cat][2]*ctx.lumi[year]
                    else:
                        for con in contrib:
                            n += total[year][tag][mappdf[con]+'.'+cat][0]*ctx.lumi[year]
                            u += total[year][tag][mappdf[con]+'.'+cat][1]*ctx.lumi[year]
                            d += total[year][tag][mappdf[con]+'.'+cat][2]*ctx.lumi[year]

                if  unc_Run2[tag] == None:
                    if splitstr.find("TT") == -1:
                        unc_Run2[tag] = {splitstr+'.'+cat : [n,u,d] }
                    else:
                        for con in contrib:
                            unc_Run2[tag] = {mappdf[con]+'.'+cat : [n,u,d] }
                else:
                    if splitstr.find("TT") == -1:
                        unc_Run2[tag].update( {splitstr+'.'+cat : [n,u,d] })
                    else:
                        for con in contrib:
                            unc_Run2[tag].update( {mappdf[con]+'.'+cat : [n,u,d] })

        print " run 2 unc "
        print unc_Run2

        print 'CMS_VV_JJ_DeepJet_Htag_eff'
        data["Run2"] = {splitstr+'_'+'CMS_VV_JJ_DeepJet_Htag_eff' : calcfinalUnc(unc_Run2,'H_tag',categories)}
        print 'CMS_VV_JJ_DeepJet_Vtag_eff'
        data["Run2"].update( {splitstr+'_'+'CMS_VV_JJ_DeepJet_Vtag_eff' : calcfinalUnc(unc_Run2,'V_tag',categories)})
        print 'CMS_VV_JJ_DeepJet_TOPtag_mistag'
        data["Run2"].update({splitstr+'_'+'CMS_VV_JJ_DeepJet_TOPtag_mistag' : calcfinalUnc(unc_Run2,'top_tag',categories)})

        jsonfilename["Run2"] = 'migrationunc_'+splitstr+'_Run2.json'
        with open(jsonfilename["Run2"], 'w') as outfile:
            json.dump(data["Run2"], outfile)


 
