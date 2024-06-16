from godot import exposed, export
from godot import *


@exposed
class CubeTest(Spatial):


	def _ready(self):
		g = ImmediateGeometry.new()
		g.material_override = self._get_line_material()
		g.begin(Mesh.PRIMITIVE_LINES)
		color = Color(73/255.0,85/255.0,33/255.0)
		g.set_color(color)
		#g.add_vertex(Vector3(1,0,0))
		g.add_vertex(Vector3(-3,-3,-3))
		g.add_vertex(Vector3(2,2,0))
		print(color)
		
		g.end()
		self.add_child(g)


	def _get_line_material(self):
		mat = SpatialMaterial()
		mat.flags_unshaded = True
		mat.vertex_color_use_as_albedo = True
		return mat


	def draw_line(self, pos1, pos2):
		g = ImmediateGeometry.new()
		g.material_override = self._get_line_material()
		g.begin(Mesh.PRIMITIVE_LINES)
		g.set_color(Color(73,85,33))
		g.add_vertex(pos1)
		g.add_vertex(pos2)
		g.end()
		self.lines_child.add_child(g)
