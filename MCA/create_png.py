import ui
import random

def save_png(png, filename):
	try:
		with open(filename, "wb") as file:
			file.write(png)
		print(f"PNG saved to {filename}")
	except Exception as e:
		print(f"Error saving PNG to {filename}: {e}") 

s = 6
fw, fh = ui.get_screen_size()
w = int(fw)
h = int(fh)
ws = w//s 
hs = h//s 

print(f'''    width: {fw} => {w}
    height: {fh} => {h}
    grid square size: {s}
    w//s: {ws} ({fw/s})
    h//s: {hs} ({fh/s})
    
''')

with ui.ImageContext(w, h) as ctx:
	#Set random pixels to black or white
	for x in range(ws):
		for y in range(hs):
			color = (
				random.random(), 
				random.random(),
				random.random(),
				1.0
			)
		#	color = (0.0,0.0,0.0,1.0)
		#	if x > 20 and x < 60 and y>20 and y<60:
		#		color=(
		#			1.0,
		#			0.0,
		#			0.0,
		#			1.0)
			
			#if random.random() < 0.5:
			#	color = (0.0, 0.0, 0.0, 1.0)
			#else:
			#	color = (1.0, 1.0, 1.0,1.0) 
			
			ui.set_color(color)
			ui.fill_rect(x*s, y*s, s, s)
		
		# Get the image from the context
		image = ctx.get_image()
	
# Save the image as a PNG file
png = image.to_png()
save_png(png, 'img/init.png')
