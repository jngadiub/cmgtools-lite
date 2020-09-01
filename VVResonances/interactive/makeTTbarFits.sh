#bin/bash!

## make pseudodata for ttbar only, change the category in the makeInputs before running it
#    python makeInputs.py -p 2016 --run "pseudoTT" 

#make the ws for ttbar only -> for the purpose of doing a ttbar only fit to get the true yields for the different ttbar contributions for the final fit 
# the workspaces need to be made with ttbar pseudodata from the ttbar-MC sample

category=("VH_NPHP_control_region") # "VH_HPLP" "VH_LPHP" "VH_HPHP" "VV_HPLP" "VV_HPHP")
for c in ${category[@]}
do 
    
    python makeCard.py --signal BulkGWW --outlabel ttbar -c ${c} -p 2016 --pseudodata ttbar
done

for c in ${category[@]}
do
  python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_BulkGWW_${c}_13TeV_2016ttbar.root  -i  results_2016//JJ_2016_nonRes_${c}.root -M 2000  -o postfit/ --channel ${c} -l pseudoTTbar_postfit_${c} --doVjets --addTop --doFit
done
  
## the fit produces output files named workspacename.json -> these are then included in the makeCard script to extract the yields if NOT pseudodata=ttbar
