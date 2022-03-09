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
RIVER_CURVE_FACTOR = .20
RIVER_SIZE = 4

#Render VARS
RENDER_SIZE_FACTOR = 1
RENDER_SAMPLE_FACTOR = .25

@dataclass
class Building:
    conjoined: bool
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
    


    bpy.ops.mesh.primitive_plane_add(size=400, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.modifier_add(type='NODES')
    bpy.data.node_groups["Geometry Nodes"].name = "mountain"
    
    create_mountain_tree()

    bpy.ops.object.shade_smooth()

    # selected_objects = (obj for obj in bpy.data.objects if obj.select_get())
    # for obj in selected_objects:
    #     modifier = obj.modifiers.new(name='mountain', type='NODES')
    # bpy.context.object.modifiers["GeometryNodes"].Input_2 = 4

    bpy.context.object.data.materials.append(mat)
    

    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()
    print("Creating color palette...")
    
    world_fixed_color = uniform(0.4,0.85)
    world_saturation = uniform(0.4, 0.8)
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

    print("Carving River...")
    carve_river(city_plan)
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()

    

    fixed_color = uniform(0,1)
    saturation = uniform(0.1, 1)
    value = uniform(0.2, 1)

    print("Joining Buildings...")
    join_buildings(city_plan, fixed_color, saturation, value)
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()

    print("Building all buildings...")

    build_all_buildings(city_plan, fixed_color, saturation, value)
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()

    print("Seting up composite...")
    setup_composite()
    print("--- %s seconds ---\n" % (time.time() - checkpoint))
    checkpoint = time.time()


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

def join_buildings(city_plan, fixed_color, saturation, value):
    for cols in range(len(city_plan)):
        for rows in range(len(city_plan[cols])):
            
            if uniform(0,1) < 0.08 and city_plan[cols][rows].height < 4 and city_plan[cols][rows].conjoined == False:
                if uniform(0,1) < 0.5:
                    try:
                        if city_plan[cols][rows+1].conjoined == False and city_plan[cols][rows+1].exists == True and city_plan[cols][rows].exists == True:
                            city_plan[cols][rows].exists = False
                            city_plan[cols][rows+1].exists = False
                            city_plan[cols][rows+1].conjoined = True

                            bpy.ops.mesh.primitive_cube_add(location = (city_plan[cols][rows].x, city_plan[cols][rows].y + .5, city_plan[cols][rows].height), scale = (.40, .90, city_plan[cols][rows].height))
                            bpy.context.object.data.materials.append(build_mat(fixed_color, saturation, value, 0))

                    except IndexError:
                        pass
                else:
                    try:
                        if city_plan[cols+1][rows].conjoined == False and city_plan[cols+1][rows].exists == True and city_plan[cols][rows].exists == True:
                            city_plan[cols][rows].exists = False
                            city_plan[cols+1][rows].exists = False
                            city_plan[cols+1][rows].conjoined = True

                            bpy.ops.mesh.primitive_cube_add(location = (city_plan[cols][rows].x + 0.5, city_plan[cols][rows].y, city_plan[cols][rows].height), scale = (.90, .40, city_plan[cols][rows].height))
                            bpy.context.object.data.materials.append(build_mat(fixed_color, saturation, value, 0))

                    except IndexError:
                        pass

    


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

    #Building is first actually initialized
    return Building(False, True, x, y, height, tier_threshold)

def build_mat(fixed_color, saturation, value, shiny):

    color_addition = uniform(-0.15, 0.15)
    varied_color = fixed_color + color_addition
    if varied_color > 1:
        varied_color - 1
    if varied_color < 0:
        varied_color + 1

    sat_addition = uniform(-0.1, 0.1)
    varied_saturation = saturation + sat_addition
    
    value_addition = uniform(-0.1, 0.1)
    varied_value = value + value_addition

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


def create_mountain_tree():

    # MATERIAL
    node_tree1 = bpy.data.node_groups.get('mountain')

    for node in node_tree1.nodes:
        node_tree1.nodes.remove(node)
    # INPUTS
    input = node_tree1.inputs.new('NodeSocketGeometry', 'Geometry')
    if hasattr(input, 'attribute_domain'):
        input.attribute_domain = 'POINT'
    if hasattr(input, 'hide_value'):
        input.hide_value = False
    if hasattr(input, 'name'):
        input.name = 'Geometry'
    # OUTPUTS
    output = node_tree1.outputs.new('NodeSocketGeometry', 'Geometry')
    if hasattr(output, 'attribute_domain'):
        output.attribute_domain = 'POINT'
    if hasattr(output, 'hide_value'):
        output.hide_value = False
    if hasattr(output, 'name'):
        output.name = 'Geometry'
    # NODES
    group_output_1 = node_tree1.nodes.new('NodeGroupOutput')
    if hasattr(group_output_1, 'color'):
        group_output_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(group_output_1, 'hide'):
        group_output_1.hide = False
    if hasattr(group_output_1, 'is_active_output'):
        group_output_1.is_active_output = True
    if hasattr(group_output_1, 'location'):
        group_output_1.location = (998.134765625, 181.331298828125)
    if hasattr(group_output_1, 'mute'):
        group_output_1.mute = False
    if hasattr(group_output_1, 'name'):
        group_output_1.name = 'Group Output'
    if hasattr(group_output_1, 'use_custom_color'):
        group_output_1.use_custom_color = False
    if hasattr(group_output_1, 'width'):
        group_output_1.width = 140.0

    subdivide_mesh_1 = node_tree1.nodes.new('GeometryNodeSubdivideMesh')
    if hasattr(subdivide_mesh_1, 'color'):
        subdivide_mesh_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(subdivide_mesh_1, 'hide'):
        subdivide_mesh_1.hide = False
    if hasattr(subdivide_mesh_1, 'location'):
        subdivide_mesh_1.location = (-539.3538818359375, 257.773681640625)
    if hasattr(subdivide_mesh_1, 'mute'):
        subdivide_mesh_1.mute = False
    if hasattr(subdivide_mesh_1, 'name'):
        subdivide_mesh_1.name = 'Subdivide Mesh'
    if hasattr(subdivide_mesh_1, 'use_custom_color'):
        subdivide_mesh_1.use_custom_color = False
    if hasattr(subdivide_mesh_1, 'width'):
        subdivide_mesh_1.width = 140.0
    input_ = next((input_ for input_ in subdivide_mesh_1.inputs if input_.identifier=='Level'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 1
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Level'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False

    position_1 = node_tree1.nodes.new('GeometryNodeInputPosition')
    if hasattr(position_1, 'color'):
        position_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(position_1, 'hide'):
        position_1.hide = False
    if hasattr(position_1, 'location'):
        position_1.location = (-457.5484619140625, 73.76937866210938)
    if hasattr(position_1, 'mute'):
        position_1.mute = False
    if hasattr(position_1, 'name'):
        position_1.name = 'Position'
    if hasattr(position_1, 'use_custom_color'):
        position_1.use_custom_color = False
    if hasattr(position_1, 'width'):
        position_1.width = 140.0
    output = next((output for output in position_1.outputs if output.identifier=='Position'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Position'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_002_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_002_1, 'color'):
        math_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_002_1, 'hide'):
        math_002_1.hide = False
    if hasattr(math_002_1, 'location'):
        math_002_1.location = (-1863.360595703125, -196.51612854003906)
    if hasattr(math_002_1, 'mute'):
        math_002_1.mute = False
    if hasattr(math_002_1, 'name'):
        math_002_1.name = 'Math.002'
    if hasattr(math_002_1, 'operation'):
        math_002_1.operation = 'ABSOLUTE'
    if hasattr(math_002_1, 'use_clamp'):
        math_002_1.use_clamp = False
    if hasattr(math_002_1, 'use_custom_color'):
        math_002_1.use_custom_color = False
    if hasattr(math_002_1, 'width'):
        math_002_1.width = 140.0
    input_ = next((input_ for input_ in math_002_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_002_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_002_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_002_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND_DOT'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_1, 'color'):
        math_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_1, 'hide'):
        math_1.hide = False
    if hasattr(math_1, 'location'):
        math_1.location = (-1860.6793212890625, -58.374664306640625)
    if hasattr(math_1, 'mute'):
        math_1.mute = False
    if hasattr(math_1, 'name'):
        math_1.name = 'Math'
    if hasattr(math_1, 'operation'):
        math_1.operation = 'INVERSE_SQRT'
    if hasattr(math_1, 'use_clamp'):
        math_1.use_clamp = False
    if hasattr(math_1, 'use_custom_color'):
        math_1.use_custom_color = False
    if hasattr(math_1, 'width'):
        math_1.width = 140.0
    input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND_DOT'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    colorramp_1 = node_tree1.nodes.new('ShaderNodeValToRGB')
    if hasattr(colorramp_1, 'color'):
        colorramp_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(colorramp_1, 'color_ramp'):
        if hasattr(colorramp_1.color_ramp, 'color_mode'):
            colorramp_1.color_ramp.color_mode = 'RGB'
        if hasattr(colorramp_1.color_ramp, 'elements'):
            if 0 >= len(colorramp_1.color_ramp.elements):
                colorramp_1.color_ramp.elements.new(0.0)
            if hasattr(colorramp_1.color_ramp.elements[0], 'alpha'):
                colorramp_1.color_ramp.elements[0].alpha = 1.0
            if hasattr(colorramp_1.color_ramp.elements[0], 'color'):
                colorramp_1.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
            if hasattr(colorramp_1.color_ramp.elements[0], 'position'):
                colorramp_1.color_ramp.elements[0].position = 0.0
            if 1 >= len(colorramp_1.color_ramp.elements):
                colorramp_1.color_ramp.elements.new(1.0)
            if hasattr(colorramp_1.color_ramp.elements[1], 'alpha'):
                colorramp_1.color_ramp.elements[1].alpha = 1.0
            if hasattr(colorramp_1.color_ramp.elements[1], 'color'):
                colorramp_1.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
            if hasattr(colorramp_1.color_ramp.elements[1], 'position'):
                colorramp_1.color_ramp.elements[1].position = 1.0
        if hasattr(colorramp_1.color_ramp, 'hue_interpolation'):
            colorramp_1.color_ramp.hue_interpolation = 'NEAR'
        if hasattr(colorramp_1.color_ramp, 'interpolation'):
            colorramp_1.color_ramp.interpolation = 'LINEAR'
    if hasattr(colorramp_1, 'hide'):
        colorramp_1.hide = False
    if hasattr(colorramp_1, 'location'):
        colorramp_1.location = (-1057.744140625, -89.62713623046875)
    if hasattr(colorramp_1, 'mute'):
        colorramp_1.mute = False
    if hasattr(colorramp_1, 'name'):
        colorramp_1.name = 'ColorRamp'
    if hasattr(colorramp_1, 'use_custom_color'):
        colorramp_1.use_custom_color = False
    if hasattr(colorramp_1, 'width'):
        colorramp_1.width = 240.0
    input_ = next((input_ for input_ in colorramp_1.inputs if input_.identifier=='Fac'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Fac'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in colorramp_1.outputs if output.identifier=='Color'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Color'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in colorramp_1.outputs if output.identifier=='Alpha'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Alpha'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    vector_math_001_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
    if hasattr(vector_math_001_1, 'color'):
        vector_math_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(vector_math_001_1, 'hide'):
        vector_math_001_1.hide = False
    if hasattr(vector_math_001_1, 'location'):
        vector_math_001_1.location = (-1266.610107421875, -412.4996032714844)
    if hasattr(vector_math_001_1, 'mute'):
        vector_math_001_1.mute = False
    if hasattr(vector_math_001_1, 'name'):
        vector_math_001_1.name = 'Vector Math.001'
    if hasattr(vector_math_001_1, 'operation'):
        vector_math_001_1.operation = 'MULTIPLY'
    if hasattr(vector_math_001_1, 'use_custom_color'):
        vector_math_001_1.use_custom_color = False
    if hasattr(vector_math_001_1, 'width'):
        vector_math_001_1.width = 140.0
    input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Vector_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.004000000189989805, 0.004000000189989805, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Vector_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_001_1.inputs if input_.identifier=='Scale'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 1.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Scale'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in vector_math_001_1.outputs if output.identifier=='Vector'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Vector'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in vector_math_001_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = False
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    colorramp_001_1 = node_tree1.nodes.new('ShaderNodeValToRGB')
    if hasattr(colorramp_001_1, 'color'):
        colorramp_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(colorramp_001_1, 'color_ramp'):
        if hasattr(colorramp_001_1.color_ramp, 'color_mode'):
            colorramp_001_1.color_ramp.color_mode = 'RGB'
        if hasattr(colorramp_001_1.color_ramp, 'elements'):
            if 0 >= len(colorramp_001_1.color_ramp.elements):
                colorramp_001_1.color_ramp.elements.new(0.468181848526001)
            if hasattr(colorramp_001_1.color_ramp.elements[0], 'alpha'):
                colorramp_001_1.color_ramp.elements[0].alpha = 1.0
            if hasattr(colorramp_001_1.color_ramp.elements[0], 'color'):
                colorramp_001_1.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
            if hasattr(colorramp_001_1.color_ramp.elements[0], 'position'):
                colorramp_001_1.color_ramp.elements[0].position = 0.468181848526001
            if 1 >= len(colorramp_001_1.color_ramp.elements):
                colorramp_001_1.color_ramp.elements.new(0.6454545259475708)
            if hasattr(colorramp_001_1.color_ramp.elements[1], 'alpha'):
                colorramp_001_1.color_ramp.elements[1].alpha = 1.0
            if hasattr(colorramp_001_1.color_ramp.elements[1], 'color'):
                colorramp_001_1.color_ramp.elements[1].color = (0.05730096995830536, 0.05730096995830536, 0.05730096995830536, 1.0)
            if hasattr(colorramp_001_1.color_ramp.elements[1], 'position'):
                colorramp_001_1.color_ramp.elements[1].position = 0.6454545259475708
        if hasattr(colorramp_001_1.color_ramp, 'hue_interpolation'):
            colorramp_001_1.color_ramp.hue_interpolation = 'NEAR'
        if hasattr(colorramp_001_1.color_ramp, 'interpolation'):
            colorramp_001_1.color_ramp.interpolation = 'EASE'
    if hasattr(colorramp_001_1, 'hide'):
        colorramp_001_1.hide = False
    if hasattr(colorramp_001_1, 'location'):
        colorramp_001_1.location = (-784.2443237304688, -350.30657958984375)
    if hasattr(colorramp_001_1, 'mute'):
        colorramp_001_1.mute = False
    if hasattr(colorramp_001_1, 'name'):
        colorramp_001_1.name = 'ColorRamp.001'
    if hasattr(colorramp_001_1, 'use_custom_color'):
        colorramp_001_1.use_custom_color = False
    if hasattr(colorramp_001_1, 'width'):
        colorramp_001_1.width = 240.0
    input_ = next((input_ for input_ in colorramp_001_1.inputs if input_.identifier=='Fac'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Fac'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in colorramp_001_1.outputs if output.identifier=='Color'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Color'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in colorramp_001_1.outputs if output.identifier=='Alpha'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Alpha'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    colorramp_002_1 = node_tree1.nodes.new('ShaderNodeValToRGB')
    if hasattr(colorramp_002_1, 'color'):
        colorramp_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(colorramp_002_1, 'color_ramp'):
        if hasattr(colorramp_002_1.color_ramp, 'color_mode'):
            colorramp_002_1.color_ramp.color_mode = 'RGB'
        if hasattr(colorramp_002_1.color_ramp, 'elements'):
            if 0 >= len(colorramp_002_1.color_ramp.elements):
                colorramp_002_1.color_ramp.elements.new(0.0)
            if hasattr(colorramp_002_1.color_ramp.elements[0], 'alpha'):
                colorramp_002_1.color_ramp.elements[0].alpha = 1.0
            if hasattr(colorramp_002_1.color_ramp.elements[0], 'color'):
                colorramp_002_1.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
            if hasattr(colorramp_002_1.color_ramp.elements[0], 'position'):
                colorramp_002_1.color_ramp.elements[0].position = 0.0
            if 1 >= len(colorramp_002_1.color_ramp.elements):
                colorramp_002_1.color_ramp.elements.new(1.0)
            if hasattr(colorramp_002_1.color_ramp.elements[1], 'alpha'):
                colorramp_002_1.color_ramp.elements[1].alpha = 1.0
            if hasattr(colorramp_002_1.color_ramp.elements[1], 'color'):
                colorramp_002_1.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
            if hasattr(colorramp_002_1.color_ramp.elements[1], 'position'):
                colorramp_002_1.color_ramp.elements[1].position = 1.0
        if hasattr(colorramp_002_1.color_ramp, 'hue_interpolation'):
            colorramp_002_1.color_ramp.hue_interpolation = 'NEAR'
        if hasattr(colorramp_002_1.color_ramp, 'interpolation'):
            colorramp_002_1.color_ramp.interpolation = 'EASE'
    if hasattr(colorramp_002_1, 'hide'):
        colorramp_002_1.hide = False
    if hasattr(colorramp_002_1, 'location'):
        colorramp_002_1.location = (-794.784423828125, -639.2159423828125)
    if hasattr(colorramp_002_1, 'mute'):
        colorramp_002_1.mute = False
    if hasattr(colorramp_002_1, 'name'):
        colorramp_002_1.name = 'ColorRamp.002'
    if hasattr(colorramp_002_1, 'use_custom_color'):
        colorramp_002_1.use_custom_color = False
    if hasattr(colorramp_002_1, 'width'):
        colorramp_002_1.width = 240.0
    input_ = next((input_ for input_ in colorramp_002_1.inputs if input_.identifier=='Fac'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Fac'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in colorramp_002_1.outputs if output.identifier=='Color'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Color'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in colorramp_002_1.outputs if output.identifier=='Alpha'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Alpha'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_006_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_006_1, 'color'):
        math_006_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_006_1, 'hide'):
        math_006_1.hide = False
    if hasattr(math_006_1, 'location'):
        math_006_1.location = (-397.509033203125, -615.8211669921875)
    if hasattr(math_006_1, 'mute'):
        math_006_1.mute = False
    if hasattr(math_006_1, 'name'):
        math_006_1.name = 'Math.006'
    if hasattr(math_006_1, 'operation'):
        math_006_1.operation = 'MULTIPLY'
    if hasattr(math_006_1, 'use_clamp'):
        math_006_1.use_clamp = False
    if hasattr(math_006_1, 'use_custom_color'):
        math_006_1.use_custom_color = False
    if hasattr(math_006_1, 'width'):
        math_006_1.width = 140.0
    input_ = next((input_ for input_ in math_006_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_006_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 10.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_006_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_006_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_004_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_004_1, 'color'):
        math_004_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_004_1, 'hide'):
        math_004_1.hide = False
    if hasattr(math_004_1, 'location'):
        math_004_1.location = (-386.968994140625, -326.9117431640625)
    if hasattr(math_004_1, 'mute'):
        math_004_1.mute = False
    if hasattr(math_004_1, 'name'):
        math_004_1.name = 'Math.004'
    if hasattr(math_004_1, 'operation'):
        math_004_1.operation = 'MULTIPLY'
    if hasattr(math_004_1, 'use_clamp'):
        math_004_1.use_clamp = False
    if hasattr(math_004_1, 'use_custom_color'):
        math_004_1.use_custom_color = False
    if hasattr(math_004_1, 'width'):
        math_004_1.width = 140.0
    input_ = next((input_ for input_ in math_004_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_004_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 10.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_004_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_004_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    wave_texture_1 = node_tree1.nodes.new('ShaderNodeTexWave')
    if hasattr(wave_texture_1, 'bands_direction'):
        wave_texture_1.bands_direction = 'X'
    if hasattr(wave_texture_1, 'color'):
        wave_texture_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(wave_texture_1, 'hide'):
        wave_texture_1.hide = False
    if hasattr(wave_texture_1, 'location'):
        wave_texture_1.location = (-1065.7056884765625, -631.5020141601562)
    if hasattr(wave_texture_1, 'mute'):
        wave_texture_1.mute = False
    if hasattr(wave_texture_1, 'name'):
        wave_texture_1.name = 'Wave Texture'
    if hasattr(wave_texture_1, 'rings_direction'):
        wave_texture_1.rings_direction = 'X'
    if hasattr(wave_texture_1, 'use_custom_color'):
        wave_texture_1.use_custom_color = False
    if hasattr(wave_texture_1, 'wave_profile'):
        wave_texture_1.wave_profile = 'TRI'
    if hasattr(wave_texture_1, 'wave_type'):
        wave_texture_1.wave_type = 'BANDS'
    if hasattr(wave_texture_1, 'width'):
        wave_texture_1.width = 150.0
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Scale'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.00800000037997961
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Scale'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Distortion'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 14.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Distortion'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Detail'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 10.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Detail'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Detail Scale'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 1.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Detail Scale'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Detail Roughness'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Detail Roughness'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in wave_texture_1.inputs if input_.identifier=='Phase Offset'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 10.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Phase Offset'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in wave_texture_1.outputs if output.identifier=='Color'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Color'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in wave_texture_1.outputs if output.identifier=='Fac'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Fac'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_005_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_005_1, 'color'):
        math_005_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_005_1, 'hide'):
        math_005_1.hide = False
    if hasattr(math_005_1, 'location'):
        math_005_1.location = (-195.2022705078125, -56.4422607421875)
    if hasattr(math_005_1, 'mute'):
        math_005_1.mute = False
    if hasattr(math_005_1, 'name'):
        math_005_1.name = 'Math.005'
    if hasattr(math_005_1, 'operation'):
        math_005_1.operation = 'MULTIPLY'
    if hasattr(math_005_1, 'use_clamp'):
        math_005_1.use_clamp = False
    if hasattr(math_005_1, 'use_custom_color'):
        math_005_1.use_custom_color = False
    if hasattr(math_005_1, 'width'):
        math_005_1.width = 140.0
    input_ = next((input_ for input_ in math_005_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_005_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_005_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_005_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_007_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_007_1, 'color'):
        math_007_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_007_1, 'hide'):
        math_007_1.hide = False
    if hasattr(math_007_1, 'location'):
        math_007_1.location = (12.68963623046875, -68.28890991210938)
    if hasattr(math_007_1, 'mute'):
        math_007_1.mute = False
    if hasattr(math_007_1, 'name'):
        math_007_1.name = 'Math.007'
    if hasattr(math_007_1, 'operation'):
        math_007_1.operation = 'MULTIPLY'
    if hasattr(math_007_1, 'use_clamp'):
        math_007_1.use_clamp = False
    if hasattr(math_007_1, 'use_custom_color'):
        math_007_1.use_custom_color = False
    if hasattr(math_007_1, 'width'):
        math_007_1.width = 140.0
    input_ = next((input_ for input_ in math_007_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_007_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_007_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_007_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_008_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_008_1, 'color'):
        math_008_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_008_1, 'hide'):
        math_008_1.hide = False
    if hasattr(math_008_1, 'location'):
        math_008_1.location = (236.2149658203125, -64.6226806640625)
    if hasattr(math_008_1, 'mute'):
        math_008_1.mute = False
    if hasattr(math_008_1, 'name'):
        math_008_1.name = 'Math.008'
    if hasattr(math_008_1, 'operation'):
        math_008_1.operation = 'DIVIDE'
    if hasattr(math_008_1, 'use_clamp'):
        math_008_1.use_clamp = False
    if hasattr(math_008_1, 'use_custom_color'):
        math_008_1.use_custom_color = False
    if hasattr(math_008_1, 'width'):
        math_008_1.width = 140.0
    input_ = next((input_ for input_ in math_008_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_008_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 5.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_008_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_008_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    combine_xyz_1 = node_tree1.nodes.new('ShaderNodeCombineXYZ')
    if hasattr(combine_xyz_1, 'color'):
        combine_xyz_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(combine_xyz_1, 'hide'):
        combine_xyz_1.hide = False
    if hasattr(combine_xyz_1, 'location'):
        combine_xyz_1.location = (466.69677734375, 18.8077392578125)
    if hasattr(combine_xyz_1, 'mute'):
        combine_xyz_1.mute = False
    if hasattr(combine_xyz_1, 'name'):
        combine_xyz_1.name = 'Combine XYZ'
    if hasattr(combine_xyz_1, 'use_custom_color'):
        combine_xyz_1.use_custom_color = False
    if hasattr(combine_xyz_1, 'width'):
        combine_xyz_1.width = 140.0
    input_ = next((input_ for input_ in combine_xyz_1.inputs if input_.identifier=='X'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'X'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in combine_xyz_1.inputs if input_.identifier=='Y'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Y'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in combine_xyz_1.inputs if input_.identifier=='Z'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Z'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in combine_xyz_1.outputs if output.identifier=='Vector'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Vector'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    set_position_1 = node_tree1.nodes.new('GeometryNodeSetPosition')
    if hasattr(set_position_1, 'color'):
        set_position_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(set_position_1, 'hide'):
        set_position_1.hide = False
    if hasattr(set_position_1, 'location'):
        set_position_1.location = (732.45654296875, 177.203369140625)
    if hasattr(set_position_1, 'mute'):
        set_position_1.mute = False
    if hasattr(set_position_1, 'name'):
        set_position_1.name = 'Set Position'
    if hasattr(set_position_1, 'use_custom_color'):
        set_position_1.use_custom_color = False
    if hasattr(set_position_1, 'width'):
        set_position_1.width = 138.1842041015625
    input_ = next((input_ for input_ in set_position_1.inputs if input_.identifier=='Selection'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = True
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Selection'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in set_position_1.inputs if input_.identifier=='Position'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Position'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in set_position_1.inputs if input_.identifier=='Offset'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Offset'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False

    position_002_1 = node_tree1.nodes.new('GeometryNodeInputPosition')
    if hasattr(position_002_1, 'color'):
        position_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(position_002_1, 'hide'):
        position_002_1.hide = False
    if hasattr(position_002_1, 'location'):
        position_002_1.location = (-1444.07763671875, -385.03790283203125)
    if hasattr(position_002_1, 'mute'):
        position_002_1.mute = False
    if hasattr(position_002_1, 'name'):
        position_002_1.name = 'Position.002'
    if hasattr(position_002_1, 'use_custom_color'):
        position_002_1.use_custom_color = False
    if hasattr(position_002_1, 'width'):
        position_002_1.width = 100.0
    output = next((output for output in position_002_1.outputs if output.identifier=='Position'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Position'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    gradient_texture_1 = node_tree1.nodes.new('ShaderNodeTexGradient')
    if hasattr(gradient_texture_1, 'color'):
        gradient_texture_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(gradient_texture_1, 'gradient_type'):
        gradient_texture_1.gradient_type = 'SPHERICAL'
    if hasattr(gradient_texture_1, 'hide'):
        gradient_texture_1.hide = False
    if hasattr(gradient_texture_1, 'location'):
        gradient_texture_1.location = (-1032.1865234375, -399.82275390625)
    if hasattr(gradient_texture_1, 'mute'):
        gradient_texture_1.mute = False
    if hasattr(gradient_texture_1, 'name'):
        gradient_texture_1.name = 'Gradient Texture'
    if hasattr(gradient_texture_1, 'use_custom_color'):
        gradient_texture_1.use_custom_color = False
    if hasattr(gradient_texture_1, 'width'):
        gradient_texture_1.width = 140.0
    input_ = next((input_ for input_ in gradient_texture_1.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in gradient_texture_1.outputs if output.identifier=='Color'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Color'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in gradient_texture_1.outputs if output.identifier=='Fac'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Fac'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    position_001_1 = node_tree1.nodes.new('GeometryNodeInputPosition')
    if hasattr(position_001_1, 'color'):
        position_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(position_001_1, 'hide'):
        position_001_1.hide = False
    if hasattr(position_001_1, 'location'):
        position_001_1.location = (-1674.4951171875, -450.0364685058594)
    if hasattr(position_001_1, 'mute'):
        position_001_1.mute = False
    if hasattr(position_001_1, 'name'):
        position_001_1.name = 'Position.001'
    if hasattr(position_001_1, 'use_custom_color'):
        position_001_1.use_custom_color = False
    if hasattr(position_001_1, 'width'):
        position_001_1.width = 140.0
    output = next((output for output in position_001_1.outputs if output.identifier=='Position'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Position'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    vector_math_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
    if hasattr(vector_math_1, 'color'):
        vector_math_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(vector_math_1, 'hide'):
        vector_math_1.hide = False
    if hasattr(vector_math_1, 'location'):
        vector_math_1.location = (-1458.2401123046875, -68.27154541015625)
    if hasattr(vector_math_1, 'mute'):
        vector_math_1.mute = False
    if hasattr(vector_math_1, 'name'):
        vector_math_1.name = 'Vector Math'
    if hasattr(vector_math_1, 'operation'):
        vector_math_1.operation = 'ADD'
    if hasattr(vector_math_1, 'use_custom_color'):
        vector_math_1.use_custom_color = False
    if hasattr(vector_math_1, 'width'):
        vector_math_1.width = 140.0
    input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Vector_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Vector_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_1.inputs if input_.identifier=='Scale'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 1.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Scale'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in vector_math_1.outputs if output.identifier=='Vector'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Vector'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in vector_math_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = False
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    combine_xyz_001_1 = node_tree1.nodes.new('ShaderNodeCombineXYZ')
    if hasattr(combine_xyz_001_1, 'color'):
        combine_xyz_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(combine_xyz_001_1, 'hide'):
        combine_xyz_001_1.hide = False
    if hasattr(combine_xyz_001_1, 'location'):
        combine_xyz_001_1.location = (-1675.7265625, -680.0128173828125)
    if hasattr(combine_xyz_001_1, 'mute'):
        combine_xyz_001_1.mute = False
    if hasattr(combine_xyz_001_1, 'name'):
        combine_xyz_001_1.name = 'Combine XYZ.001'
    if hasattr(combine_xyz_001_1, 'use_custom_color'):
        combine_xyz_001_1.use_custom_color = False
    if hasattr(combine_xyz_001_1, 'width'):
        combine_xyz_001_1.width = 140.0
    input_ = next((input_ for input_ in combine_xyz_001_1.inputs if input_.identifier=='X'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'X'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in combine_xyz_001_1.inputs if input_.identifier=='Y'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Y'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in combine_xyz_001_1.inputs if input_.identifier=='Z'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Z'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in combine_xyz_001_1.outputs if output.identifier=='Vector'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND_DOT'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Vector'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    vector_math_002_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
    if hasattr(vector_math_002_1, 'color'):
        vector_math_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(vector_math_002_1, 'hide'):
        vector_math_002_1.hide = False
    if hasattr(vector_math_002_1, 'location'):
        vector_math_002_1.location = (-1418.8975830078125, -645.041015625)
    if hasattr(vector_math_002_1, 'mute'):
        vector_math_002_1.mute = False
    if hasattr(vector_math_002_1, 'name'):
        vector_math_002_1.name = 'Vector Math.002'
    if hasattr(vector_math_002_1, 'operation'):
        vector_math_002_1.operation = 'ADD'
    if hasattr(vector_math_002_1, 'use_custom_color'):
        vector_math_002_1.use_custom_color = False
    if hasattr(vector_math_002_1, 'width'):
        vector_math_002_1.width = 140.0
    input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Vector_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Vector_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in vector_math_002_1.inputs if input_.identifier=='Scale'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 1.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Scale'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in vector_math_002_1.outputs if output.identifier=='Vector'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Vector'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in vector_math_002_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = False
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    value_1 = node_tree1.nodes.new('ShaderNodeValue')
    if hasattr(value_1, 'color'):
        value_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(value_1, 'hide'):
        value_1.hide = False
    if hasattr(value_1, 'location'):
        value_1.location = (-1039.0345458984375, 128.6600341796875)
    if hasattr(value_1, 'mute'):
        value_1.mute = False
    if hasattr(value_1, 'name'):
        value_1.name = 'Value'
    if hasattr(value_1, 'use_custom_color'):
        value_1.use_custom_color = False
    if hasattr(value_1, 'width'):
        value_1.width = 140.0
    output = next((output for output in value_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 30.12345
        if hasattr(output, 'display_shape'):
            output.display_shape = 'CIRCLE'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    math_003_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_003_1, 'color'):
        math_003_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_003_1, 'hide'):
        math_003_1.hide = False
    if hasattr(math_003_1, 'location'):
        math_003_1.location = (-2056.113525390625, -80.286865234375)
    if hasattr(math_003_1, 'mute'):
        math_003_1.mute = False
    if hasattr(math_003_1, 'name'):
        math_003_1.name = 'Math.003'
    if hasattr(math_003_1, 'operation'):
        math_003_1.operation = 'MULTIPLY_ADD'
    if hasattr(math_003_1, 'use_clamp'):
        math_003_1.use_clamp = False
    if hasattr(math_003_1, 'use_custom_color'):
        math_003_1.use_custom_color = False
    if hasattr(math_003_1, 'width'):
        math_003_1.width = 140.0
    input_ = next((input_ for input_ in math_003_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_003_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 100000.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in math_003_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 10000.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Value'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in math_003_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND_DOT'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    group_input_1 = node_tree1.nodes.new('NodeGroupInput')
    if hasattr(group_input_1, 'color'):
        group_input_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(group_input_1, 'hide'):
        group_input_1.hide = False
    if hasattr(group_input_1, 'location'):
        group_input_1.location = (-2557.44189453125, 79.42236328125)
    if hasattr(group_input_1, 'mute'):
        group_input_1.mute = False
    if hasattr(group_input_1, 'name'):
        group_input_1.name = 'Group Input'
    if hasattr(group_input_1, 'use_custom_color'):
        group_input_1.use_custom_color = False
    if hasattr(group_input_1, 'width'):
        group_input_1.width = 140.0

    value_001_1 = node_tree1.nodes.new('ShaderNodeValue')
    if hasattr(value_001_1, 'color'):
        value_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(value_001_1, 'hide'):
        value_001_1.hide = False
    if hasattr(value_001_1, 'location'):
        value_001_1.location = (-2328.45849609375, -130.68389892578125)
    if hasattr(value_001_1, 'mute'):
        value_001_1.mute = False
    if hasattr(value_001_1, 'name'):
        value_001_1.name = 'Value.001'
    if hasattr(value_001_1, 'use_custom_color'):
        value_001_1.use_custom_color = False
    if hasattr(value_001_1, 'width'):
        value_001_1.width = 140.0
    output = next((output for output in value_001_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = uniform(0,10.12345)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'CIRCLE'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Value'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    noise_texture_1 = node_tree1.nodes.new('ShaderNodeTexNoise')
    if hasattr(noise_texture_1, 'color'):
        noise_texture_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(noise_texture_1, 'hide'):
        noise_texture_1.hide = False
    if hasattr(noise_texture_1, 'location'):
        noise_texture_1.location = (-1280.82421875, -97.9427490234375)
    if hasattr(noise_texture_1, 'mute'):
        noise_texture_1.mute = False
    if hasattr(noise_texture_1, 'name'):
        noise_texture_1.name = 'Noise Texture'
    if hasattr(noise_texture_1, 'noise_dimensions'):
        noise_texture_1.noise_dimensions = '3D'
    if hasattr(noise_texture_1, 'use_custom_color'):
        noise_texture_1.use_custom_color = False
    if hasattr(noise_texture_1, 'width'):
        noise_texture_1.width = 140.0
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='Vector'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = (0.0, 0.0, 0.0)
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = True
        if hasattr(input_, 'name'):
            input_.name = 'Vector'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='W'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = False
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'W'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='Scale'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.03999999910593033
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Scale'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='Detail'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 10.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Detail'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='Roughness'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.4000000059604645
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Roughness'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='Distortion'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'DIAMOND_DOT'
        if hasattr(input_, 'enabled'):
            input_.enabled = True
        if hasattr(input_, 'hide'):
            input_.hide = False
        if hasattr(input_, 'hide_value'):
            input_.hide_value = False
        if hasattr(input_, 'name'):
            input_.name = 'Distortion'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    output = next((output for output in noise_texture_1.outputs if output.identifier=='Fac'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Fac'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False
    output = next((output for output in noise_texture_1.outputs if output.identifier=='Color'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = (0.0, 0.0, 0.0, 0.0)
        if hasattr(output, 'display_shape'):
            output.display_shape = 'DIAMOND'
        if hasattr(output, 'enabled'):
            output.enabled = True
        if hasattr(output, 'hide'):
            output.hide = False
        if hasattr(output, 'hide_value'):
            output.hide_value = False
        if hasattr(output, 'name'):
            output.name = 'Color'
        if hasattr(output, 'show_expanded'):
            output.show_expanded = False

    # LINKS
    node_tree1.links.new(subdivide_mesh_1.outputs[0], set_position_1.inputs[0])
    node_tree1.links.new(noise_texture_1.outputs[0], colorramp_1.inputs[0])
    node_tree1.links.new(position_1.outputs[0], set_position_1.inputs[2])
    node_tree1.links.new(position_001_1.outputs[0], vector_math_1.inputs[0])
    node_tree1.links.new(vector_math_1.outputs[0], noise_texture_1.inputs[0])
    node_tree1.links.new(combine_xyz_001_1.outputs[0], vector_math_1.inputs[1])
    node_tree1.links.new(math_1.outputs[0], combine_xyz_001_1.inputs[0])
    node_tree1.links.new(math_002_1.outputs[0], combine_xyz_001_1.inputs[1])
    node_tree1.links.new(math_003_1.outputs[0], combine_xyz_001_1.inputs[2])
    node_tree1.links.new(math_003_1.outputs[0], math_1.inputs[0])
    node_tree1.links.new(math_003_1.outputs[0], math_002_1.inputs[0])
    node_tree1.links.new(position_002_1.outputs[0], vector_math_001_1.inputs[0])
    node_tree1.links.new(vector_math_001_1.outputs[0], gradient_texture_1.inputs[0])
    node_tree1.links.new(gradient_texture_1.outputs[0], colorramp_001_1.inputs[0])
    node_tree1.links.new(colorramp_001_1.outputs[0], math_004_1.inputs[0])
    node_tree1.links.new(math_004_1.outputs[0], math_005_1.inputs[1])
    node_tree1.links.new(combine_xyz_1.outputs[0], set_position_1.inputs[3])
    node_tree1.links.new(math_005_1.outputs[0], math_007_1.inputs[0])
    node_tree1.links.new(colorramp_002_1.outputs[0], math_006_1.inputs[0])
    node_tree1.links.new(colorramp_1.outputs[0], math_005_1.inputs[0])
    node_tree1.links.new(math_006_1.outputs[0], math_007_1.inputs[1])
    node_tree1.links.new(wave_texture_1.outputs[0], colorramp_002_1.inputs[0])
    node_tree1.links.new(math_007_1.outputs[0], math_008_1.inputs[0])
    node_tree1.links.new(math_008_1.outputs[0], combine_xyz_1.inputs[2])
    node_tree1.links.new(position_001_1.outputs[0], vector_math_002_1.inputs[0])
    node_tree1.links.new(vector_math_002_1.outputs[0], wave_texture_1.inputs[0])
    node_tree1.links.new(combine_xyz_001_1.outputs[0], vector_math_002_1.inputs[1])
    node_tree1.links.new(value_1.outputs[0], subdivide_mesh_1.inputs[1])
    node_tree1.links.new(group_input_1.outputs[0], subdivide_mesh_1.inputs[0])
    node_tree1.links.new(set_position_1.outputs[0], group_output_1.inputs[0])
    node_tree1.links.new(value_001_1.outputs[0], math_003_1.inputs[0])

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


