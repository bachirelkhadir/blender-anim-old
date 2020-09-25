# blender-anim

Clone Repo
``git clone https://github.com/bachirelkhadir/blender-anim.git``


Render hellow world scene to video
``cd blender-anim``

``blender --background assets/monkey_sphere.blend --python sample_scenes/hello_world.py -- -lrvp``

# Command line arguments

```
blender-anim

optional arguments:
  -h, --help  show this help message and exit
  -H          High quality
  -l          Low quality
  -p          Play video at the end
  -b          Open blender file
  -r          Render pngs
  -v          Write png frames to video with ffmpeg
```
