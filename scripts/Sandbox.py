from godot import exposed, export
from godot import *
import os

os.system("pwd")

@exposed
class Sandbox(Spatial):
	def _ready(self):
		"""
		Called every time the node is added to the scene.
		Initialization here.
		"""
		pass
