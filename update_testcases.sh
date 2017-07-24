#!/bin/sh -xf

pat=$(dirname $(head -n 1 "test/split.1.source_tree.txt"))
repl="$(pwd)/test"
echo $pat
echo $repl
for f in $(find "test" -name "*.txt" -type f); do
    sed -i.bac "s:${pat}:${repl}:g" $f
done
