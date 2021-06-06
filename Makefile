BLENDER= "/Applications/Blender.app/Contents/MacOS/Blender" # "blender"

all:
	${BLENDER} --background assets/polytope.blend --python sample_scenes/polytope.py -- -lrvp


logo:
	${BLENDER} --background assets/polytope.blend --python sample_scenes/logo.py -- -lrvp
