from godot import exposed, export
from godot import *
import sys

sys.path.append('./')

from scripts import MyGlobal as MG

@exposed
class Satellite(StaticBody):

	# member variables here, example:
	a = export(int)
	b = export(str, default='foo')
	
	rotation_speed = 360.0 / (MG.TIME)

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass # TODO: spawn satellites

	def _physics_process(self, delta2):
		self.rotate_y(-self.deg2rad(float(self.rotation_speed)))

	def deg2rad(self, deg):
		return deg * 3.14159265 / 180
