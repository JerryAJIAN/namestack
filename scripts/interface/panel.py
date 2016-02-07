
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  this program; if not, write to the Free Software Foundation, Inc.,
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import re
import os
from bpy.types import Panel
from .. import storage
from . import icon

# addon
addon = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# name
class name(Panel):
  '''
    Name panel.
  '''
  bl_idname = 'VIEW3D_PT_name'
  bl_space_type = 'VIEW_3D'
  bl_label = 'Name'
  bl_region_type = 'TOOLS'
  bl_options = {'HIDE_HEADER'}
  bl_category = 'Name'

  # draw
  def draw(self, context):
    '''
      Name panel body.
    '''


    # layout
    layout = self.layout

    # option
    option = context.scene.NamePanel

    # selected objects
    selectedObjects = [
      # [object.name, object]
    ]

    # column
    column = layout.column(align=True)

    # filter
    filters(self, context, column, option)

    # search
    search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

    # member
    member = {object.name: [] for object in context.selected_objects[:]}

    # member
    member = gather(context, member)
    # print(member)

    # selected
    if option.selected:

      # objects
      for object in context.selected_objects[:]:
        selectedObjects.append([object.name, object])
    if selectedObjects != []:

      # pin active object
      if option.pinActiveObject:
        if context.active_object:

          # search
          if search == '' or re.search(search, context.active_object.name) or [re.search(search, item) for item in member[context.active_object.name]]:

            # populate
            populate(self, context, layout, context.active_object, option)

        # selected
        if option.selected:

          # sorted
          for datablock in sorted(selectedObjects):
            if datablock[1] != context.active_object:

              # search
              if search == '' or re.search(search, datablock[1].name) or [re.search(search, item) for item in member[object.name]]:

                # populate
                populate(self, context, layout, datablock[1], option)
      else:

        # sorted
        for datablock in sorted(selectedObjects):

          # search
          if search == '' or re.search(search, datablock[1].name) or [re.search(search, item) for item in member[object.name]]:

            # populate
            populate(self, context, layout, datablock[1], option)

    else:
      column = layout.column()
      column.label('Nothing to show.')

# filters
def filters(self, context, layout, option):
  '''
    The name panel filters
  '''

  # row
  row = layout.row(align=True)

  # scale
  row.scale_y = 1.25

  # icon toggle
  if option.filters:
    iconToggle = 'RADIOBUT_ON'
  else:
    iconToggle = 'RADIOBUT_OFF'

  # filters
  row.prop(option, 'filters', text='Filters', icon=iconToggle, toggle=True)

  # options
  row.prop(option, 'options', text='', icon='SETTINGS')

  # selected
  row.prop(option, 'selected', text='', icon='OOPS')

  # operator menu
  row.menu('VIEW3D_MT_name_panel_specials', text='', icon='COLLAPSEMENU')

  # filters
  if option.filters:

    # row 1
    row = layout.row(align=True)

    # scale
    row.scale_x = 5 # hack: forces buttons to line up correctly

    # groups
    row.prop(option, 'groups', text='', icon='GROUP')

    # action
    row.prop(option, 'action', text='', icon='ACTION')

    # grease pencil
    row.prop(option, 'greasePencil', text='', icon='GREASEPENCIL')

    # constraints
    row.prop(option, 'constraints', text='', icon='CONSTRAINT')

    # modifiers
    row.prop(option, 'modifiers', text='', icon='MODIFIER')

    # bone groups
    row.prop(option, 'boneGroups', text='', icon='GROUP_BONE')

    # bone constraints
    row.prop(option, 'boneConstraints', text='', icon='CONSTRAINT_BONE')

    # row 2
    row = layout.row(align=True)

    # scale
    row.scale_x = 5 # hack: forces buttons to line up correctly

    # vertex groups
    row.prop(option, 'vertexGroups', text='', icon='GROUP_VERTEX')

    # shapekeys
    row.prop(option, 'shapekeys', text='', icon='SHAPEKEY_DATA')

    # uvs
    row.prop(option, 'uvs', text='', icon='GROUP_UVS')

    # vertex colors
    row.prop(option, 'vertexColors', text='', icon='GROUP_VCOL')

    # materials
    row.prop(option, 'materials', text='', icon='MATERIAL')

    # textures
    row.prop(option, 'textures', text='', icon='TEXTURE')

    # particles systems
    row.prop(option, 'particleSystems', text='', icon='PARTICLES')

  # row
  row = layout.row(align=True)

  # search
  row.prop(option, 'search', text='', icon='VIEWZOOM')
  row.operator('wm.regular_expression_cheatsheet', text='', icon='FILE_TEXT')
  row.prop(option, 'regex', text='', icon='SCRIPTPLUGINS')

