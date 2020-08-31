#bin/bash!

## make pseudodata for ttbar only
# category=( "VH_HPLP" "VH_LPHP" "VH_HPHP" "VV_HPLP" "VV_HPHP")
# for c in ${category[@]}
#   do
#    python /work/dschaefer/DiBoson3D/makePseudoData.py --output newmodel4GeV/pseudo40/JJ_PD_${c}.root -k ttbarmodeling/save_new_shapes_2016_pythia_${c}_3D.root --norm ttbarmodeling/JJ_2016_nonRes_${c}.root --data ttbarmodeling/pseudo40/JJ_PD_${c}.root --which ttbar --workspace workspace_JJ_ZprimeZH_${c}_13TeV_2016ttbar.root --purity ${c}
#  done

#make the ws for ttbar only -> for the purpose of doing a ttbar only fit to get the true yields for the different ttbar contributions for the final fit 
# the workspaces need to be made with ttbar pseudodata from the ttbar-MC sample
python makeCard.py --signal ZprimeZH --outlabel ttbar -c VH_LPHP,VH_HPHP,VH_HPLP,VV_HPHP,VV_HPLP -p 2016 --pseudodata ttbar
 
category=( "VH_HPLP" "VH_LPHP" "VH_HPHP" "VV_HPLP" "VV_HPHP")
for c in ${category[@]}
  do

  python runFitPlots_vjets_signal_bigcombo_splitRes.py -n workspace_JJ_ZprimeZH_${c}_13TeV_2016ttbar.root  -i  newmodel4GeV/JJ_2016_nonRes_${c}.root -M 2000  -o postfitnewmodel4GeV/ --channel ${c} -l pseudoTTbar_postfit_${c} --doVjets --addTop --doFit
  done
  
## the fit produces output files named workspacename.json -> these are then included in the makeCard script to extract the yields if NOT pseudodata=ttbar
