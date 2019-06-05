#!/bin/bash
set -eu

dir=$1
python gangvis/gendot.py $dir/bytter.txt >file.dot && dot -n -Tpng file.dot >$dir/generated-gangvis.png
