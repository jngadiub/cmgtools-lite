#!bin/bash

basedir=results_2016_tt/
categories=("VV_HPHP") # "VV_HPLP" "VH_HPHP" "VH_LPHP" "VH_HPLP") # "VH_LPLP")
categories=("VV_HPHP" "VV_HPLP" "VH_HPHP" "VH_LPHP" "VH_HPLP") # "VH_LPLP")

#dir20=${basedir}pseudo20/
#echo $dir20
#mkdir $dir20
dir40=${basedir}pseudo40/
mkdir $dir40
#dir10=${basedir}pseudo10/
#mkdir $dir10

for cat in ${categories[*]}; do
    echo $cat
    #echo $dir20
    #python rebinPseudodata.py -c $cat -i ${basedir}pseudo80/ -o $dir20 -b 4
    echo $dir40
    python rebinPseudodataAndTemplates.py -c $cat -i ${basedir}pseudo80/ -o $dir40 -b 2
#    echo $dir10
#    python rebinPseudodata.py -c $cat -i ${basedir}pseudo80/ -o $dir10 -b 8


done


