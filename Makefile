BLENDER= "blender"


hello:
	${BLENDER} --background assets/hello_world.blend --python sample_scenes/hello_world.py -- -r -n 0,10