# attached
def gather(context, member):
  '''
    Creates a object datablock dictionary for name panel.
  '''

  # option
  option = context.scene.NamePanel

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  for object in context.selected_objects:

    # group
    if option.groups:
      for group in bpy.data.groups[:]:
        for groupobject in group.objects[:]:
          if groupobject == object:

            # search
            if search == '' or re.search(search, group.name):

              # member
              member[object.name].append(group.name)

    # action
    if option.action:
      if hasattr(object.animation_data, 'action'):
        if hasattr(object.animation_data.action, 'name'):

          # search
          if search == '' or re.search(search, object.animation_data.action.name):

            member[object.name].append(object.animation_data.action.name)

    # grease pencil
    if option.greasePencil:
      if hasattr(object.grease_pencil, 'name'):

        # layers
        layers = [layer.info for layer in bpy.data.objects[object.name].grease_pencil.layers[:]]

        # search
        if search == '' or re.search(search, object.grease_pencil.name) or [re.search(search, item) for item in layers]:

          # member
          member[object.name].append(object.grease_pencil.name)

          # pencil layers
          for layer in bpy.data.objects[object.name].grease_pencil.layers[:]:

            # search
            if search == '' or re.search(search, layer.info):

              # member
              member[object.name].append(layer.info)

    # constraints
    if option.constraints:
      for constraint in object.constraints[:]:

        # search
        if search == '' or re.search(search, constraint.name):

          # attached
          member[object.name].append(constraint.name)

    # modifiers
    if option.modifiers:
      for modifier in object.modifiers[:]:
        if modifier.type in 'PARTICLE_SYSTEM':

          # particle
          particle = modifier.particle_system.name

        else:

          # particle
          particle = ''

        # search
        if search == '' or re.search(search, modifier.name) or re.search(search, particle):

          # member
          member[object.name].append(modifier.name)

          # particle systems
          if option.particleSystems:
            if modifier.type in 'PARTICLE_SYSTEM':

              # search
              if search == '' or re.search(search, modifier.particle_system.name):

                # member
                member[object.name].append(modifier.particle_system.name)

                if search == '' or re.search(search, modifier.particle_system.settings.name):

                  # member
                  member[object.name].append(modifier.particle_system.settings.name)

    # materials
    if option.materials:
      for slot in object.material_slots:
        if slot.material != None:

          # textures
          textures = [tslot.texture.name for tslot in slot.material.texture_slots[:] if hasattr(tslot, 'texture')]

          # search
          if search == '' or re.search(search, slot.material.name) or [re.search(search, item) for item in textures]:

            # member
            member[object.name].append(slot.material.name)

            # textures
            if option.textures:
              if context.scene.render.engine in {'BLENDER_RENDER', 'BLENDER_GAME'}:
                for tslot in slot.material.texture_slots[:]:
                  if hasattr(tslot, 'texture'):
                    if tslot.texture != None:

                      # search
                      if search == '' or re.search(search, tslot.texture.name):

                        # member
                        member[object.name].append(tslot.texture.name)


    # object data
    if object.type != 'EMPTY':

      if search == '' or re.search(search, object.data.name):

        # member
        member[object.name].append(object.data.name)

    # vertex groups
    if option.vertexGroups:
      if hasattr(object, 'vertex_groups'):
        for group in object.vertex_groups[:]:

          # search
          if search == '' or re.search(search, group.name):

            # member
            member[object.name].append(group.name)

    # shapekeys
    if option.shapekeys:
      if hasattr(object.data, 'shape_keys'):
        if hasattr(object.data.shape_keys, 'key_blocks'):
          for key in object.data.shape_keys.key_blocks[:]:

            # search
            if search == '' or re.search(search, key.name):

              # member
              member[object.name].append(key.name)

    # uvs
    if option.uvs:
      if object.type in 'MESH':
        for uv in object.data.uv_textures[:]:

          # search
          if search == '' or re.search(search, uv.name):

            # member
            member[object.name].append(uv.name)

    # vertex colors
    if option.vertexColors:
      if object.type in 'MESH':
        for vertexColor in object.data.vertex_colors[:]:

          # search
          if search == '' or re.search(search, vertexColor.name):

            # member
            member[object.name].append(vertexColor.name)

    # bone groups
    if option.boneGroups:
      if object.type in 'ARMATURE':
        for group in object.pose.bone_groups[:]:

          # search
          if search == '' or re.search(search, group.name):

            # member
            member[object.name].append(group.name)

    # bones
    if object.type in 'ARMATURE':
      if object.mode in {'POSE', 'EDIT'}:

        # bones
        if object.mode in 'POSE':
          bone = context.active_bone
        else:
          bone = context.active_bone

        # constraints
        constraints = [constraint.name for constraint in bone.constraints]

        # search
        if search == '' or re.search(search, bone.name) or [re.search(search, item) for item in constraints]:

          # member
          member[object.name].append(bone.name)

        # bone constraints
        if option.boneConstraints:
          if object.mode in 'POSE':
            bone = context.active_pose_bone
            for constraint in bone.constraints[:]:

              # search
              if search == '' or re.search(search, constraint.name):

                # member
                member[object.name].append(constraint.name)

        # selected bones
        if option.selectedBones:

          # edit mode
          if object.mode in 'POSE':
            bones = object.data.bones[:]

          # pose mode
          else:
            bones = object.data.edit_bones[:]

          # sort and display
          for bone in bones:
            if bone.name != context.active_bone:

              # constraints
              constraints = [constraint.name for constraint in object.pose.bones[bone.name].constraints[:]]

              # search
              if search == '' or re.search(search, bone.name) or [re.search(search, item) for item in constraints]:

                # member
                member[object.name].append(bone.name)

              # bone constraints
              if option.boneConstraints:
                if object.mode in 'POSE':
                  for constraint in object.pose.bones[bone.name].constraints[:]:

                    # search
                    if search == '' or re.search(search, constraint.name):

                      # member
                      member[object.name].append(constraint.name)

  return member

