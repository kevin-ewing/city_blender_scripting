import bpy

# MATERIAL
node_tree1 = bpy.data.node_groups.get('mountains')
if not node_tree1:
    node_tree1 = bpy.data.node_groups.new('mountains', 'GeometryNodeTree')

    for node in node_tree1.nodes:
        node_tree1.nodes.remove(node)
    # INPUTS
    input = node_tree1.inputs.new('NodeSocketGeometry', 'Mesh')
    if hasattr(input, 'attribute_domain'):
        input.attribute_domain = 'POINT'
    if hasattr(input, 'hide_value'):
        input.hide_value = False
    if hasattr(input, 'name'):
        input.name = 'Mesh'
    input = node_tree1.inputs.new('NodeSocketFloat', 'Value')
    if hasattr(input, 'attribute_domain'):
        input.attribute_domain = 'POINT'
    if hasattr(input, 'default_value'):
        input.default_value = 0.5
    if hasattr(input, 'hide_value'):
        input.hide_value = False
    if hasattr(input, 'max_value'):
        input.max_value = 10000.0
    if hasattr(input, 'min_value'):
        input.min_value = -10000.0
    if hasattr(input, 'name'):
        input.name = 'Value'
    input = node_tree1.inputs.new('NodeSocketFloat', 'Value')
    if hasattr(input, 'attribute_domain'):
        input.attribute_domain = 'POINT'
    if hasattr(input, 'default_value'):
        input.default_value = 0.5
    if hasattr(input, 'hide_value'):
        input.hide_value = False
    if hasattr(input, 'max_value'):
        input.max_value = 10000.0
    if hasattr(input, 'min_value'):
        input.min_value = -10000.0
    if hasattr(input, 'name'):
        input.name = 'Value'
    # OUTPUTS
    output = node_tree1.outputs.new('NodeSocketGeometry', 'Geometry')
    if hasattr(output, 'attribute_domain'):
        output.attribute_domain = 'POINT'
    if hasattr(output, 'hide_value'):
        output.hide_value = False
    if hasattr(output, 'name'):
        output.name = 'Geometry'
    # NODES
    subdivide_mesh_1 = node_tree1.nodes.new('GeometryNodeSubdivideMesh')
    if hasattr(subdivide_mesh_1, 'color'):
        subdivide_mesh_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(subdivide_mesh_1, 'hide'):
        subdivide_mesh_1.hide = False
    if hasattr(subdivide_mesh_1, 'location'):
        subdivide_mesh_1.location = (122.474609375, 448.49481201171875)
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

    math_001_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_001_1, 'color'):
        math_001_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_001_1, 'hide'):
        math_001_1.hide = False
    if hasattr(math_001_1, 'location'):
        math_001_1.location = (-160.6524658203125, 320.966064453125)
    if hasattr(math_001_1, 'mute'):
        math_001_1.mute = False
    if hasattr(math_001_1, 'name'):
        math_001_1.name = 'Math.001'
    if hasattr(math_001_1, 'operation'):
        math_001_1.operation = 'MULTIPLY'
    if hasattr(math_001_1, 'use_clamp'):
        math_001_1.use_clamp = False
    if hasattr(math_001_1, 'use_custom_color'):
        math_001_1.use_custom_color = False
    if hasattr(math_001_1, 'width'):
        math_001_1.width = 140.0
    input_ = next((input_ for input_ in math_001_1.inputs if input_.identifier=='Value'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
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
    input_ = next((input_ for input_ in math_001_1.inputs if input_.identifier=='Value_001'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 2.0
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
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
    input_ = next((input_ for input_ in math_001_1.inputs if input_.identifier=='Value_002'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.5
        if hasattr(input_, 'display_shape'):
            input_.display_shape = 'CIRCLE'
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
    output = next((output for output in math_001_1.outputs if output.identifier=='Value'), None)
    if output:
        if hasattr(output, 'default_value'):
            output.default_value = 0.0
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

    position_1 = node_tree1.nodes.new('GeometryNodeInputPosition')
    if hasattr(position_1, 'color'):
        position_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(position_1, 'hide'):
        position_1.hide = False
    if hasattr(position_1, 'location'):
        position_1.location = (204.280029296875, 264.4905090332031)
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
        math_002_1.location = (-1201.5321044921875, -5.7949981689453125)
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

    math_003_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_003_1, 'color'):
        math_003_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_003_1, 'hide'):
        math_003_1.hide = False
    if hasattr(math_003_1, 'location'):
        math_003_1.location = (-1394.2850341796875, 110.43426513671875)
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

    math_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_1, 'color'):
        math_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_1, 'hide'):
        math_1.hide = False
    if hasattr(math_1, 'location'):
        math_1.location = (-1198.850830078125, 132.34646606445312)
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

    noise_texture_1 = node_tree1.nodes.new('ShaderNodeTexNoise')
    if hasattr(noise_texture_1, 'color'):
        noise_texture_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(noise_texture_1, 'hide'):
        noise_texture_1.hide = False
    if hasattr(noise_texture_1, 'location'):
        noise_texture_1.location = (-618.9957275390625, 92.77838134765625)
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
            input_.default_value = 0.05000000074505806
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
            input_.name = 'Detail'
        if hasattr(input_, 'show_expanded'):
            input_.show_expanded = False
    input_ = next((input_ for input_ in noise_texture_1.inputs if input_.identifier=='Roughness'), None)
    if input_:
        if hasattr(input_, 'default_value'):
            input_.default_value = 0.10000000149011612
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
        colorramp_1.location = (-395.9156494140625, 101.093994140625)
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
        vector_math_001_1.location = (-604.7816162109375, -221.77847290039062)
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
            input_.default_value = (0.0044999998062849045, 0.0044999998062849045, 0.0044999998062849045)
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
                colorramp_001_1.color_ramp.elements.new(0.0)
            if hasattr(colorramp_001_1.color_ramp.elements[0], 'alpha'):
                colorramp_001_1.color_ramp.elements[0].alpha = 1.0
            if hasattr(colorramp_001_1.color_ramp.elements[0], 'color'):
                colorramp_001_1.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
            if hasattr(colorramp_001_1.color_ramp.elements[0], 'position'):
                colorramp_001_1.color_ramp.elements[0].position = 0.0
            if 1 >= len(colorramp_001_1.color_ramp.elements):
                colorramp_001_1.color_ramp.elements.new(0.7886362671852112)
            if hasattr(colorramp_001_1.color_ramp.elements[1], 'alpha'):
                colorramp_001_1.color_ramp.elements[1].alpha = 1.0
            if hasattr(colorramp_001_1.color_ramp.elements[1], 'color'):
                colorramp_001_1.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
            if hasattr(colorramp_001_1.color_ramp.elements[1], 'position'):
                colorramp_001_1.color_ramp.elements[1].position = 0.7886362671852112
        if hasattr(colorramp_001_1.color_ramp, 'hue_interpolation'):
            colorramp_001_1.color_ramp.hue_interpolation = 'NEAR'
        if hasattr(colorramp_001_1.color_ramp, 'interpolation'):
            colorramp_001_1.color_ramp.interpolation = 'EASE'
    if hasattr(colorramp_001_1, 'hide'):
        colorramp_001_1.hide = False
    if hasattr(colorramp_001_1, 'location'):
        colorramp_001_1.location = (-122.41583251953125, -159.58544921875)
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
        colorramp_002_1.location = (-132.9559326171875, -448.49481201171875)
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
        math_006_1.location = (264.3194580078125, -425.10003662109375)
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

    wave_texture_1 = node_tree1.nodes.new('ShaderNodeTexWave')
    if hasattr(wave_texture_1, 'bands_direction'):
        wave_texture_1.bands_direction = 'X'
    if hasattr(wave_texture_1, 'color'):
        wave_texture_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(wave_texture_1, 'hide'):
        wave_texture_1.hide = False
    if hasattr(wave_texture_1, 'location'):
        wave_texture_1.location = (-403.877197265625, -440.7808837890625)
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
            input_.default_value = 0.004000000189989805
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
        math_005_1.location = (466.626220703125, 134.27886962890625)
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
        math_007_1.location = (674.5181274414062, 122.43222045898438)
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

    combine_xyz_1 = node_tree1.nodes.new('ShaderNodeCombineXYZ')
    if hasattr(combine_xyz_1, 'color'):
        combine_xyz_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(combine_xyz_1, 'hide'):
        combine_xyz_1.hide = False
    if hasattr(combine_xyz_1, 'location'):
        combine_xyz_1.location = (1128.5252685546875, 209.52886962890625)
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
        set_position_1.location = (1394.2850341796875, 367.92449951171875)
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

    group_input_1 = node_tree1.nodes.new('NodeGroupInput')
    if hasattr(group_input_1, 'color'):
        group_input_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(group_input_1, 'hide'):
        group_input_1.hide = False
    if hasattr(group_input_1, 'location'):
        group_input_1.location = (-1594.2850341796875, -0.0)
    if hasattr(group_input_1, 'mute'):
        group_input_1.mute = False
    if hasattr(group_input_1, 'name'):
        group_input_1.name = 'Group Input'
    if hasattr(group_input_1, 'use_custom_color'):
        group_input_1.use_custom_color = False
    if hasattr(group_input_1, 'width'):
        group_input_1.width = 140.0
    if hasattr(group_input_1.outputs[1], 'default_value'):
        group_input_1.outputs[1].default_value = 0.5
    if hasattr(group_input_1.outputs[1], 'display_shape'):
        group_input_1.outputs[1].display_shape = 'CIRCLE'
    if hasattr(group_input_1.outputs[1], 'enabled'):
        group_input_1.outputs[1].enabled = True
    if hasattr(group_input_1.outputs[1], 'hide'):
        group_input_1.outputs[1].hide = False
    if hasattr(group_input_1.outputs[1], 'hide_value'):
        group_input_1.outputs[1].hide_value = False
    if hasattr(group_input_1.outputs[1], 'name'):
        group_input_1.outputs[1].name = 'Value'
    if hasattr(group_input_1.outputs[1], 'show_expanded'):
        group_input_1.outputs[1].show_expanded = False
    if hasattr(group_input_1.outputs[2], 'default_value'):
        group_input_1.outputs[2].default_value = 0.5
    if hasattr(group_input_1.outputs[2], 'display_shape'):
        group_input_1.outputs[2].display_shape = 'DIAMOND'
    if hasattr(group_input_1.outputs[2], 'enabled'):
        group_input_1.outputs[2].enabled = True
    if hasattr(group_input_1.outputs[2], 'hide'):
        group_input_1.outputs[2].hide = False
    if hasattr(group_input_1.outputs[2], 'hide_value'):
        group_input_1.outputs[2].hide_value = False
    if hasattr(group_input_1.outputs[2], 'name'):
        group_input_1.outputs[2].name = 'Value'
    if hasattr(group_input_1.outputs[2], 'show_expanded'):
        group_input_1.outputs[2].show_expanded = False

    group_output_1 = node_tree1.nodes.new('NodeGroupOutput')
    if hasattr(group_output_1, 'color'):
        group_output_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(group_output_1, 'hide'):
        group_output_1.hide = False
    if hasattr(group_output_1, 'is_active_output'):
        group_output_1.is_active_output = True
    if hasattr(group_output_1, 'location'):
        group_output_1.location = (1582.46923828125, -0.0)
    if hasattr(group_output_1, 'mute'):
        group_output_1.mute = False
    if hasattr(group_output_1, 'name'):
        group_output_1.name = 'Group Output'
    if hasattr(group_output_1, 'use_custom_color'):
        group_output_1.use_custom_color = False
    if hasattr(group_output_1, 'width'):
        group_output_1.width = 140.0

    position_002_1 = node_tree1.nodes.new('GeometryNodeInputPosition')
    if hasattr(position_002_1, 'color'):
        position_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(position_002_1, 'hide'):
        position_002_1.hide = False
    if hasattr(position_002_1, 'location'):
        position_002_1.location = (-782.2491455078125, -194.3167724609375)
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
        gradient_texture_1.location = (-370.3580322265625, -209.10162353515625)
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
        position_001_1.location = (-1012.6666259765625, -259.3153381347656)
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
        vector_math_1.location = (-796.41162109375, 122.4495849609375)
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
        combine_xyz_001_1.location = (-1013.8980712890625, -489.29168701171875)
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
            input_.display_shape = 'DIAMOND'
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
            input_.display_shape = 'DIAMOND'
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
    output = next((output for output in combine_xyz_001_1.outputs if output.identifier=='Vector'), None)
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

    vector_math_002_1 = node_tree1.nodes.new('ShaderNodeVectorMath')
    if hasattr(vector_math_002_1, 'color'):
        vector_math_002_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(vector_math_002_1, 'hide'):
        vector_math_002_1.hide = False
    if hasattr(vector_math_002_1, 'location'):
        vector_math_002_1.location = (-757.069091796875, -454.31988525390625)
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

    math_004_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_004_1, 'color'):
        math_004_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_004_1, 'hide'):
        math_004_1.hide = False
    if hasattr(math_004_1, 'location'):
        math_004_1.location = (220.59957885742188, -66.66891479492188)
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

    math_008_1 = node_tree1.nodes.new('ShaderNodeMath')
    if hasattr(math_008_1, 'color'):
        math_008_1.color = (0.6079999804496765, 0.6079999804496765, 0.6079999804496765)
    if hasattr(math_008_1, 'hide'):
        math_008_1.hide = False
    if hasattr(math_008_1, 'location'):
        math_008_1.location = (898.04345703125, 126.09844970703125)
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

    # LINKS
    node_tree1.links.new(group_input_1.outputs[0], subdivide_mesh_1.inputs[0])
    node_tree1.links.new(group_input_1.outputs[1], math_001_1.inputs[0])
    node_tree1.links.new(set_position_1.outputs[0], group_output_1.inputs[0])
    node_tree1.links.new(group_input_1.outputs[2], math_003_1.inputs[0])
    node_tree1.links.new(subdivide_mesh_1.outputs[0], set_position_1.inputs[0])
    node_tree1.links.new(math_001_1.outputs[0], subdivide_mesh_1.inputs[1])
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

    # TO ACTIVE
selected_objects = (obj for obj in bpy.data.objects if obj.select_get())
for obj in selected_objects:
    modifier = obj.modifiers.new(name='mountains', type='NODES')
    modifier.node_group = node_tree1
