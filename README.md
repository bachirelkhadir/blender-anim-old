# blender-anim

Install blender, clone Repo
```
git clone https://github.com/bachirelkhadir/blender-anim.git
```

Install python dependencies
```
/Applications/Blender.app/Contents/Resources/2.90/python/bin/python3.7m -m pip install -U tqdm
```



Render hellow world scene to video
```
cd blender-anim

blender --background assets/monkey_sphere.blend --python sample_scenes/hello_world.py -- -lrvp
```

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



  
