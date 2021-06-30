# blender-anim

Install blender, clone Repo
```
git clone https://github.com/bachirelkhadir/blender-anim.git
```

Install python dependencies
```
/Applications/Blender.app/Contents/Resources/2.90/python/bin/python3.7m -m pip install -U tqdm pyaml
```


or in Linux:

```
/snap/blender/161/2.93/python/bin/python3.9 -m ensurepip
/snap/blender/161/2.93/python/bin/python3.9  -m pip install -U tqdm pyaml plotly pandas
```
make sure local site-packages is in path

```
/home/bachir/.local/lib/python3.9/site-packages
```


*Make* sure cleansvg is installed.

# RUN

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



  
