#!/bin/bash
COUNTER=10
while [ $COUNTER -lt 23 ]; do 
DATA=$COUNTER
grep -E -c "\[\S*2014:$DATA.*200" datamining.log | awk '{print $0,"\n"}' >> 1.txt
let COUNTER=COUNTER+1
done 