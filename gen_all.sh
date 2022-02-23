range=`expr ${2} - ${1} + 1`
count=${1}


for i in $(seq $range); do
    blender --background --python gen_city.py ${count}
    count=`expr ${count} + 1`
done