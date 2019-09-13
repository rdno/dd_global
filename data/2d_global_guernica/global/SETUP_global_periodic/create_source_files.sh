#!/bin/sh


nsrc=`wc -l sources.dat | cut -d ' ' -f 1`
for i in `seq 1 $nsrc`;
do
    xs=$(awk -v "line=$i" 'NR==line { print $1 }' sources.dat)
    zs=$(awk -v "line=$i" 'NR==line { print $2 }' sources.dat)
    name=$(awk -v "line=$i" 'NR==line { print $1 }' events_21)
    cp SOURCE{,_${name}}
    sed -i "s/\(^xs.*=[ ]*\)[-\.0-9]*/\1$xs/g" SOURCE_${name}
    sed -i "s/\(^zs.*=[ ]*\)[-\.0-9]*/\1$zs/g" SOURCE_${name}
done
