declare -a arr=("element1" "element2" "element3")

for i in "${arr[@]}"
do
   echo "$i"
   # or do whatever with individual element of the array
done
