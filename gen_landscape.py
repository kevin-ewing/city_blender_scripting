import bpy
import time
from random import *
from math import *
from dataclasses import dataclass
from array import *
import sys
from colorsys import hsv_to_rgb

RENDER = False

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
   
    #Clearing all objects and materials from the prior scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.context.scene.render.engine = 'CYCLES'
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
        
#    for geom_node in bpy.ops.node:
#        bpy.ops.node.delete(geom_node)
    

    #Adds floor facing the camera
    mat = bpy.data.materials.new(name="floor")
    mat.use_nodes = True
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs["Metallic"].default_value = 0.65
            n.inputs["Roughness"].default_value = 0.15
            

    path = "/Users/kewing/Desktop/sp22/anim/blender/city/dependencies/geom_node_tree.blend\\NodeTree\\Mountains\\"
    material_name = "mountains"
    bpy.ops.wm.append( filename = material_name, directory = path)

    
    bpy.ops.mesh.primitive_plane_add(size=400, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.ops.object.modifier_add(type='NODES')
    bpy.context.object.data.materials.append(mat)
    
    world_fixed_color = uniform(0.4,0.85)
    world_saturation = uniform(0.1, 0.5)
    world_value = uniform(0.2, 1)

    #Sets world color 
    world_strength = uniform(0, 10)
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (hsv_to_rgb(world_fixed_color, world_saturation, world_value)[0], hsv_to_rgb(world_fixed_color, world_saturation, world_value)[1],hsv_to_rgb(world_fixed_color, world_saturation, world_value)[2], world_strength)
    


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

if __name__ == "__main__":  
    start_checkpoint = time.time()
    run_ops_without_view_layer_update(main)
    if RENDER:
        print("Rendering...")
        checkpoint = time.time()
        bpy.context.scene.render.filepath = "./output/o" + sys.argv[7]
        bpy.context.scene.cycles.samples = 1024 * RENDER_SAMPLE_FACTOR
        bpy.context.scene.render.resolution_x = 3840 * RENDER_SIZE_FACTOR
        bpy.context.scene.render.resolution_y = 1644 * RENDER_SIZE_FACTOR
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=True)
        print("--- %s seconds ---\n" % (time.time() - checkpoint))
        print("Total Time: --- %s seconds ---\n"% (time.time() - start_checkpoint))

