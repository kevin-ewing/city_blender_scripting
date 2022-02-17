import bpy
from random import *
from math import *
import sys

SIZE_OF_CITY = 45
CENTER_FACTOR = 5

#Blender will update the view with each primative addition, we do not want that, instead lets block it from updating the view until the end
#https://blender.stackexchange.com/questions/7358/python-performance-with-blender-operators
def run_ops_without_view_layer_update(func):
    from bpy.ops import _BPyOpsSubModOp
    view_layer_update = _BPyOpsSubModOp._view_layer_update
    def dummy_view_layer_update(context):
        pass
    try:
        _BPyOpsSubModOp._view_layer_update = dummy_view_layer_update
        func()
    finally:
        _BPyOpsSubModOp._view_layer_update = view_layer_update
        

def main():
    '''
    Main function
        clears scene, sets conditions, calls grid of building()
    '''

    #Clearing all objects and materials from the prior scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.context.scene.render.engine = 'CYCLES'
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    #Randomly generates the "city center"
    center_coord = SIZE_OF_CITY//CENTER_FACTOR
    center_x=randint(-center_coord, center_coord)
    center_y=randint(-center_coord, center_coord)
    
    #Randomly creates the Sun somwhere in the scene
    sun_x=uniform(-SIZE_OF_CITY,SIZE_OF_CITY)
    sun_y=uniform(-SIZE_OF_CITY,SIZE_OF_CITY)
    bpy.ops.object.light_add(type='POINT', radius=10, location=(sun_x, sun_y, 20), scale=(1, 1, 1))
    bpy.context.object.data.energy = 10000
    
    #Randomly places the Camera in the first quadrant of the scene
    camera_x=uniform(1.1*SIZE_OF_CITY,2*SIZE_OF_CITY)
    camera_y=uniform(1.1*SIZE_OF_CITY,2*SIZE_OF_CITY)
    camera_z=uniform(SIZE_OF_CITY/2,SIZE_OF_CITY)

    #Adds Camera
    camera_angle_z = pi - atan(camera_x / camera_y)
    camera_angle_x = pi/10 + atan(camera_x / camera_z)
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camera_x, camera_y, camera_z), rotation=(camera_angle_x, 0, camera_angle_z), scale=(1, 1, 1))
    bpy.context.scene.camera = bpy.context.object

    #Adds floor facing the camera
    mat = bpy.data.materials.new(name="floor")
    mat.use_nodes = True
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Metallic"].default_value = 0.65
            n.inputs["Roughness"].default_value = 0.15
#    bpy.ops.mesh.primitive_plane_add(size=2*SIZE_OF_CITY, enter_editmode=False, align='WORLD', location=(0, 0, 0), , scale=(2, 1, 1))
    
    
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, -1), rotation=(0, 0, camera_angle_z), scale = (2*SIZE_OF_CITY, SIZE_OF_CITY, 1))
    bpy.context.object.data.materials.append(mat)
    
    #Determining which way the palette will be "stuck"
    decider = randint(0,2)
    fixed_color_1 = uniform(0,1)
    fixed_color_2 = uniform(0,1)
    
    if decider == 1:
        c1 = 1-fixed_color_1
        c2 = 1-fixed_color_2
        c3 = uniform(0,1)
    elif decider == 2:
        c1 = 1-fixed_color_1
        c2 = uniform(0,1)
        c3 = 1-fixed_color_2
    else:
        c1 = uniform(0,1)
        c2 = 1-fixed_color_1
        c3 = 1-fixed_color_2

    #Sets world color 
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (c1, c2, c3, 1)
    
    #Generate a new random color in line with the palette and then create a building
    for i in range (-SIZE_OF_CITY//2,SIZE_OF_CITY//2):
        for j in range (-SIZE_OF_CITY//2,SIZE_OF_CITY//2):
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
            
            building(i, j, center_x, center_y, c1, c2, c3)

def building(x, y, center_x, center_y,  c1, c2, c3):
    height = determine_building_height(x, y, center_x, center_y, SIZE_OF_CITY)

    mat = bpy.data.materials.new(name="test_mat")
    mat.diffuse_color = (c1, c2, c3, 1.0)
        
    tier_threshold = randint(0, 100)*height
    if tier_threshold > 345:
        pointed_building(x, y, height, mat)
    elif tier_threshold > 265:
        tiered_building(x, y, height, mat)
    elif tier_threshold > 240:
        striped_building(x, y, height, mat)
    elif tier_threshold > 230:
        spired_building(x, y, height, mat)
    elif tier_threshold > 180:
        crossed_building(x, y, height, mat)
    elif tier_threshold > 120:
        glass_building(x, y, height, c1, c2, c3)
    elif tier_threshold > 100:
        l_building(x, y, height, mat)
    elif tier_threshold > 90:
        pass
    elif  tier_threshold < 10:
        small_building(x, y, height, mat)
    else:
        bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.40, .40, height))
        bpy.context.object.data.materials.append(mat)

