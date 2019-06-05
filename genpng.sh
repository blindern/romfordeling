#!/bin/bash
set -eu

dir=$1
python gendot.py $dir/utlyst.txt $dir/bytter.txt >file.dot && dot -n -Tpng file.dot >$dir/generated.png
