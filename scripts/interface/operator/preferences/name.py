
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# imports
import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from ....function import options
from ....function.preferences import name as nameD

# addon
addon = bpy.context.user_preferences.addons.get(__name__.partition('.')[0])

# name
class name(Operator):
  '''
    Name Panel.
  '''
  bl_idname = 'wm.name_panel_defaults'
  bl_label = 'Name Panel Defaults'
  bl_description = 'Name panel defaults.'
  bl_options = {'INTERNAL'}

  # check
  def check(self, context):
    return True

  # draw
  def draw(self, context):
    '''
      Operator body.
    '''

    # layout
    layout = self.layout

    # panel
    panel = context.scene.NamePanel

    # column
    column = layout.column(align=True)

    # row
    row = column.row(align=True)

    # scale
    row.scale_y = 1.25

    # icon toggle
    iconToggle = 'RADIOBUT_ON' if panel.filters else 'RADIOBUT_OFF'

    # filters
    row.prop(panel, 'filters', text='Filters', icon=iconToggle, toggle=True)

    # display names
    row.prop(panel, 'displayNames', text='', icon='ZOOM_SELECTED')

    # options
    row.prop(panel, 'options', text='', icon='SETTINGS')

    # # operator menu
    row.menu('VIEW3D_MT_name_panel_specials', text='', icon='COLLAPSEMENU')

    # filters
    if panel.filters:

      # separate
      column.separator()

      # row
      row = column.row(align=True)

      # scale
      row.scale_x = 5 # hack: forces buttons to line up correctly

      # action
      row.prop(panel, 'action', text='', icon='ACTION')

      # grease pencil
      row.prop(panel, 'greasePencil', text='', icon='GREASEPENCIL')

      # groups
      row.prop(panel, 'groups', text='', icon='GROUP')

      # constraints
      row.prop(panel, 'constraints', text='', icon='CONSTRAINT')

      # modifiers
      row.prop(panel, 'modifiers', text='', icon='MODIFIER')

      # bone groups
      row.prop(panel, 'boneGroups', text='', icon='GROUP_BONE')

      # bone constraints
      row.prop(panel, 'boneConstraints', text='', icon='CONSTRAINT_BONE')

      # row
      row = column.row(align=True)

      # scale
      row.scale_x = 5 # hack: forces buttons to line up correctly

      # vertex groups
      row.prop(panel, 'vertexGroups', text='', icon='GROUP_VERTEX')

      # shapekeys
      row.prop(panel, 'shapekeys', text='', icon='SHAPEKEY_DATA')

      # uvs
      row.prop(panel, 'uvs', text='', icon='GROUP_UVS')

      # vertex colors
      row.prop(panel, 'vertexColors', text='', icon='GROUP_VCOL')

      # materials
      row.prop(panel, 'materials', text='', icon='MATERIAL')

      # textures
      row.prop(panel, 'textures', text='', icon='TEXTURE')

      # particles systems
      row.prop(panel, 'particleSystems', text='', icon='PARTICLES')

      # hide find & replace
      if panel.hideFindReplace:

        # separate
        column.separator()

        # row
        row = column.row(align=True)

        # find
        row.prop(panel, 'search', text='', icon='VIEWZOOM')

        # sub
        sub = row.split(align=True)

        # scale x
        sub.scale_x = 0.1

        # regex
        sub.prop(panel, 'regex', text='.*', toggle=True)

        # row
        row = column.row(align=True)

        # replace
        row.prop(context.scene.BatchName, 'replace', text='', icon='FILE_REFRESH')

        # sub
        sub = row.split(align=True)

        # scale x
        sub.scale_x = 0.15

        # batch name
        op = sub.operator('wm.batch_name', text='OK')
        op.simple = True
        op.quickBatch = True

        # batch name
        op = row.operator('wm.batch_name', text='', icon='SORTALPHA')
        op.simple = False
        op.quickBatch = True

    # hide find & replace
    if not panel.hideFindReplace:

      # separate
      column.separator()

      # row
      row = column.row(align=True)

      # find
      row.prop(panel, 'search', text='', icon='VIEWZOOM')

      # sub
      sub = row.split(align=True)

      # scale x
      sub.scale_x = 0.1

      # regex
      sub.prop(panel, 'regex', text='.*', toggle=True)

      # row
      row = column.row(align=True)

      # replace
      row.prop(context.scene.BatchName, 'replace', text='', icon='FILE_REFRESH')

      # sub
      sub = row.split(align=True)

      # scale x
      sub.scale_x = 0.15

      # batch name
      op = sub.operator('wm.batch_name', text='OK')
      op.simple = True
      op.quickBatch = True

      # batch name
      op = row.operator('wm.batch_name', text='', icon='SORTALPHA')
      op.simple = False
      op.quickBatch = True

    # enabled
    if panel.displayNames:

      # separate
      column.separator()

      # row
      row = column.row()

      # mode
      row.prop(panel, 'mode', expand=True)

    # separate
    column.separator()

    # row
    row = column.row()

    # display bones
    row.prop(panel, 'displayBones', icon='BONE_DATA')

    # display bones
    if panel.displayBones:

      # separate
      column.separator()

      # row
      row = column.row()

      # bone mode
      row.prop(panel, 'boneMode', expand=True)

  # execute
  def execute(self, context):
    '''
      Execute the operator.
    '''

    # main
    nameD.main(context)

    # transfer options
    options.transfer(context, True, False, False, False, False)
    return {'FINISHED'}

  # invoke
  def invoke(self, context, event):
    '''
      Invoke the operator panel/menu, control its width.
    '''

    # size
    try: size = 200 if addon.preferences['largePopups'] == 0 else 400
    except: size = 200

    context.window_manager.invoke_props_dialog(self, width=size)
    return {'RUNNING_MODAL'}
