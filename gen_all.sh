count=${1}
for i in $(seq $count); do
    blender --background --python gen_city.py ${i}
done