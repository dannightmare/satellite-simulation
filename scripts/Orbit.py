from godot import exposed, export
from godot import *
from datetime import datetime, timedelta
import sys, os
import time
from math import sqrt
import heapq as hq

sys.path.append('res://')

from scripts.extractxyz import extractxyz

sys.path.append('./')

from scripts import MyGlobal as MG


def FindMaxRadius(satellite):
	EARTH_RADIUS = 63.71
	# This offsets for light being unable to pass directly next to earth
	# simulating mountains and molehills
	C = 1	# 100 km
	distance = satellite.get_global_translation().length()
	# distance ** 2 = EARTH_RADIUS ** 2 + x ** 2
	x = sqrt(distance**2 - EARTH_RADIUS**2)
	print(x)
	return x - C


@exposed
class Orbit(Spatial):
	
	history_file_path = "historyNS.txt"
	curtime = datetime.now()
	Satellite = ResourceLoader.load('scenes/Satellite.tscn')
	tlefilename = "starlink.tle"
	tlestring = ""
	satellites = {}
	deprecated_sats = []
	special_child = Spatial.new()
	lines_child = Spatial.new()
	iter = 0
	station1name = "Spain"
	station2name = "NewZealand"


	def _ready(self):
		# Settings

		self.Stations = {self.station1name: self.get_node("Earth/" + self.station1name),
						 self.station2name: self.get_node("Earth/" + self.station2name)}
		self.LineColor = Color(0,1,0)

		with open(self.tlefilename, 'r') as file:
			self.tlestring = file.read()
		self.satellites = extractxyz(self.tlestring, self.curtime)
		#print("children count:", self.special_child.get_child_count())
		#print("children:", self.special_child.get_children())
		for sat in list(self.satellites.keys())[:len(self.satellites) // 1]:
			if self.satellites[sat].length() > 67: # 63.71 + 3.3
				self.special_child.add_child(self.spawn_object(self.satellites[sat], sat))
			else:
				self.deprecated_sats.append(sat)

		self.add_child(self.special_child)
		print("children count:", self.special_child.get_child_count())
		Engine.time_scale = 1500	# set relative time of simulation
		
		lowestsat = min(self.special_child.get_children(), key=lambda x : x.get_global_translation().length())
		print('debug: lowestsat height:', lowestsat.get_global_translation().length())
		# Max distance between a ground station and satellites
		self.maxR = FindMaxRadius(lowestsat)
		# Max distance between two satellites
		self.maxD = 2 * self.maxR

		# self.special_child.get_children()
		
		# screenshot test
		#screenshot_name = "user://screenshot_NS" + str(self.iter) + ".png"
		#self.get_viewport().get_texture().get_data().save_png(screenshot_name)


	def _process(self, delta):
		self.iter += 1
		
		self.curtime += timedelta(seconds=delta)
		
		self.satellites = extractxyz(self.tlestring, self.curtime)
		
		#for i, sat in enumerate(self.special_child.get_children()):
		#	sat.set_global_translation(self.satellites[i][1])
		#print("children:", self.special_child.get_children())
		print("children count before:", self.special_child.get_child_count())
		
		delete_sats = []
		for sat in self.satellites:
			if sat in self.deprecated_sats:
				continue
			pos = self.satellites[sat]
			node = self.special_child.get_node(sat)
			if node is None:
				#print("Warning: Node is none with name: ", sat)
				continue
			if pos.length() > 67:
				node.set_global_translation(pos)
			else:
				node.queue_free()
				self.deprecated_sats.append(sat)

		print("children count after:", self.special_child.get_child_count())

		#raise Exception("before graphing")
		print("before graphing")
		start_time = time.perf_counter()
		self.Orbit_graph = dict()
		self.construct_graph()
		end_time = time.perf_counter()
		print("graph constructed: took time: ", end_time - start_time)
		#raise Exception("before astar")
		start_time = time.perf_counter()
		nodenames = self.a_star(self.Orbit_graph, self.station1name, self.station2name, self.distance)
		end_time = time.perf_counter()
		print("a_star finished: took time: ", end_time - start_time)
		
		self.lines_child.queue_free()
		if nodenames is None:
			print("nodenames is None")
			return
		#raise Exception("before drawing")
		# draw path
		self.lines_child = Spatial.new()
		curpos = self.Stations[nodenames[0]].get_global_translation()
		for name in nodenames[1:-1]:
			if name in self.deprecated_sats:
				print(f"{name} was deprecated, but trying to draw a line to it. FAIL")
				break
			nextpos = self.satellites[name]

			print(f'\tdebug: {pos.length()}')
			self.draw_line(curpos, nextpos)
			curpos = nextpos
		
		nextpos = self.Stations[nodenames[-1]].get_global_translation()
		self.draw_line(curpos, nextpos)
		self.add_child(self.lines_child)
		
		#screenshot_name = "user://screenshot_NS" + str(self.iter) + ".png"
		
		#img = self.get_viewport().get_texture().get_data()
		#img.flip_y()
		#img.save_png(screenshot_name)


	def _get_line_material(self):
		mat = SpatialMaterial()
		mat.flags_unshaded = True
		mat.vertex_color_use_as_albedo = True
		return mat


	def draw_line(self, pos1, pos2):
		g = ImmediateGeometry.new()
		g.material_override = self._get_line_material()
		g.begin(Mesh.PRIMITIVE_LINES)
		g.set_color(self.LineColor)
		g.add_vertex(pos1)
		g.add_vertex(pos2)
		g.end()
		self.lines_child.add_child(g)


	def construct_graph(self):
		satellites = self.special_child.get_children()
		for i, satnode in enumerate(satellites):
			start_time = time.perf_counter()
			satname = str(satnode.get_name())
			self.Orbit_graph[satname] = {}
			Sat1Loc = self.satellites[satname]
			for station_name in self.Stations:
				GrStLoc = self.Stations[station_name].get_global_translation()
				distance = (Sat1Loc - GrStLoc).length()
				if distance < self.maxR:
					self.Orbit_graph[satname][station_name] = distance
					if station_name not in self.Orbit_graph:
						self.Orbit_graph[station_name] = {}
					self.Orbit_graph[station_name][satname] = distance
					
			for j in range(i+1, len(satellites)):
				sat2node = satellites[j]
				sat2name = str(sat2node.get_name())
				Sat2Loc = self.satellites[sat2name]
				distance = (Sat1Loc - Sat2Loc).length()
				if distance < self.maxD:
					self.Orbit_graph[satname ][sat2name] = distance
					if sat2name not in self.Orbit_graph:
						self.Orbit_graph[sat2name] = {}
					self.Orbit_graph[sat2name][satname ] = distance
			end_time = time.perf_counter()
			#print(f"graph creation iteration {i} took {start_time - end_time}")


	def spawn_object(self, position, name):
		# Create an instance of the scene
		instance = self.Satellite.instance()

		# Set the position of the instance if it's a spatial or 2D node
		instance.set_global_translation(position)	# For 3D

		instance.set_name(name)

		return instance


	def distance(self, sat1name, sat2name):
		# print(sat1name)
		Sat1Loc = self.satellites.get(sat1name) or self.get_node("Earth/" + sat1name).get_global_translation()
		# print(sat2name)
		Sat2Loc = self.satellites.get(sat2name) or self.get_node("Earth/" + sat2name).get_global_translation()
		return (Sat1Loc - Sat2Loc).length()


	def a_star(self, graph, startname, endname, heuristic):
		"""
		take a graph and pick a start and end position,
		and a heuristic function that accepts two points and returns their heuristic,
		and returns the shortest path between the two points
		"""
		def reconstruct_path(came_from, current):
			total_path = [current]
			while current in came_from:
				current = came_from[current]
				total_path.append(current)
			total_path.reverse()
			return total_path

		open = [(heuristic(startname, endname),
				 startname)]
		came_from = {}
		closed = set()

		g_score = {node: float('inf') for node in graph}
		g_score[startname] = 0
		f_score = {node: float('inf') for node in graph}
		f_score[startname] = heuristic(startname, endname)

		iters = 1
		while open:

			_, cur = hq.heappop(open)
			if cur == endname:
				print(f"Done, iters: {iters}")
				return reconstruct_path(came_from, cur)
			closed = closed | set(cur)
			iters+=1
			for neighbor in graph[cur]:
				if neighbor in closed:
					continue
				d_neighbor = graph[cur][neighbor]
				neighbor_cost = g_score[cur] + d_neighbor
				if neighbor_cost < g_score[neighbor]:
					came_from[neighbor] = cur
					g_score[neighbor] = neighbor_cost
					f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, endname)
					hq.heappush(open, (f_score[neighbor], neighbor))

		print(f"None, iters: {iters}")
		return None
