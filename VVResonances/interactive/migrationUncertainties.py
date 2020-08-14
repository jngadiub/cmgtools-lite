############# script to estimate migration uncertainties for the full hadronic VV/VH -> 4q analysis ###############
############# base calculation on measuremnt of sf uncertainties for the W/H-tagging scale factors  ###############

# for the moment there are the same scale factors for W-tagging and H-tagging, for 2018 i put the same as for 2017 for now!
import ROOT
from optparse import OptionParser
import sys,os
import cuts #, HPSF16, HPSF17, LPSF16, LPSF17, dijetbins, HCALbinsMVVSignal
import json



def calculateWeight(e,category,uncertainty_var, uncertainty_num,variation):
    factor =1
    jet1truth = ''
    if e.jj_l1_mergedVTruth==1: 
        jet1truth = 'V'
    if e.jj_l1_mergedHTruth==1 or e.jj_l1_mergedZbbTruth==1: 
        jet1truth = 'H'
    jet2truth = ''
    if e.jj_l2_mergedVTruth==1: jet2truth = 'V'
    if e.jj_l2_mergedHTruth==1 or e.jj_l2_mergedZbbTruth==1: jet2truth = 'H'
    # up variation HP H-tag
    if uncertainty_var.find("H_tag")!=-1 and uncertainty_var.find("HP")!=-1 and variation=="up":
        factor = uncpercategory_HPHtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,uncertainty_num)
    if uncertainty_var.find("H_tag")!=-1 and uncertainty_var.find("HP")!=-1 and variation=="down":
        factor = uncpercategory_HPHtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,-uncertainty_num)
    if uncertainty_var.find("V_tag")!=-1 and uncertainty_var.find("HP")!=-1 and variation=="up":
        factor = uncpercategory_HPVtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,uncertainty_num)
    if uncertainty_var.find("V_tag")!=-1 and uncertainty_var.find("HP")!=-1 and variation=="down":
        factor = uncpercategory_HPVtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,-uncertainty_num)    
    
    if uncertainty_var.find("H_tag")!=-1 and uncertainty_var.find("LP")!=-1 and variation=="up":
        factor = uncpercategory_LPHtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,uncertainty_num)
    if uncertainty_var.find("H_tag")!=-1 and uncertainty_var.find("LP")!=-1 and variation=="down":
        factor = uncpercategory_LPHtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,-uncertainty_num)
        
    if uncertainty_var.find("V_tag")!=-1 and uncertainty_var.find("LP")!=-1 and variation=="up":
        factor = uncpercategory_LPVtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,uncertainty_num)
    if uncertainty_var.find("V_tag")!=-1 and uncertainty_var.find("LP")!=-1 and variation=="down":
        factor = uncpercategory_LPVtag(category,jet1truth,e.jj_l1_jetTag,jet2truth,e.jj_l2_jetTag,-uncertainty_num)    
        
    return factor


def uncpercategory_HPHtag(category,jet1truth,jet1tag,jet2truth,jet2tag,uncertainty):
    # jet1truth = is this H or V jet from MC truth, jet1tag= in which category was this jet tagged f.e. HPHtag
    w = 1.
    if category=='VH_HPHP' or category=='VH_LPHP':
        if (jet1truth=='H') and jet1tag.find('HPHtag')!=-1: w = w*(1+uncertainty)
        if (jet2truth=='H') and jet2tag.find('HPHtag')!=-1: w = w*(1+uncertainty)
    if category=='VV_HPLP' or category=='VH_HPLP' or category=='VH_LPHP' or category=='VV_HPHP':
        if (jet1truth=='H') and jet1tag.find('Vtag')!=-1: w = w*(1-uncertainty)
        if (jet2truth=='H') and jet2tag.find('Vtag')!=-1: w = w*(1-uncertainty)
    
    return w

