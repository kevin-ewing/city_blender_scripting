from re import S
import bpy
import time
from random import *
from math import *
from dataclasses import dataclass
from array import *
import sys
from colorsys import hsv_to_rgb

RENDER = True

#City VARS
SIZE_OF_CITY = 120
CENTER_FACTOR = 5
CENTER_SIZE = 9
MAX_BRIGHT = 13
RIVER_CURVE_FACTOR = .25
RIVER_SIZE = 5

#Render VARS
RENDER_SIZE_FACTOR = 1
RENDER_SAMPLE_FACTOR = .25


@dataclass
class Building:
    exists: bool
    x: float
    y: float
    height: float
    tier_threshold: float


#Blender will update the view with each primitive addition, we do not want that, instead lets block it from updating the view until the end
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
    city_plan = []

    print("Clearing all buildings...")
    checkpoint = time.time()

    #Clearing all objects and materials from the prior scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.context.scene.render.engine = 'CYCLES'
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()

    #Randomly generates the "city center"
    print("Randomizing center of city and sun...")
    center_coord = SIZE_OF_CITY//CENTER_FACTOR
    center_x=randint(-center_coord, center_coord)
    center_y=randint(-center_coord, center_coord)

    sun_distance=2*SIZE_OF_CITY
    sun_x=uniform(-sun_distance,sun_distance)
    sun_decider = randint(0,1)
    if sun_decider:
        sun_y=sqrt(pow(sun_distance,2)-pow(sun_x,2))
    else:
        sun_y=-sqrt(pow(sun_distance,2)-pow(sun_x,2))
    sun_z=uniform(1,50)

    #Adds Sun
    sun_angle_z = pi - atan(sun_x / sun_y)
    if sun_decider:
        sun_angle_x = atan(sun_distance / (sun_z))
    else:
        sun_angle_x = -atan(sun_distance / (sun_z))
    sun_strength = uniform(1,MAX_BRIGHT)
    bpy.ops.object.light_add(type='SUN', radius=1, location=(sun_x, sun_y, sun_z), rotation=(sun_angle_x, 0, sun_angle_z), scale=(1, 1, 1))
    bpy.context.object.data.energy = sun_strength
    
    sun_mat = bpy.data.materials.new(name="sun_mat")
    sun_mat.use_nodes = True
    for n in sun_mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Emission Strength"].default_value = 10
            n.inputs["Emission"].default_value = (1, 1, 1, 1)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=5, enter_editmode=False, align='WORLD', location=(sun_x, sun_y, sun_z), scale=(1, 1, 1))
    bpy.context.object.data.materials.append(sun_mat)
    bpy.context.object.visible_shadow = False

    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()
    print("Randomizing camera...")
    #Randomly places the Camera in the first quadrant of the scene
    camera_distance=uniform(.8*SIZE_OF_CITY,1*SIZE_OF_CITY)
    camera_x=uniform(0,camera_distance)
    camera_y=sqrt(pow(camera_distance,2)-pow(camera_x,2))
    camera_z=uniform(5,20)

    #Adds Camera
    camera_angle_z = pi - atan(camera_x / camera_y)
    camera_angle_x = atan(camera_distance / (camera_z - 5))
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(camera_x, camera_y, camera_z), rotation=(camera_angle_x, 0, camera_angle_z), scale=(1, 1, 1))
    bpy.context.scene.camera = bpy.context.object

    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()
    print("Creating floor...")
    #Adds floor facing the camera
    mat = bpy.data.materials.new(name="floor")
    mat.use_nodes = True
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Metallic"].default_value = 0.65
            n.inputs["Roughness"].default_value = 0.15
    
    bpy.ops.mesh.primitive_cube_add(location = (0, 0, -1), rotation=(0, 0, camera_angle_z), scale = (3*SIZE_OF_CITY, 3*SIZE_OF_CITY, 1))
    bpy.context.object.data.materials.append(mat)
    

    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()
    print("Creating color palette...")
    
    world_fixed_color = uniform(0.4,0.85)
    world_saturation = uniform(0.1, 0.5)
    world_value = uniform(0.2, 1)

    #Sets world color 
    world_strength = uniform(0, sun_strength/MAX_BRIGHT)
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (hsv_to_rgb(world_fixed_color, world_saturation, world_value)[0], hsv_to_rgb(world_fixed_color, world_saturation, world_value)[1],hsv_to_rgb(world_fixed_color, world_saturation, world_value)[2], world_strength)
    
    #Generate a new random color in line with the palette and then create a building
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()
    print("Generating building plans...")
    for i in range (-SIZE_OF_CITY//2,SIZE_OF_CITY//2):
        temp = []
        for j in range (-SIZE_OF_CITY//2,SIZE_OF_CITY//2):
            temp.append(plan_building(i, j, center_x, center_y))
        city_plan.append(temp)

    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()
    print("Building all buildings...")
    carve_river(city_plan)


    fixed_color = uniform(0.4,0.85)
    saturation = uniform(0.1, 0.5)
    value = uniform(0.2, 1)

    build_all_buildings(city_plan, fixed_color, saturation, value)
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()

    setup_composite()


def carve_park(city_plan):
    """
    Carves out a park in the city
    """
    center = randint(-SIZE_OF_CITY//2, SIZE_OF_CITY)
    height = randint(0, 12)
    width = randint(0, 12)
    for i in range (center + (-height//2), center + (height//2)):
        for j in range (center + (-width//2), center + (width//2)):
            try:
                city_plan[i][j].exists = False
            except IndexError:
                pass

def carve_river(city_plan):
    """
    Carves out a river through the city
    """
    edge = False
    direction = 0
    for cols in city_plan:
        rand_start = randint(0, len(cols))
    
    current_x = rand_start
    current_y = 0

    
    while edge == False:
        dir_change = uniform(0,1)
        if dir_change < RIVER_CURVE_FACTOR:
            direction = (direction - 1) % 4
        elif dir_change < RIVER_CURVE_FACTOR * 2:
            direction = (direction + 1) % 4
        try: 
            if direction == 0:
                current_y += 1
            elif direction == 1:
                current_x += 1
            elif direction == 2:
                current_y -= 1
            else:
                current_x -= 1

            
            #clear around
            try:
                for i in range(-RIVER_SIZE//2, RIVER_SIZE//2):
                    for j in range(-RIVER_SIZE//2, RIVER_SIZE//2):
                        city_plan[current_x + i][current_y + j].exists = False
            except IndexError:
                pass

            #If actual plan is at edge then we do exit loop
            city_plan[current_x][current_y].exists = False

        except IndexError:
            edge = True


    


def setup_composite():
    #https://blender.stackexchange.com/questions/19500/controling-compositor-by-python
    # switch on nodes and get reference
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    # clear default nodes
    for node in tree.nodes:
        tree.nodes.remove(node)

    # create input image node
    image_node = tree.nodes.new(type='CompositorNodeRLayers')

    # create glare node
    glare_node = tree.nodes.new('CompositorNodeGlare')
    glare_node.glare_type = "FOG_GLOW"
    glare_node.size = 5

    # create output node
    comp_node = tree.nodes.new('CompositorNodeComposite')

    # link nodes
    links = tree.links
    links.new(image_node.outputs[0], glare_node.inputs[0])
    links.new(glare_node.outputs[0], comp_node.inputs[0])




def plan_building(x, y, center_x, center_y):
    height = determine_building_height(x, y, center_x, center_y, SIZE_OF_CITY)
    tier_threshold = randint(0, 20)*height

    return Building(True, x, y, height, tier_threshold)

def build_mat(fixed_color, saturation, value, shiny):

    color_addition = uniform(-0.25, 0.25)
    varied_color = fixed_color + color_addition
    if varied_color > 1:
        varied_color - 1
    if varied_color < 0:
        varied_color + 1

    sat_addition = uniform(-0.1, 0.1)
    varied_saturation = saturation + sat_addition
    if varied_saturation > 1:
        varied_saturation - 1
    if varied_saturation < 0:
        varied_saturation + 1
    
    value_addition = uniform(-0.1, 0.1)
    varied_value = value + value_addition
    if varied_value > 1:
        varied_value - 1
    if varied_value < 0:
        varied_value + 1

    if shiny:
        built_mat = bpy.data.materials.new(name=str(varied_color+varied_saturation+varied_value))
        built_mat.use_nodes = True
        for n in built_mat.node_tree.nodes:
            if n.type == 'BSDF_PRINCIPLED':
                n.inputs["Metallic"].default_value = 0.5
                n.inputs["Roughness"].default_value = 0.05
                n.inputs["Base Color"].default_value = (hsv_to_rgb(varied_color, varied_saturation, varied_value)[0], hsv_to_rgb(varied_color, varied_saturation, varied_value)[1],hsv_to_rgb(varied_color, varied_saturation, varied_value)[2], 1.0)
    else:
        built_mat = bpy.data.materials.new(name="mat")
        built_mat.diffuse_color = (hsv_to_rgb(varied_color, varied_saturation, varied_value)[0], hsv_to_rgb(varied_color, varied_saturation, varied_value)[1],hsv_to_rgb(varied_color, varied_saturation, varied_value)[2], 1.0)

    return built_mat

def build_all_buildings(city_plan, fixed_color, saturation, value):
    th_max = 0
    for cols in city_plan:
        for row in cols:
            if row.tier_threshold > th_max:
                th_max = row.tier_threshold

    for cols in city_plan:
        for row in cols:
            if row.exists == False:
                pass
            elif row.tier_threshold > (11 * (th_max/15)):
                pointed_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            elif row.tier_threshold > (9 * (th_max/15)):
                tiered_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            elif row.tier_threshold > (8 * (th_max/15)):
                striped_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            elif row.tier_threshold > (7 * (th_max/15)):
                spired_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            elif row.tier_threshold > (6 * (th_max/15)):
                crossed_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            elif row.tier_threshold > (5 * (th_max/15)):
                glass_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 1))
            elif row.tier_threshold > (4 * (th_max/15)):
                l_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            elif row.tier_threshold > (2 * (th_max/15)):
                pass
            elif row.tier_threshold < (.8 * (th_max/15)):
                small_building(row.x, row.y, row.height, build_mat(fixed_color, saturation, value, 0))
            else:
                bpy.ops.mesh.primitive_cube_add(location = (row.x, row.y, row.height), scale = (.40, .40, row.height))
                bpy.context.object.data.materials.append(build_mat(fixed_color, saturation, value, 0))

def determine_building_height(x, y, center_x, center_y, SIZE_OF_CITY):
    distance = sqrt((x - center_x)**2 + (y - center_y)**2)
    minimum = (distance ** 0.25) / (SIZE_OF_CITY/10)
    maximum = 9 - (8 / (1 + pow(1.3, (-1.4 * (distance - CENTER_SIZE)))))
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

def glass_building(x, y, height, mat):
    bpy.ops.mesh.primitive_cube_add(location = (x, y, height), scale = (.40, .40, height)) 
    bpy.context.object.data.materials.append(mat)

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
    start_checkpoint = time.time()
    run_ops_without_view_layer_update(main)
    if RENDER:
        print("Rendering...")
        checkpoint = time.time()
        bpy.context.scene.render.filepath = "/Users/kewing/Desktop/sp22/anim/blender/city/output/o" + sys.argv[7]
        bpy.context.scene.cycles.samples = 1024 * RENDER_SAMPLE_FACTOR
        bpy.context.scene.render.resolution_x = 3840 * RENDER_SIZE_FACTOR
        bpy.context.scene.render.resolution_y = 1644 * RENDER_SIZE_FACTOR
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
        print("--- %s seconds ---\n" % (time.time() - checkpoint))
        print("Total Time: --- %s seconds ---\n"% (time.time() - start_checkpoint))