# populate
def populate(self, context, layout, object, option):
  '''
    Populates the name panel with datablock names.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # column
  column = layout.column()

  # object
  Object(self, context, column, object, option)

  # group
  block.object.group(self, context, column, object, option)

  # action
  block.object.action(self, context, column, object, option)

  # grease pencil
  block.object.greasePencil(self, context, column, object, option)

  # constraint
  block.object.constraint(self, context, column, object, option)

  # modifier
  block.object.modifier(self, context, column, object, option)

  # material
  block.object.material(self, context, column, object, option)

  # object data
  ObjectData(self, context, column, object, option)

  # vertex group
  block.objectData.vertexGroup(self, context, column, object, option)

  # shapekey
  block.objectData.shapekey(self, context, column, object, option)

  # uv
  block.objectData.uv(self, context, column, object, option)

  # vertex color
  block.objectData.vertexColor(self, context, column, object, option)

  # material
  block.objectData.material(self, context, column, object, option)

  # bone group
  block.objectData.boneGroup(self, context, column, object, option)

  # bones
  block.bone(self, context, column, object, option)

# block
class block:
  '''
    contains classes;
      object
      objectData

    contains functions;
      bone
      material
  '''

  # object
  class object:
    '''
      contains functions;
        group
        action
        greasepencil
        constraint
        modifier
        material
    '''

    # group
    def group(self, context, layout, object, option):
      '''
        group related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # groups
      if option.groups:
        for group in bpy.data.groups[:]:
          for groupobject in group.objects[:]:
            if groupobject == object:

              # search
              if search == '' or re.search(search, group.name):

                # group
                Group(self, context, layout, group, object)

    # action
    def action(self, context, layout, object, option):
      '''
        action related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # action
      if option.action:
        if hasattr(object.animation_data, 'action'):
          if hasattr(object.animation_data.action, 'name'):

            # search
            if search == '' or re.search(search, object.animation_data.action.name):

              # action
              Action(self, context, layout, object.animation_data.action, object)

    # greasePencil
    def greasePencil(self, context, layout, object, option):
      '''
        grease pencil related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # grease pencil
      if option.greasePencil:
        if hasattr(object.grease_pencil, 'name'):

          # layers
          layers = [layer.info for layer in bpy.data.objects[object.name].grease_pencil.layers[:]]

          # search
          if search == '' or re.search(search, object.grease_pencil.name) or [re.search(search, item) for item in layers]:

            # grease pencil
            GreasePencil(self, context, layout, object.grease_pencil, object, option)

            # pencil layers
            for layer in bpy.data.objects[object.name].grease_pencil.layers[:]:

              # search
              if search == '' or re.search(search, layer.info):

                # pencil layer
                PencilLayer(self, context, layout, layer, object, option)

    # constraint
    def constraint(self, context, layout, object, option):
      '''
        Constraint related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # constraints
      if option.constraints:
        for constraint in object.constraints[:]:

          # search
          if search == '' or re.search(search, constraint.name):

            # constraint
            Constraint(self, context, layout, constraint, object, None, option)

    # modifier
    def modifier(self, context, layout, object, option):
      '''
        Modifier related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # modifiers
      if option.modifiers:
        for modifier in object.modifiers[:]:
          if modifier.type in 'PARTICLE_SYSTEM':

            # particle
            particle = [modifier.particle_system.name, modifier.particle_system.settings.name]

          else:

            # particle
            particle = []

          # search
          if search == '' or re.search(search, modifier.name) or [re.search(search, item) for item in particle]:

            # modifier
            Modifier(self, context, layout, modifier, object, option)

            # particle systems
            if option.particleSystems:
              if modifier.type in 'PARTICLE_SYSTEM':

                # search
                if search == '' or re.search(search, modifier.particle_system.name) or re.search(search, modifier.particle_system.settings.name):

                  # particle
                  Particle(self, context, layout, modifier, object, option)

      else:
        context.scene['NamePanel']['particleSystems'] = 0

    # material
    def material(self, context, layout, object, option):
      '''
        Material related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # materials
      if option.materials:
        for slot in object.material_slots:
          if slot.link == 'OBJECT':
            if slot.material != None:

              # textures
              textures = [tslot.texture.name for tslot in slot.material.texture_slots[:]]

              # search
              if search == '' or re.search(search, slot.material.name) or [re.search(search, item) for item in textures]:

                # material
                Material(self, context, layout, slot, object, option)

                # textures
                if option.textures:
                  if context.scene.render.engine in {'BLENDER_RENDER', 'BLENDER_GAME'}:
                    for tslot in slot.material.texture_slots[:]:
                      if hasattr(tslot, 'texture'):
                        if tslot.texture != None:

                          # search
                          if search == '' or re.search(search, tslot.texture.name):

                            # texture
                            Texture(self, context, layout, tslot, object, option)

      else:
        context.scene['NamePanel']['textures'] = 0


  # object data
  class objectData:
    '''
      Constains Functions;
        vertexGroup
        shapekey
        uv
        vertexColor
        material
        boneGroup
    '''

    # vertex group
    def vertexGroup(self, context, layout, object, option):
      '''
        Vertex group related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # vertex groups
      if option.vertexGroups:
        if hasattr(object, 'vertex_groups'):
          for group in object.vertex_groups[:]:

            # search
            if search == '' or re.search(search, group.name):

              # vertex group
              VertexGroup(self, context, layout, group, object, option)

    # shapekey
    def shapekey(self, context, layout, object, option):
      '''
        Shapekey related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # shapekeys
      if option.shapekeys:
        if hasattr(object.data, 'shape_keys'):
          if hasattr(object.data.shape_keys, 'key_blocks'):
            for key in object.data.shape_keys.key_blocks[:]:

              # search
              if search == '' or re.search(search, key.name):

                # shapekey
                Shapekey(self, context, layout, key, object, option)

    # uv
    def uv(self, context, layout, object, option):
      '''
        UV related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # uvs
      if option.uvs:
        if object.type in 'MESH':
          for uv in object.data.uv_textures[:]:

            # search
            if search == '' or re.search(search, uv.name):

              # uv
              UV(self, context, layout, uv, object, option)

    # vertex color
    def vertexColor(self, context, layout, object, option):
      '''
        Vertex color related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # vertex colors
      if option.vertexColors:
        if object.type in 'MESH':
          for vertexColor in object.data.vertex_colors[:]:

            # search
            if search == '' or re.search(search, vertexColor.name):

              # vertex color
              VertexColor(self, context, layout, vertexColor, object, option)

    # material
    def material(self, context, layout, object, option):
      '''
        Material related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # materials
      if option.materials:
        for slot in object.material_slots:
          if slot.link == 'DATA':
            if slot.material != None:

              # textures
              textures = [tslot.texture.name for tslot in slot.material.texture_slots[:] if tslot != None]

              # search
              if search == '' or re.search(search, slot.material.name) or [re.search(search, item) for item in textures]:

                # material
                Material(self, context, layout, slot, object, option)

                # textures
                if option.textures:
                  if context.scene.render.engine in {'BLENDER_RENDER', 'BLENDER_GAME'}:
                    for tslot in slot.material.texture_slots[:]:
                      if hasattr(tslot, 'texture'):
                        if tslot.texture != None:

                          # search
                          if search == '' or re.search(search, tslot.texture.name):

                            # texture
                            Texture(self, context, layout, tslot, object, option)
      else:
        context.scene['NamePanel']['textures'] = 0

    # bone groups
    def boneGroup(self, context, layout, object, option):
      '''
        Bone group related code block.
      '''

      # search
      search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

      # bone groups
      if option.boneGroups:
        if object.type in 'ARMATURE':
          for group in object.pose.bone_groups[:]:

            # search
            if search == '' or re.search(search, group.name):

              # bone group
              BoneGroup(self, context, layout, group, object)

              # attached
              attached[object.name] = True

  # bones
  def bone(self, context, layout, object, option):
    '''
      Bone related code block.
    '''

    # search
    search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

    # active bone
    if object.type in 'ARMATURE':
      if object.mode in {'POSE', 'EDIT'}:

        layout.separator()

        # bones
        if object.mode in 'POSE':
          bone = context.active_bone
        else:
          bone = context.active_bone

        # constraints
        constraints = [constraint.name for constraint in bone.constraints]

        # search
        if search == '' or re.search(search, bone.name) or [re.search(search, item) for item in constraints]:

          # bone
          Bone(self, context, layout, bone, object, option)

          # attached
          attached[object.name] = True

        # bone constraints
        if option.boneConstraints:
          if object.mode in 'POSE':
            bone = context.active_pose_bone
            for constraint in bone.constraints[:]:

              # search
              if search == '' or re.search(search, constraint.name):

                # constraint
                Constraint(self, context, layout, constraint, object, bone, option)

                # attached
                attached[object.name] = True

        # selected bones
        if option.selectedBones:

          # row
          row = layout.row()

          # separator
          row.separator()

          # edit mode
          if object.mode in 'POSE':
            bones = object.data.bones[:]

          # pose mode
          else:
            bones = object.data.edit_bones[:]

          # selected bones
          selectedBones = [
            # [name, object]
          ]

          for bone in bones:

            if bone.select:
              selectedBones.append([bone.name, bone])

          # sort and display
          for bone in sorted(selectedBones):
            if bone[1] != context.active_bone:

              # constraints
              constraints = [constraint.name for constraint in object.pose.bones[bone[1].name].constraints[:]]

              # search
              if search == '' or re.search(search, bone[1].name) or [re.search(search, item) for item in constraints]:

                # bone
                Bone(self, context, layout, bone[1], object, option)

                # attached
                attached[object.name] = True

              # bone constraints
              if option.boneConstraints:
                if object.mode in 'POSE':
                  for constraint in object.pose.bones[bone[1].name].constraints[:]:

                    # search
                    if search == '' or re.search(search, constraint.name):

                      # constraint
                      Constraint(self, context, layout, constraint, object, bone[1], option)

                      # attached
                      attached[object.name] = True

              # row
              row = layout.row()

              # separator
              row.separator()
        else:

          # row
          row = layout.row()

          # separator
          row.separator()

