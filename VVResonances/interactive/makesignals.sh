#!bin/bash
script=makeInputs.py
signals=("ZprimeZH" "WprimeWH" "ZprimeWW" "BGWW" "BGZZ"  "WprimeWZ")
commands=("sigmj" "sigmvv" "signorm")
inputdir="2016trainingV2/"
''' 
for signal in ${signals[*]}; do
    echo $signal
    for cmd in ${commands[*]}; do
	echo $cmd
	python ${script} -p 2016 --run ${cmd} --signal ${signal} --batch False  
    done
done


python ${script} -p 2016 --run "sigmj" --signal "WprimeWH" --batch False  
python ${script} -p 2016 --run "sigmj" --signal "ZprimeWW" --batch False  
python ${script} -p 2016 --run "sigmj" --signal "BGWW" --batch False  
python ${script} -p 2016 --run "sigmj" --signal "BGZZ" --batch False  
python ${script} -p 2016 --run "sigmj" --signal "WprimeWZ" --batch False  


python ${script} -p 2016 --run "sigmvv" --signal "BGWW" --batch False  
python ${script} -p 2016 --run "sigmvv" --signal "ZprimeZH" --batch False
python ${script} -p 2016 --run "sigmvv" --signal "WprimeWH" --batch False
python ${script} -p 2016 --run "sigmvv" --signal "ZprimeWW" --batch False  
python ${script} -p 2016 --run "sigmvv" --signal "BGZZ" --batch False  
python ${script} -p 2016 --run "sigmvv" --signal "WprimeWZ" --batch False  

python ${script} -p 2016 --run "signorm" --signal "ZprimeWW" --batch False
python ${script} -p 2016 --run "signorm" --signal "ZprimeZH" --batch False  
python ${script} -p 2016 --run "signorm" --signal "WprimeWH" --batch False  
python ${script} -p 2016 --run "signorm" --signal "BGWW" --batch False  
python ${script} -p 2016 --run "signorm" --signal "BGZZ" --batch False  
python ${script} -p 2016 --run "signorm" --signal "WprimeWZ" --batch False  
'''

signals=("ZprimeToZh" "ZprimeToWW" "WprimeToWh" "BulkGravToWW" "BulkGravToZZ")

for signal in ${signals[*]}; do                                                                                                                                                                                                              
    echo $signal                                                                                                                                                                                                                             
    python categorisation.py -y 2016  -s ${signal} -d ${inputdir}
done
