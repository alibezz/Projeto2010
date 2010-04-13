#!/bin/bash

LIST=$1
DIR=$2

mkdir articles
while read line; do
  cp $DIR$line articles
done < $LIST 