# object
def Object(self, context, layout, datablock, option):
  '''
    The object.
  '''
  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # active object
  if datablock == context.active_object:

    # row
    row = layout.row(align=True)
    row.active = (search == '' or re.search(search, datablock.name) != None)

    # template
    row.template_ID(context.scene.objects, 'active')

  # selected object
  else:

    # row
    row = layout.row(align=True)
    row.active = (search == '' or re.search(search, datablock.name) != None)

    # sub
    sub = row.row(align=True)

    # scale
    sub.scale_x = 1.6

    # make active
    sub.operator('view3d.active_object', text='', icon=icon.object(datablock)).target = datablock.name

    # object
    row.prop(datablock, 'name', text='')

    # options
    if option.options:

      # hide
      row.prop(datablock, 'hide', text='')

      # hide select
      row.prop(datablock, 'hide_select', text='')

      # hide render
      row.prop(datablock, 'hide_render', text='')

# group
def Group(self, context, layout, datablock, object):
  '''
    The object group.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='GROUP')

  # name
  row.prop(datablock, 'name', text='')

# action
def Action(self, context, layout, datablock, object):
  '''
    The object action.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='ACTION')

  # name
  row.prop(datablock, 'name', text='')

# grease pencil
def GreasePencil(self, context, layout, datablock, object, option):
  '''
    The object grease pencil.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # row
  row = layout.row(align=True)
  row.active = (search == '' or re.search(search, datablock.name) != None)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='GREASEPENCIL')

  # name
  row.prop(datablock, 'name', text='')

# pencil layer
def PencilLayer(self, context, layout, datablock, object, option):
  '''
    The object pencil layer.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row(align=True)

  # scale
  sub.scale_x = 0.085

  # fill color
  sub.prop(datablock, 'fill_color', text='')

  # color
  sub.prop(datablock, 'color', text='')

  # info (name)
  row.prop(datablock, 'info', text='')

  # options
  if option.options:

    # lock
    row.prop(datablock, 'lock', text='')

    # hide
    row.prop(datablock, 'hide', text='')

