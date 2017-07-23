#!/bin/sh -xf

pat=$(dirname $(head -n 1 "test/dedup.1.source_tree.txt"))
pat=$(dirname $(head -n 1 "test/split.1.source_tree.txt"))
pat=$(dirname $(head -n 1 "test/map.input.2.txt"))
pat=$(dirname $(head -n 1 "test/map.input.3.txt"))
repl="$(pwd)/test"
echo $pat
echo $repl
for f in $(find "test" -name "*.txt" -type f); do
    sed -i.bac "s:${pat}:${repl}:g" $f
done
