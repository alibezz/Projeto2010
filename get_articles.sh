#!/bin/bash

#ALINE BESSA - 12/04/2010
#This script gets articles from documents in bitterlemons corpus
#The script generates different articles from a single document

DIR=$1
PARSED=parsed_$(basename $DIR)
SCRIPT=$2

test -e $PARSED || mkdir $PARSED
for FILE in $DIR/*; do
  awk '/TITLE/,/<i>Published/ { print }' $FILE > tmp
  awk '/AUTHOR-->/,/<i>Published/ { print }' tmp > parsed_$(basename $FILE)
  ./$SCRIPT parsed_$(basename $FILE)
done
mv *.html $PARSED
