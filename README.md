# Training YOLOv11 to accurately recognize images of fire and smoke
Train yolov11 with images of fire and smoke

## key terms:
- dataset: a folder of images plus matching label files (the boxes)
- ```yolo11n.pt```: the starter brain everyone trains from; knows general shapes, not fire yet. auto-downloads on first use
- model / brain / "best.pt" : the trained result. stored in ```runs/detect/<name>/weights/```.
- epoch: one full pass over all training images.

> This guide uses `device=mps`, which is **Apple Silicon (M1/M2/M3/M4) only**.
> 
> Windows/Linux with an NVIDIA GPU → use ```device=0```. No GPU → use ```device=cpu``` (slower).

## You need:
- adjust ```device``` as above according to device (mac vs windows/linux)
- **Python 3.11+** installed.


# Things to do, in order
1. [Setup](##create-a-folder)
2. [Download datasets](#2-download-datasets-training)
3. Activate environment
4. Build files
5. Train
6. Run



# specific instructions

## 1. create a folder
where your downloaded datasets will go. *yolo11n.pt is here.*

for this guide, the folder is called *fire-detect*.
```
mkdir -p ~/projects/fire-detect
cd ~/projects/fire-detect
```

### set up the environment (first-timers only)
create the environment:
```
python3 -m venv .venv
```
install YOLO
```
pip install --upgrade pip
pip install ultralytics
```

when the venv is on, your prompt starts with `(.venv)`. confirm it works:

```
yolo checks
```

## 2. download datasets: training
should at least include: data.yaml, test (folder), train (folder), valid (folder)
* i personally renamed every one to fire[number] (ex. fire1, fire2, ... fireN)
* if you do not do this, you must manually list out every folder name when building.

> Once you train a model on your fire/smoke data, the resulting brain (```best.pt```) only knows fire and smoke. Training a seed brain creates a new brain that only recognizes your 2 classes (seen in your ```data.yaml```).



## 3. activate your environment (every time, before you can do anything)
go to your folder full of datasets
```
cd ~/projects/fire-detect
```

activate:
```
source .venv/bin/activate
```


## 4. build
build, train, and rebuild whenever your data changes


```build_dataset.py``` combines all your dataset folders, shuffles them, and splits them into the ```combined_split/``` folder that training reads.

Save ```build_dataset.py``` into your project folder (same place as ```yolo11n.pt```)

[WHY BUILD_DATASET.PY?](#WHY-BUILD_DATASET.PY?)

[***PLEASE READ THIS BEFORE YOU BUILD***](#CLASS NAME AND ORDER MISMATCHES)

build the dataset
```
python build_dataset.py fire1 fire2
```

if you have a lot of dataset folders named in a specific format:
```
python build_dataset.py fire*
```


## 5. train the new brain

```
yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v2
```
- ```epochs=100``` - how many times it studies the full set
- ```patience=20``` - auto-stop if it stops imprving for 20 epochs (keeps the best version)
- ```name=fire_v2``` - change this number if you don't want to overwrite your previous brain.
- ```imgsz``` - target image resolution
- [more details regarding brains](#BRAIN-MANAGEMENT)


## 6. ACTUALLY RUNNING YOLO
0. make sure your environment is activated duh
1. This is the basic yolo detection one (the model is the default seed)
   ```yolo predict model=yolo11n.pt source=0 device=mps show=True```

2. This is the more detailed one:
   ```yolo detect predict model=path/to/brain.pt source=0 device=mps name=wtv_name_you_want show=True ```
> ```model=``` is just a file path. YOLO loads whatever ```.pt``` sits at that path.
> ```name=``` only controls the output folder under ```runs/detect/<name>/```
>
> notice the yolo detect **predict** vs **train**
> source depends on whether you want your built in camera or another connected device



# CLASS NAME AND ORDER MISMATCHES



# WHY USE BUILD_DATASET.PY?
roboflow splits each dataset into folders named train, valid, and test. This works for one dataset, but YOLO cannot be directed towards multiple folders. It would also be tedious and unrealistic for one to manually move the contents of new datasets into one combined folder (see [the complicated file structure](#FILE-STRUCTURE)) AND split it 80/10/10, especially when there are thousands of images and txt files with *very* interesting file names.

```build_dataset.py``` deletes and rebuilds ```combined_split/``` from scratch each run so it's freshly split 80/10/10 each time you add something.



# BRAIN MANAGEMENT
## to find every brain you have at once:
```
find runs -name best.pt
```

## create a new brain (keeps all old ones)
change the `name=`. new name -> new folder -> old brains untouched.
```
yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v3
```
this will put the brain in runs/detect/fire_v3/weights/best.pt

## overwrite an existing brain
1. reuse the name and force it with `exist_ok=True`:
   
   ```
   yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v2 exist_ok=True
   ```
2. **OR** delete the old folder, and then train normally



# FILE STRUCTURE
```
~/projects/fire-detect/
├── yolo11n.pt                  ← the STARTER brain (not yours; the seed)
├── build_dataset.py
├── combined_split/             ← your training data
│   ├── data.yaml
│   ├── train/   valid/   test/
├── fire1/                      ← dataset backups
│   ├── data.yaml
│   ├── test/
│       ├── images/   labels/
│   ├── train/
│       ├── images/   labels/
│   ├── valid/
│       ├── images/             
│       └── labels/             ← annotations
├── fire2/
│   └── ...
└── runs/
    └── detect/
        ├── wildfires/          ← a TRAINED brain (your first run)
        │   └── weights/
        │       ├── best.pt     ★ THE BRAIN you use
        │       └── last.pt       (final-epoch version, usually ignore)
        ├── fire_v2/            ← next trained brain (after you run it)
        │   └── weights/
        │       ├── best.pt     ★
        │       └── last.pt
        ├── predict/ … predict-10/   ← detection outputs, NOT brains
        └── ...
```


# Datasets used (this is for my own sake this shouldn't matter to whoever's reading lol)
1. https://universe.roboflow.com/peter-malak-j25xh/wildfire-detection-5fgxd
2. https://universe.roboflow.com/waleed-azzi-o5bzp/wildfire-detection-3vcvr
