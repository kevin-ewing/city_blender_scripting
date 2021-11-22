import bpy
from random import *
from math import *

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
bpy.context.scene.render.engine = 'CYCLES'
for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)

MINIMUM_BUILDING_SIZE = .2
MAXIMUM_BUILDING_SIZE = 10

def building(x, y, center_x, center_y, size_of_city,  c1, c2, c3):
    height = determine_building_height(x, y, center_x, center_y, size_of_city)
    mat = bpy.data.materials.new(name=str(c1+c2+c3))
    mat.diffuse_color = (c1, c2, c3, 1.0)
    
    tier_threshold = randint(0, 100)*height
    if tier_threshold > 340:
        bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.45, .45, height))
        bpy.context.object.data.materials.append(mat)
        size_of_point = uniform(0.05, 0.12)
        length_of_point = uniform(10, 20)*size_of_point
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
        bpy.ops.transform.resize(value=(size_of_point, size_of_point, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.translate(value=(0, 0, length_of_point), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    elif tier_threshold > 280:
        bpy.ops.mesh.primitive_cube_add(location = (x, y, height/4), scale = (.45, .45, height/4))
        bpy.context.object.data.materials.append(mat)
        bpy.ops.mesh.primitive_cube_add(location = (x, y, 3 * (height/4)), scale = (.35, .35, height/4))
        bpy.context.object.data.materials.append(mat)
        bpy.ops.mesh.primitive_cube_add(location = (x, y, 5 * (height/4)), scale = (.3, .3, height/4))
        bpy.context.object.data.materials.append(mat)
        bpy.ops.mesh.primitive_cube_add(location = (x, y, 7 * (height/4)), scale = (.25, .25, height/4))
        bpy.context.object.data.materials.append(mat)
    else:
        bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.40, .40, height))    
        bpy.context.object.data.materials.append(mat)

    
def determine_building_height(x, y, center_x, center_y, size_of_city):
    distance = size_of_city - sqrt((x - center_x)**2 + (y - center_y)**2)
    minimum = (distance ** .3) / 3
    maximum = (distance** 1.2)/5
    return uniform(minimum, maximum)
    

def main():
    size_of_city = 16
    center_x=randint(-size_of_city//5,size_of_city//5)
    center_y=randint(-size_of_city//5,size_of_city//5)
    
    sun_x=uniform(-size_of_city,size_of_city)
    sun_y=uniform(-size_of_city,size_of_city)
    
    camera_x=uniform(1.2*size_of_city,2*size_of_city)
    camera_y=uniform(1.2*size_of_city,2*size_of_city)
    camera_z=uniform(size_of_city/2,size_of_city)
    
    bpy.ops.object.light_add(type='POINT', radius=10, location=(sun_x, sun_y, 20), scale=(1, 1, 1))
    bpy.context.object.data.energy = 10000
    
    
    
#    bpy.data.World.color (0.325353, 0.532963, 0.199391)


    #Adds Camera
    camera_angle_z = pi - atan(camera_x / camera_y)
    camera_angle_x = pi/10 + atan(camera_x / camera_z)
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camera_x, camera_y, camera_z), rotation=(camera_angle_x, 0, camera_angle_z), scale=(1, 1, 1))
    bpy.context.scene.camera = bpy.context.object

    #Adds floor
    bpy.ops.mesh.primitive_plane_add(size=2*size_of_city, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(0, 0, camera_angle_z), scale=(2, 1, 1))
    
    
    decider = randint(0,2)
    fixed_color_1 = uniform(0,1)
    fixed_color_2 = uniform(0,1)
    
    if decider == 0:
        c1 = fixed_color_1
        c2 = uniform(0,1)
        c3 = fixed_color_2
    elif decider == 1:
        c1 = uniform(0,1)
        c2 = fixed_color_1
        c3 = fixed_color_2
    else:
        c1 = fixed_color_1
        c2 = fixed_color_2
        c3 = uniform(0,1)
        
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (c1, c2, c3, 1)

           
    for i in range (-size_of_city//2,size_of_city//2):
        for j in range (-size_of_city//2,size_of_city//2):
            if decider == 1:
                c1 = fixed_color_1
                c2 = fixed_color_2
                c3 = uniform(0,1)
            elif  decider == 2:
                c1 = fixed_color_1
                c2 = uniform(0,1)
                c3 = fixed_color_2
            else:
                c1 = uniform(0,1)
                c2 = fixed_color_1
                c3 = fixed_color_2
            
            building(i, j, center_x, center_y, size_of_city, c1, c2, c3)


           
if __name__ == "__main__":  
    main()
    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
    