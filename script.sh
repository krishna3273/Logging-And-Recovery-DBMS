#!/bin/bash

argc="$#" 

if [ $argc -eq 1 ]
then
    python3 20171196_2.py "$1"
else
    python3 20171196_1.py "$1" "$2"
fi