def uncpercategory_HPVtag(category,jet1truth,jet1tag,jet2truth,jet2tag,uncertainty):
    # jet1truth = is this H or V jet from MC truth, jet1tag= in which category was this jet tagged f.e. HPHtag
    w = 1.
    if category=='VV_HPHP' or category=='VH_HPLP' or category=='VV_HPLP' or category=='VH_HPHP':
        if (jet1truth=='V') and jet1tag.find('HPVtag')!=-1: w = w*(1+uncertainty)
        if (jet2truth=='V') and jet2tag.find('HPVtag')!=-1: w = w*(1+uncertainty)
    if category == 'VH_LPHP' or category=='VH_HPLP' :
        if (jet1truth=='V') and jet1tag.find('Htag')!=-1: w = w*(1-uncertainty)
        if (jet2truth=='V') and jet2tag.find('Htag')!=-1: w = w*(1-uncertainty)
    return w


def uncpercategory_LPVtag(category,jet1truth,jet1tag,jet2truth,jet2tag,uncertainty):
    # jet1truth = is this H or V jet from MC truth, jet1tag= in which category was this jet tagged f.e. HPHtag
    # LP is anti-correlated to HP so here everything that would be + in HP is -
    w = 1.
    if category=='VV_HPLP' or category=='VH_LPHP':
        if (jet1truth=='V') and jet1tag.find('LPVtag')!=-1: w = w*(1-uncertainty)
        if (jet2truth=='V') and jet2tag.find('LPVtag')!=-1: w = w*(1-uncertainty)
    #if category == ''
    #if (jet1truth=='V') and jet1tag.find('Htag')!=-1: w = w*(1+uncertainty)
    #if (jet2truth=='V') and jet2tag.find('Htag')!=-1: w = w*(1+uncertainty)
    return w

def uncpercategory_LPHtag(category,jet1truth,jet1tag,jet2truth,jet2tag,uncertainty):
    # jet1truth = is this H or V jet from MC truth, jet1tag= in which category was this jet tagged f.e. HPHtag
    # LP is anti-correlated to HP so here everything that would be + in HP is -
    w = 1.
    if category=='VH_HPLP' or category=='VH_HPLP':
        if (jet1truth=='H') and jet1tag.find('LPHtag')!=-1: w = w*(1-uncertainty)
        if (jet2truth=='H') and jet2tag.find('LPHtag')!=-1: w = w*(1-uncertainty)
    if category=='VV_HPLP' and category=='VV_HPLP':
        if (jet1truth=='H') and jet1tag.find('Vtag')!=-1: w = w*(1+uncertainty)
        if (jet2truth=='H') and jet2tag.find('Vtag')!=-1: w = w*(1+uncertainty)
    return w


def calculateMigration(tree,uncertainty_var,uncertainty_num,category):
    events   = 0
    events_wup = 0
    events_wdown = 0
    # calculate effect of sf uncertainty for one particular category 
    # loop through tree
    for e in tree:
        # apply category cuts to the tree
        if e.category.find(category)==-1: continue
        events += e.genWeight*e.puWeight
        # apply weight of uncertainty up/down variation to events with real W or H boson
        # apply also weight for up/down variation if only a anti-tag requirement is present ...
        # count overall weighted events in the category
        # count unweighted events in the category
        events_wup += e.genWeight*e.puWeight*calculateWeight(e,category,uncertainty_var, uncertainty_num,'up')
        events_wdown += e.genWeight*e.puWeight*calculateWeight(e,category,uncertainty_var, uncertainty_num,'down')
        
    
    # return list with number of unweighted, weighted events in the category given by category cuts
    return [events, events_wup,events_wdown]

