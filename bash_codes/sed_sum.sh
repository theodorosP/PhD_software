#! /bin/bash
i=1
sed -i "s/a = -3/a = $((1 - $i))/g" file