# constraint
def Constraint(self, context, layout, datablock, object, bone, option):
  '''
    The object or pose bone constraint.
  '''

  # enable popup
  try:
    popup = context.user_preferences.addons[addon].preferences['popups']
  except:
    popup = False

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='CONSTRAINT')

  # name
  row.prop(datablock, 'name', text='')

  # options
  if option.options:

    # influence
    if datablock.type not in {'RIGID_BODY_JOINT', 'NULL'}:

      # sub
      sub = row.row(align=True)

      # scale
      sub.scale_x = 0.17

      # influence
      sub.prop(datablock, 'influence', text='')

    # icon view
    if datablock.mute:
      iconView = 'RESTRICT_VIEW_ON'
    else:
      iconView = 'RESTRICT_VIEW_OFF'

    # mute
    row.prop(datablock, 'mute', text='', icon=iconView)

    # popup
    if popup:
      if object.type in 'ARMATURE' and object.mode in 'POSE':
        prop = row.operator('view3d.constraint_settings', text='', icon='COLLAPSEMENU')
        prop.object = object.name
        prop.bone = bone.name
        prop.target = datablock.name
      else:
        prop = row.operator('view3d.constraint_settings', text='', icon='COLLAPSEMENU')
        prop.object = object.name
        prop.bone = ''
        prop.target = datablock.name

