from godot import exposed, export
from godot import *
import sys

sys.path.append('./')

from scripts import MyGlobal as MG


@exposed
class Earth(Spatial):

	rotation_speed = 360.0 / MG.DAY

	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass

	def _physics_process(self, delta):
		self.rotate_y(self.deg2rad(self.rotation_speed * delta))


	def deg2rad(self, deg):
		return deg * 3.14159265 / 180
