#!bin/bash
script=makeInputs.py
signals=("ZprimeZH" "WprimeWH" "ZprimeWW" "BGWW" "BGZZ"  "WprimeWZ")
commands=("sigmj" "sigmvv" "signorm")
inputdir="2016/"

for signal in ${signals[*]}; do
    echo $signal
    for cmd in ${commands[*]}; do
	echo $cmd
	python ${script} -p 2016 --run ${cmd} --signal ${signal} --batch False  
    done
done


signals=("ZprimeToZh" "ZprimeToWW" "WprimeToWh" "BulkGravToWW" "BulkGravToZZ")
script=categorisation.py
for signal in ${signals[*]}; do                                                                                                                                                                                                              
    echo $signal                                                                                                                                                                                                                             
    python ${script} -y 2016  -s ${signal} -d ${inputdir}
done

