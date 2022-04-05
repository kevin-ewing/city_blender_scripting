
if [ $# == 2 ]
then
    count=${1}
    range=`expr ${2} - ${1} + 1`
    for i in $(seq $range); do
        blender --background --python gen_city.py -t 64 --python-exit-code ${count}
        count=`expr ${count} + 1`
    done
elif [ $# == 1 ]
then
    count=${1}
    blender --background --python gen_city.py -t 64 --python-exit-code ${count}
else
    echo "Check the README.md for doccumentation"
fi