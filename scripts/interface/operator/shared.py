
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

# sort
def sort(layout, option):

  # separate
  layout.separator()

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row(align=True)

# scale x
  sub.scale_x = 0.2

  # sort
  sub.prop(option, 'sort', toggle=True)

  # sub sub
  subsub = sub.row(align=True)

  # active
  subsub.active = option.sort

  # scale x
  subsub.scale_x = 5

  # type
  subsub.prop(option, 'type', toggle=True, expand=True)

  # sub sub sub
  subsubsub = subsub.row(align=True)

  # active
  subsubsub.active = option.type == 'POSITIONAL'

  # scale x
  subsubsub.scale_x = 0.2

  # axis
  subsubsub.prop(option, 'axis', expand=True)

  # subsub
  subsub = sub.row(align=True)

  # active
  subsub.active = option.sort

  # scale x
  subsub.scale_x = 2.2

  # dummy 9
  subsub.prop(option, 'invert', toggle=True)

# count
def count(layout, option):

  # separate
  layout.separator()

  # row
  row = layout.row(align=True)

  # sub
  sub = row.row(align=True)

  # scale
  sub.scale_x = 0.2

  # sort
  sub.prop(option, 'count', toggle=True)

  # sub
  subsub = sub.row(align=True)

  # active
  subsub.active = option.count

  # icon
  icon = 'LINKED' if option.link else 'UNLINKED'

  # link
  subsub.prop(option, 'link', text='', icon=icon)

  # pad
  subsub.prop(option, 'pad', text='Pad')

  # start
  subsub.prop(option, 'start', text='Start')

  # step
  subsub.prop(option, 'step', text='Step')

  # sub
  subsubsub = subsub.row(align=True)

  # scale
  subsubsub.scale_x = 0.1

  # separate
  subsubsub.prop(option, 'separator', text='')

  # ignore
  subsub.prop(option, 'ignore', text='', icon='ZOOM_PREVIOUS')
