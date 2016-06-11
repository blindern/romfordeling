#!/bin/bash
python gendot.py $1 $2 >file.dot && dot -n -Tpng file.dot >file.png
