# ### BEGIN GPL LICENSE BLOCK ###
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ### END GPL LICENSE BLOCK ###

import bpy
from bpy.types import Operator

bl_info = {
	"name": "UV Map Order",
	"author": "Jake Dube, cdeguise, bovesan, APEC, iaian7",
	"version": (1, 2),
	"blender": (2, 80, 0),
	"location": "Properties > Data > UV Maps panel (with mesh selected)",
	"description": "Rearrange and sort uv map order",
	"doc_url": "https://github.com/iaian7/BlenderUVMapOrder",
	"tracker_url": "https://github.com/iaian7/BlenderUVMapOrder/issues",
	"category": "UV"
}

# Original sources: https://blender.stackexchange.com/questions/67266/changing-order-of-uv-maps/

##################################################
# General functions

def make_active(name):
	uvs = bpy.context.view_layer.objects.active.data.uv_layers
	for uv in uvs:
		if uv.name == name:
			uvs.active = uv
			return
	print("Could not find:", name, "\n(this should never happen)")

def move_to_bottom(index):
	uvs = bpy.context.view_layer.objects.active.data.uv_layers
	uvs.active_index = index
	new_name = uvs.active.name
	
	bpy.ops.mesh.uv_texture_add()
	
	# delete the "old" one
	make_active(new_name)
	bpy.ops.mesh.uv_texture_remove()
	
	# set the name of the last one
	uvs.active_index = len(uvs) - 1
	uvs.active.name = new_name

##################################################
# Move up/down
	
class MESH_OT_uv_up(Operator):
	bl_idname = "mesh.uv_texture_up"
	bl_label = "Move Up"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		uvs = bpy.context.view_layer.objects.active.data.uv_layers
		
		# End early if the layer is already at the top
		if uvs.active_index == 0:
			return {'FINISHED'}
		
		original = uvs.active.name
		uvs.active_index -= 1
		bpy.ops.mesh.uv_texture_down()
		make_active(original)
		
		return {'FINISHED'}

class MESH_OT_uv_down(Operator):
	bl_idname = "mesh.uv_texture_down"
	bl_label = "Move Down"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		uvs = context.view_layer.objects.active.data.uv_layers
		
		# get the selected UV map
		orig_ind = uvs.active_index
		orig_name = uvs.active.name
		
		# End early if the layer is already at the bottom
		if orig_ind == len(uvs) - 1:
			return {'FINISHED'}
		
		# use "trick" on the one after it
		move_to_bottom(orig_ind + 1)
		
		# use the "trick" on the UV map
		move_to_bottom(orig_ind)
		
		# use the "trick" on the rest that are after where it was
		for i in range(orig_ind, len(uvs) - 2):
			move_to_bottom(orig_ind)
			
		make_active(orig_name)
		
		return {'FINISHED'}

##################################################
# Move to top/bottom

class MESH_OT_uv_top(Operator):
	bl_idname = "mesh.uv_texture_top"
	bl_label = "Move to Top"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		uvs = context.view_layer.objects.active.data.uv_layers
		
		# get the selected UV map
		orig_ind = uvs.active_index
		orig_name = uvs.active.name
		
		# End early if the layer is already at the top
		if orig_ind == 0:
			return {'FINISHED'}
		
		# use the "trick" on the UV map (this ensures we can then process all the previous ones)
		move_to_bottom(orig_ind)
		
		# use the "trick" on the rest of the maps
		for i in range(len(uvs) - 1):
			move_to_bottom(0)
		
		make_active(orig_name)
		
		return {'FINISHED'}

class MESH_OT_uv_bottom(Operator):
	bl_idname = "mesh.uv_texture_bottom"
	bl_label = "Move to Bottom"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		uvs = context.view_layer.objects.active.data.uv_layers
		
		# get the selected UV map
		orig_ind = uvs.active_index
		orig_name = uvs.active.name
		
		# End early if the layer is already at the bottom
		if orig_ind == len(uvs) - 1:
			return {'FINISHED'}
		
		# use the "trick" on the UV map
		move_to_bottom(orig_ind)
		
		make_active(orig_name)
		
		return {'FINISHED'}
	

##################################################
# Sort ascending/descending

class MESH_OT_uv_a_to_z (Operator):
	bl_idname = 'mesh.uv_texture_a_to_z'
	bl_label = 'Sort A to Z'
	bl_description = "Sorting UVs by name (A to Z)"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):        
		uvs = context.view_layer.objects.active.data.uv_layers
		orig_name = uvs.active.name
		
		for j in range (len(uvs)):
			for i in range (len(uvs)-1):
				uvs.active_index = i
				temp_name = uvs.active.name
				uvs.active_index = i+1
				if uvs.active.name < temp_name:
					bpy.ops.mesh.uv_texture_up()
					
		make_active(orig_name)
		
		return {"FINISHED"}

class MESH_OT_uv_z_to_a (Operator):
	bl_idname = 'mesh.uv_texture_z_to_a'
	bl_label = 'Sort Z to A'
	bl_description = "Sorting UVs by name (Z to A)"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		uvs = context.view_layer.objects.active.data.uv_layers
		orig_name = uvs.active.name
		
		for j in range (len(uvs)):
			for i in range (len(uvs)-1):
				uvs.active_index = i+1
				temp_name = uvs.active.name
				uvs.active_index = i
				if uvs.active.name < temp_name:
					bpy.ops.mesh.uv_texture_down()
					
		make_active(orig_name)
		
		return {"FINISHED"}

##################################################
# UI layout

def uv_tools_addition(self, context):
	layout = self.layout
	row = layout.row()
	
	col1 = row.column(align=True)
	col1.operator("mesh.uv_texture_up", icon='TRIA_UP')
	col1.operator("mesh.uv_texture_down", icon='TRIA_DOWN')
	
	layout.separator()
	
	col2 = row.column(align=True)
	col2.operator("mesh.uv_texture_top", icon='TRIA_UP_BAR')
	col2.operator("mesh.uv_texture_bottom", icon='TRIA_DOWN_BAR')
	
	layout.separator()
	
	col2 = row.column(align=True)
	col2.operator("mesh.uv_texture_a_to_z", icon='TRIA_RIGHT') # SORTALPHA SORT_ASC TRIA_RIGHT
	col2.operator("mesh.uv_texture_z_to_a", icon='TRIA_LEFT') # SORTALPHA SORT_DESC TRIA_LEFT

##################################################
# Plugin install/uninstall

classes = (MESH_OT_uv_down, MESH_OT_uv_up, MESH_OT_uv_top, MESH_OT_uv_bottom, MESH_OT_uv_a_to_z, MESH_OT_uv_z_to_a)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.DATA_PT_uv_texture.append(uv_tools_addition)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	bpy.types.DATA_PT_uv_texture.remove(uv_tools_addition)

if __name__ == "__main__":
	register()
	