# modifier
def Modifier(self, context, layout, datablock, object, option):
  '''
    The object modifier.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # enable popup
  try:
    popup = context.user_preferences.addons[addon].preferences['popups']
  except:
    popup = False

  # row
  row = layout.row(align=True)
  row.active = (search == '' or re.search(search, datablock.name) != None)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon=icon.modifier(datablock))

  # name
  row.prop(datablock, 'name', text='')

  # options
  if option.options:
    if datablock.type not in {'COLLISION', 'SOFT_BODY'}:

      # icon render
      if datablock.show_render:
        iconRender = 'RESTRICT_RENDER_OFF'
      else:
        iconRender = 'RESTRICT_RENDER_ON'

      # show render
      row.prop(datablock, 'show_render', text='', icon=iconRender)

      # icon view
      if datablock.show_viewport:
        iconView = 'RESTRICT_VIEW_OFF'
      else:
        iconView = 'RESTRICT_VIEW_ON'

      # show viewport
      row.prop(datablock, 'show_viewport', text='', icon=iconView)

    # popup
    if popup:
      prop = row.operator('view3d.modifier_settings', text='', icon='COLLAPSEMENU')
      prop.object = object.name
      prop.target = datablock.name

# object data
def ObjectData(self, context, layout, datablock, option):
  '''
    The object data.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # row
  row = layout.row(align=True)
  row.active = (search == '' or re.search(search, datablock.data.name) != None)

  # empty
  if datablock.type in 'EMPTY':

    # empty image draw type
    if datablock.empty_draw_type in 'IMAGE':

      # image
      row.template_ID(datablock, 'data', open='image.open', unlink='image.unlink')

  else:

    # active
    if datablock == context.active_object:

      # name
      row.template_ID(datablock, 'data')

    # selected
    else:

      # name
      row.prop(datablock.data, 'name', text='', icon=icon.objectData(datablock))