def printresult(res,cats):
    masses=[]
    for key in res.keys():
        if (key.split('.')[1]).find(cats[0])!=-1:
            masses.append(int(key.split('.')[0]))

    c = 'mass '
    for cat in cats:
        c+='              '
        c+=cat 
    print c
    for m in sorted(masses):
        tmp =str(m)+'  '
        for cat in cats:
            if res[str(m)+'.'+cat][0]!=0 :
                tmp+= str(res[str(m)+'.'+cat][1]/float(res[str(m)+'.'+cat][0]))+' / '+str(res[str(m)+'.'+cat][2]/res[str(m)+'.'+cat][0])
            #print res[str(m)+'.'+cat][1]
            #print res[str(m)+'.'+cat][0]
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
                tmp+= str(res[str(m)+'.'+cat][1]/float(res[str(m)+'.'+cat][0]))+' / '+str(res[str(m)+'.'+cat][2]/res[str(m)+'.'+cat][0])
            #print res[str(m)+'.'+cat][1]
            #print res[str(m)+'.'+cat][0]
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
    res2=final[savekeys[1]]
    for key in res.keys():
        if (key.split('.')[1]).find(cats[0])!=-1:
            masses.append(key.split('.')[0])
    tmplistu = []
    tmplistd = []
    c = 'mass '
    for cat in cats:
        c+='              '
        c+=cat 
        tmplistd.append(0.)
        tmplistu.append(0.)
    print c
    
    for m in sorted(masses):
        tmp =str(m)+'  '
        i=0
        for cat in cats:
            if res[str(m)+'.'+cat][0]!=0 and res2[str(m)+'.'+cat][0] != 0:
                tmp+= str(round(res[str(m)+'.'+cat][1]/float(res[str(m)+'.'+cat][0])* res2[str(m)+'.'+cat][1]/float(res2[str(m)+'.'+cat][0]),2))+' / '+str(round(res[str(m)+'.'+cat][2]/res[str(m)+'.'+cat][0]* res2[str(m)+'.'+cat][2]/res2[str(m)+'.'+cat][0],2))
                tmplistu[i]+= res[str(m)+'.'+cat][1]/float(res[str(m)+'.'+cat][0])* res2[str(m)+'.'+cat][1]/float(res2[str(m)+'.'+cat][0])
                tmplistd[i]+= res[str(m)+'.'+cat][2]/res[str(m)+'.'+cat][0]* res2[str(m)+'.'+cat][2]/float(res2[str(m)+'.'+cat][0])
                i+=1
            tmp+='   '
            
        print tmp
    i=0
    for c in cats:
        data[c+'_up']= round(tmplistu[i]/float(len(masses)),2)
        data[c+'_down']= round(tmplistd[i]/float(len(masses)),2)
    
    return data
    
    