def determine_building_height(x, y, center_x, center_y, SIZE_OF_CITY):
    distance = SIZE_OF_CITY - sqrt((x - center_x)**2 + (y - center_y)**2)
    minimum = (distance ** .3) / 3
    maximum = (distance** 1.2)/10
    return uniform(minimum, maximum)
     
def pointed_building(x, y, height, mat):
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.45, .45, height))
    bpy.context.object.data.materials.append(mat)
    size_of_point = uniform(0.05, 0.12)
    length_of_point = uniform(10, 20)*size_of_point
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
    bpy.ops.transform.resize(value=(size_of_point, size_of_point, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.translate(value=(0, 0, length_of_point), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

def tiered_building(x, y, height, mat):
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height/4), scale = (.45, .45, height/4))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, 3 * (height/4)), scale = (.4, .4, height/4))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, 5 * (height/4)), scale = (.35, .35, height/4))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, 7 * (height/4)), scale = (.3, .3, height/4))
    bpy.context.object.data.materials.append(mat)

def striped_building(x, y, height, mat):
    step_height_factor = uniform(1.05, 1.2)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.35, .35, height))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x+.25, y+.25, height/step_height_factor), scale = (.13, .13, height/step_height_factor))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x-.25, y+.25, height/step_height_factor), scale = (.13, .13, height/step_height_factor))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x+.25, y-.25, height/step_height_factor), scale = (.13, .13, height/step_height_factor))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x-.25, y-.25, height/step_height_factor), scale = (.13, .13, height/step_height_factor))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height+2*(step_height_factor-1)), scale = (.3, .3, height))
    bpy.context.object.data.materials.append(mat)
    
def spired_building(x, y, height, mat):
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.40, .40, height))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cone_add(location = (x, y, 2*height+.14), scale = (.34, .34, .7))
    bpy.ops.object.shade_smooth()
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, 2*height+.14), scale = (.38, .38, .08))
    bpy.context.object.data.materials.append(mat)

def crossed_building(x, y, height, mat):
    max_beam_count = 10

    number_beams = randint(3, max_beam_count)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.35, .35, height+.04))
    bpy.context.object.data.materials.append(mat)
    beam_offset = 2*(.35/number_beams)
    for i in range (number_beams+1):
        bpy.ops.mesh.primitive_cube_add(location = (x, y-.35+(beam_offset*i), height), scale = (.4, .4/(3*number_beams), height))
        bpy.context.object.data.materials.append(mat)
        bpy.ops.mesh.primitive_cube_add(location = (x-.35+(beam_offset*i), y, height), scale = (.4/(3*number_beams), .4, height))
        bpy.context.object.data.materials.append(mat)

def glass_building(x, y, height, c1, c2, c3):
    reflective_mat = bpy.data.materials.new(name=str(c1+c2+c3))
    reflective_mat.use_nodes = True
    for n in reflective_mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Metallic"].default_value = 0.4
            n.inputs["Roughness"].default_value = 0.1
            n.inputs["Base Color"].default_value = (c1, c2, c3, 1.0)
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.40, .40, height)) 
    bpy.context.object.data.materials.append(reflective_mat)

def l_building(x, y, height, mat):
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.39, .39, height))
    bpy.context.object.data.materials.append(mat)
    floors = int (height // .2)
    for i in range (floors + 1):
        bpy.ops.mesh.primitive_cube_add(location = (x, y, i*.4), scale = (.4, .4, .02))
        bpy.context.object.data.materials.append(mat)   

def small_building(x, y, height, mat):
    x_orient = choice([-1, 1])
    y_orient = choice([-1, 1])
    scaler = uniform(.9, 1.1)
    bpy.ops.mesh.primitive_cube_add(location = (x + (.2 * x_orient), y, height*scaler), scale = (.2, .4, height*scaler))
    bpy.context.object.data.materials.append(mat)
    bpy.ops.mesh.primitive_cube_add(location = (x, y + (.2 * y_orient), height), scale = (.4, .2, height))
    bpy.context.object.data.materials.append(mat)
        
           
if __name__ == "__main__":  
    run_ops_without_view_layer_update(main)
    bpy.context.scene.render.filepath = "/Users/kewing/Desktop/sp22/anim/blender/city/sample_out/o" + sys.argv[4]
    bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)