# vertex group
def VertexGroup(self, context, layout, datablock, object, option):
  '''
    The object data vertex group.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  # sub.label(text='', icon='GROUP_VERTEX')

  # select vertex group
  prop = sub.operator('object.select_vertex_group', text='', icon='GROUP_VERTEX', emboss=False)
  prop.object = object.name
  prop.target = datablock.name

  # name
  row.prop(datablock, 'name', text='')

  # options
  if option.options:

    # icon lock
    if datablock.lock_weight:
      iconLock = 'LOCKED'
    else:
      iconLock = 'UNLOCKED'

    # lock weight
    row.prop(datablock, 'lock_weight', text='', icon=iconLock)

# shapekey
def Shapekey(self, context, layout, datablock, object, option):
  '''
    The object animation data data shapekey.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='SHAPEKEY_DATA')

  # name
  row.prop(datablock, 'name', text='')

  # options
  if option.options:
    if datablock != object.data.shape_keys.key_blocks[0]:

      # sub
      sub = row.row(align=True)

      # scale
      sub.scale_x = 0.17

      # value
      sub.prop(datablock, 'value', text='')

    # mute
    row.prop(datablock, 'mute', text='', icon='RESTRICT_VIEW_OFF')

# uv
def UV(self, context, layout, datablock, object, option):
  '''
    The object data uv.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='GROUP_UVS')

  # name
  row.prop(datablock, 'name', text='')

  # options
  if option.options:

    # icon active
    if datablock.active_render:
      iconActive = 'RESTRICT_RENDER_OFF'
    else:
      iconActive = 'RESTRICT_RENDER_ON'

    # active render
    row.prop(datablock, 'active_render', text='', icon=iconActive)

# vertex color
def VertexColor(self, context, layout, datablock, object, option):
  '''
    The object data vertex color.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='GROUP_VCOL')

  # name
  row.prop(datablock, 'name', text='')

  # options
  if option.options:

    # icon active
    if datablock.active_render:
      iconActive = 'RESTRICT_RENDER_OFF'
    else:
      iconActive = 'RESTRICT_RENDER_ON'

    # active_render
    row.prop(datablock, 'active_render', text='', icon=iconActive)