if __name__=="__main__":
    # calculate migration uncertainty for all categories
    # up variation of W-Tag HP Sf -> down variation of W-tag LP sf, down variation of anti W-tag HP category
    # do it for all the categories and for W-tag HP up/down, W-tag LP up/down, H-tag HP up/down, H-tag LP up/down
    # and for the combination of: W-tag + H-tag HP up/down and LP up/down
    
    ######### first apply the usual acceptance cuts to the trees ####################
    data ={}
    year = '2016,2017,2018'
    masses = [1200,1400,1600,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000]
    ctx  = cuts.cuts("init_VV_VH.json",year,"random_dijetbins")
    if year != '2016,2017,2018' :
        W_tag_SF_HP = ctx.HPSF_vtag[year]
        W_tag_SF_LP = ctx.LPSF_vtag[year]

        H_tag_SF_HP = ctx.HPSF_htag[year]
        H_tag_SF_LP = ctx.LPSF_htag[year]

        W_tag_unc_HP = ctx.W_tag_unc_HP[year]
        W_tag_unc_LP = ctx.W_tag_unc_LP[year]

        H_tag_unc_HP = ctx.H_tag_unc_HP[year]
        H_tag_unc_LP = ctx.H_tag_unc_LP[year]

    else:
        years = year.split(",")
        W_tag_SF_HP = 0
        W_tag_SF_LP = 0

        H_tag_SF_HP = 0
        H_tag_SF_LP = 0

        W_tag_unc_HP = 0
        W_tag_unc_LP = 0

        H_tag_unc_HP = 0
        H_tag_unc_LP = 0

        for y in years:

            W_tag_SF_HP += ctx.HPSF_vtag[y]*ctx.lumi[y]/ctx.lumi["Run2"]
            W_tag_SF_LP += ctx.LPSF_vtag[y]*ctx.lumi[y]/ctx.lumi["Run2"]

            H_tag_SF_HP += ctx.HPSF_htag[y]*ctx.lumi[y]/ctx.lumi["Run2"]
            H_tag_SF_LP += ctx.LPSF_htag[y]*ctx.lumi[y]/ctx.lumi["Run2"]

            W_tag_unc_HP += ctx.W_tag_unc_HP[y]*ctx.lumi[y]/ctx.lumi["Run2"]
            W_tag_unc_LP += ctx.W_tag_unc_LP[y]*ctx.lumi[y]/ctx.lumi["Run2"]

            H_tag_unc_HP += ctx.H_tag_unc_HP[y]*ctx.lumi[y]/ctx.lumi["Run2"]
            H_tag_unc_LP += ctx.H_tag_unc_LP[y]*ctx.lumi[y]/ctx.lumi["Run2"]

    categories = ['VH_HPHP','VV_HPHP','VH_LPHP','VH_HPLP','VV_HPLP']
    tags = ['H_tag_HP','H_tag_LP','V_tag_HP','V_tag_LP']
    directory = "migrationunc/Run2/"

    #files = ["BulkGravToWW_Run2.root"]
    #files = ["ZprimeToZh_2016.root",'ZprimeToWW_2016.root',"WprimeToWh_2016.root","BulkGravToWW_2016.root","BulkGravToZZ_2016.root","WprimeToWZ_2016.root"]
    files = ['WJetsToQQ_Run2.root','ZJetsToQQ_Run2.root']
    #files = ["BulkGravToWW_2016.root"]
    final={}

    for root_file in files:
        for tag in tags:
            
            File = ROOT.TFile(directory+root_file,"READ")
            print 'for signal '+str(root_file.replace('.root',''))
            result = {}
            trees = []
            if root_file.find("Jets")==-1:
               for i in masses:
                   trees.append(root_file.split("_")[0]+"_narrow_"+str(i))
            else:
                trees.append(root_file.split("_")[0])
            print " trees ",trees
            for t in trees:
                try:
                    fulltree = File.Get(t)
                    print fulltree.GetEntries() 
                except :
                    print t," not found" 
                    continue
                print " using tree ",t 
                if root_file.find("Jets")==-1: splitstr = t.split('narrow_')[1]
                else:  splitstr = root_file.split("_")[0]
                for cat in categories:
                    if tag.find('HP')!=-1:
                        if tag.find('V')!=--1:
                            result[splitstr+'.'+cat] = calculateMigration(fulltree,tag,W_tag_unc_HP,cat)
                        if tag.find('H')!=-1:
                            result[splitstr+'.'+cat] = calculateMigration(fulltree,tag,H_tag_unc_HP,cat)
                    if tag.find('LP')!=-1:
                        if tag.find('V')!=-1:
                            result[splitstr+'.'+cat] = calculateMigration(fulltree,tag,W_tag_unc_LP,cat)
                        if tag.find('H')!=-1:
                            result[splitstr+'.'+cat] = calculateMigration(fulltree,tag,H_tag_unc_LP,cat)
            
        
            print '###################'+tag+'######################'
            if root_file.find("Jets")==-1: printresult(result,categories)
            else: printresultbkg(result,categories)
            final[tag]=result

        print 'CMS_VV_JJ_DeepJet_Htag_eff' 
        data[root_file.replace('.root','')+'_'+'CMS_VV_JJ_DeepJet_Htag_eff'] = calcfinalUnc(final,'H_tag',categories)
        print 'CMS_VV_JJ_DeepJet_Vtag_eff' 
        data[root_file.replace('.root','')+'_'+'CMS_VV_JJ_DeepJet_Vtag_eff'] = calcfinalUnc(final,'V_tag',categories)

        with open('migrationunc_'+root_file.split(".")[0]+'.json', 'w') as outfile:
            json.dump(data, outfile)
    
    
    
    
    
