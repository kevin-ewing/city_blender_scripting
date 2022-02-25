range=`expr ${2} - ${1} + 1`
count=${1}


for i in $(seq $range); do
    blender --background --python gen_city.py -t 64 --python-exit-code ${count} 2> render_log.txt
    count=`expr ${count} + 1`
done