# material
def Material(self, context, layout, datablock, object, option):
  '''
    The object material.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # row
  row = layout.row(align=True)
  row.active = (search == '' or re.search(search, datablock.name) != None)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='MATERIAL')

  # name
  row.prop(datablock.material, 'name', text='')

# texture
def Texture(self, context, layout, datablock, object, option):
  '''
    The object material texture.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='TEXTURE')

  # name
  row.prop(datablock.texture, 'name', text='')

  # options
  if option.options:

    # icon toggle
    if datablock.use:
      iconToggle = 'RADIOBUT_ON'
    else:
      iconToggle = 'RADIOBUT_OFF'

    # use
    row.prop(datablock, 'use', text='', icon=iconToggle)

# particle
def Particle(self, context, layout, datablock, object, option):
  '''
    The modifier particle system and settings.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # row
  row = layout.row(align=True)
  row.active = (search == '' or re.search(search, datablock.particle_system.name) != None)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='PARTICLES')

  # name
  row.prop(datablock.particle_system, 'name', text='')

  # search
  if search == '' or re.search(search, datablock.particle_system.settings.name):

    # row
    row = layout.row(align=True)

    # sub
    sub = row.row()

    # scale
    sub.scale_x = 1.6

    # label
    sub.label(text='', icon='DOT')

    # name
    row.prop(datablock.particle_system.settings, 'name', text='')

# bone group
def BoneGroup(self, context, layout, datablock, object):
  '''
    The object data bone group.
  '''

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row()

  # scale
  sub.scale_x = 1.6

  # label
  sub.label(text='', icon='GROUP_BONE')

  # name
  row.prop(datablock, 'name', text='')

# bone
def Bone(self, context, layout, datablock, object, option, bone):
  '''
    The object data bone.
  '''

  # search
  search = context.scene.NamePanel.search if option.regex else re.escape(context.scene.NamePanel.search)

  # row
  row = layout.row(align=True)
  row.active = (search == '' or re.search(search, datablock.name) != None)

  # sub
  sub = row.row(align=True)

  # scale
  sub.scale_x = 1.6

  # active
  if datablock == context.active_bone:

    # selected bones
    sub.prop(option, 'selectedBones', text='', icon='BONE_DATA')

  # selected
  # else:
  #   sub.label(text='', icon='BONE_DATA')

  # pose mode
  if object.mode in 'POSE':

    # name
    if not datablock == context.active_bone:

      # make active bone
      sub.operator('view3d.active_bone', text='', icon='BONE_DATA').target = datablock.name

      row.prop(datablock, 'name', text='')
    else:
      row.prop(datablock, 'name', text='')

    # options
    if option.options:

      # icon view
      if datablock.hide:
        iconView = 'RESTRICT_VIEW_ON'
      else:
        iconView = 'RESTRICT_VIEW_OFF'

      # hide
      row.prop(datablock, 'hide', text='', icon=iconView)

      # icon hide select
      if datablock.hide_select:
        iconSelect = 'RESTRICT_SELECT_ON'
      else:
        iconSelect = 'RESTRICT_SELECT_OFF'

      # hide select
      row.prop(datablock, 'hide_select', text='', icon=iconSelect)

  # edit mode
  else:

    # name
    if not datablock == context.active_bone:

      # make active bone
      sub.operator('view3d.make_active_bone', text='', icon='BONE_DATA').target = datablock.name
    row.prop(datablock, 'name', text='')

    # options
    if option.options:

      # icon view
      if datablock.hide:
        iconView = 'RESTRICT_VIEW_ON'
      else:
        iconView = 'RESTRICT_VIEW_OFF'

      # hide
      row.prop(datablock, 'hide', text='', icon=iconView)

      # icon select
      if datablock.hide_select:
        iconSelect = 'RESTRICT_SELECT_ON'
      else:
        iconSelect = 'RESTRICT_SELECT_OFF'

      # hide select
      row.prop(datablock, 'hide_select', text='', icon=iconSelect)

      # icon lock
      if datablock.lock:
        iconLock = 'LOCKED'
      else:
        iconLock = 'UNLOCKED'

      # lock
      row.prop(datablock, 'lock', text='', icon=iconLock)\
