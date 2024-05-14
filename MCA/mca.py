
# coding: utf-8

'''
Mobile Cellular Automata - 

A Pythonista app for exploring CAs written in GLSL.

'''
import console
import ui
import dialogs
import time
import random
from scene import *

form_param = {
	'p1': {
		'type': 'number',
		'key': 'p1',
		'value': '0.5',
		'title': 'p1: ',
	},
	'p2': {	
		'type': 'number',
		'key': 'p2',
		'value': '0.993',
		'title': 'p2: ',
	},
	'o_weight': {
		'type': 'number',
		'key': 'o_weight',
		'value': '1.0',
		'title': 'Origin Cell: ',
	},	
	'a_weight': {
		'type': 'number',
		'key': 'a_weight',
		'value': '1.0',
		'title': 'Adjacent Cells: ',
	},	
	'c_weight': {
		'type': 'number',
		'key': 'c_weight',
		'value': '1.0',
		'title': 'Corner Cells: ',
	},
}



w, h = ui.get_screen_size()

class ShaderScene (Scene):
	def setup(self):
		
		print('loading shader')
		with open('glsl/cca_p2m9b.fsh') as f:
			src = f.read()
			shader = Shader(src)
			
		print('setting shader')
		self.shader = shader # for convenience
		
			
		# Shader param defaults
		self.params = {
			'p1': 0.5,
			'p2': 0.993,
			'o_weight': 1.0,
			'a_weight': 1.0,
			'c_weight': 1.0,
		}
		
		self.set_shader_params()
			
		self.sprite = SpriteNode(
			'img/init.png', 
			size=self.size, 
			position=self.size/2, 
			parent=self)
		self.sprite.shader = shader
		

	# overridden methods	
			
	def draw(self):
		self.sprite.texture = self.sprite.render_to_texture()

	def touch_began(self, touch):
		self.change_shader_params()
		#self.set_params_from_touch(touch)

	def touch_moved(self, touch):
		pass
		#self.set_params_from_touch(touch)
				
#	def update(self):
#		if random.random() > 0.993:
#			r=random.random()
		
	def did_change_size(self):
		self.sprite.position = self.size/2
		self.sprite.size = self.size
		
		
	# Utility methods
	@ui.in_background
	def change_params_dialog(self):
		for k, v in self.params.items():
			form_param[k].update(value=str(v))
			
		form_sections = [
		('Basic Params', 
			[
				form_param['p1'], 
				form_param['p2']
			], 
			'''These are the basic parameters for the continuous cellular automaton.'''),
		('Cell Weights', 
			[
				form_param['o_weight'],
				form_param['a_weight'],
				form_param['c_weight'],		
			], 
			'''These are the weights for cells in the Moore neighborhood.'''),			
		]		
		self.view.paused = True
		new_params = dialogs.form_dialog(
			'Parameters', 
			sections=form_sections)
	
		if new_params is None:
			return
			
		for k,v in new_params.items():
			self.params[k] = float(v)
		
		self.set_shader_params()
		
		self.view.paused=False	
		#return new_params
			
			
	
	def set_params_from_touch(self, touch):
		r1 = float(touch.location.x) / w
		r2 = float(touch.location.y) / h
		p1 = 0.5 + (r1 * 0.5)
		p2 = 0.8 + (r2 * 0.2)
		print(f'params: {p1}, {p2}')
		self.sprite.shader.set_uniform('p1', p1)
		self.sprite.shader.set_uniform('p2', p2)
		
	def change_shader_params(self):
		self.change_params_dialog()

	def set_shader_params(self):
		for k, v in self.params.items():
			self.shader.set_uniform(k,v)
		print(self.params)



def main():

	console.clear()
	print('Running (main) ...')
	run(
		ShaderScene(),
		frame_interval=1, 
		show_fps=True)
		


if __name__ == '__main__':
	main()
