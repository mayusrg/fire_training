# Training YOLOv11 to accurately recognize images of fire and smoke
Train YOLOv11 with images of fire and smoke

## Key terms:
- dataset: a folder of images plus matching label files (the boxes)
- ```yolo11n.pt```: the starter brain everyone trains from; knows general shapes, not fire yet. auto-downloads on first use
- model / brain / "best.pt" : the trained result. stored in ```runs/detect/<name>/weights/```.
- epoch: one full pass over all training images

> This guide uses `device=mps`, which is **Apple Silicon (M1/M2/M3/M4) only**.
> 
> Windows/Linux with an NVIDIA GPU → use ```device=0```. No GPU → use ```device=cpu``` (slower).

## You need:
- to adjust ```device``` as above according to device (Mac vs Windows/linux)
- **Python 3.11+** installed.


# Things to do, in order
1. [Setup](#1-create-a-folder)
2. [Download datasets](#2-download-datasets-training)
3. [Activate environment](#3-activate-your-environment)
4. [Build files](#4-build)
5. [Train](#5-train-the-new-brain)
6. [Run](#6-actually-running-yolo)



# Specific instructions

## 1. Create a folder
Where your downloaded datasets will go. ```yolo11n.pt``` is here.

For this guide, the folder is called ```fire-detect```.

Make the folder:
```
mkdir -p ~/projects/fire-detect
```

Go to the folder:
```
cd ~/projects/fire-detect
```


### Set up the environment (first-timers only)
Create the environment:
```
python3 -m venv .venv
```

Install YOLO:
```
pip install --upgrade pip
pip install ultralytics
```

When the venv is on, your prompt starts with `(.venv)`. Confirm it works:

```
yolo checks
```


## 2. Download datasets: training
Should at least include: data.yaml, test (folder), train (folder), valid (folder)
* I personally renamed every one to fire[number] (ex. fire1, fire2, ... fireN)
* If you do not do this, you must manually list out every folder name when building.

> Once you train a model on your fire/smoke data, the resulting brain (```best.pt```) only knows fire and smoke. Training a seed brain creates a new brain that only recognizes your 2 classes (seen in your ```data.yaml```).


## 3. Activate your environment (every time, before you can do anything)
Go to your folder full of datasets:
```
cd ~/projects/fire-detect
```

Activate:
```
source .venv/bin/activate
```


## 4. Build
Build, train, and rebuild whenever your data changes.


```build_dataset.py``` combines all your dataset folders, shuffles them, and splits them into the ```combined_split/``` folder that training reads.

Save ```build_dataset.py``` into your project folder (same place as ```yolo11n.pt```)

Copy and paste this into your terminal:
```
cat > build_dataset.py << 'EOF'
```

Then paste in the contents of ```build_dataset.py```.

[WHY BUILD_DATASET.PY?](#WHY-BUILD_DATASET.PY?)

> [!WARNING]
> [***PLEASE READ THIS BEFORE YOU BUILD***](#CLASS-NAME-AND-ORDER-MISMATCHES)

Build the dataset, IF YOU ALREADY HAVE ```build_dataset.py``` DOWNLOADED:
```
python build_dataset.py fire1 fire2
```

> If you have a lot of dataset folders named in a specific format:
> ```
> python build_dataset.py fire*
> ```


If you DON'T want to download the file, copy and paste this into your terminal:
```
cat > build_dataset.py << 'EOF'
```

Then paste in the contents of ```build_dataset.py```.


## 5. Train the new brain

```
yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v2
```
- ```epochs=100``` - how many times it studies the full set
- ```patience=20``` - auto-stop if it stops improving for 20 epochs (keeps the best version)
- ```name=fire_v2``` - change this number if you don't want to overwrite your previous brain.
- ```imgsz``` - target image resolution
- [more details regarding brains](#BRAIN-MANAGEMENT)


## 6. ACTUALLY RUNNING YOLO
0. Make sure your environment is activated duh
1. This is the basic yolo detection one (the model is the default seed)
   ```yolo predict model=yolo11n.pt source=0 device=mps show=True```

2. This is the more detailed one:
   ```yolo detect predict model=path/to/brain.pt source=0 device=mps name=wtv_name_you_want show=True ```
> ```model=``` is just a file path. YOLO loads whatever ```.pt``` sits at that path.
> ```name=``` only controls the output folder under ```runs/detect/<name>/```
>
> notice the yolo detect **predict** vs **train**
> source depends on whether you want your built in camera or another connected device

<br><br>

# CLASS NAME AND ORDER MISMATCHES
> [!WARNING]
> ALL DATASETS MUST USE THE SAME CLASSES IN THE SAME ORDER!!!!!!

In the ```data.yaml``` file of any dataset, you will see the following lines:
```
nc: 2
names: ['fire', 'smoke']
```

**THE NAMES MAY DIFFER.**

```nc``` represents the number of classes, equal to the length of ```names```. The .txt files only store class NUMBERS, not words. The position of the words decides the meaning.

Cases you might see + how to fix:

1. ```names: ['0', '1']```: Unhelpful labels; boxes that show up real-time will display '0' or '1'. If 0 really is fire and 1 really is smoke, the POSITIONS match. You can change '0' to 'fire' and '1' to 'smoke'.
   > On Roboflow, you can verify this by opening an image and checking the left-side panel for classes.

2. ```names: ['fire', 'smoke']```: Fine, ideal.
   
3. ```names: ['smoke', 'fire']```: NOT FINE!!! Fix it in Roboflow and re-download (you may have to clone your desired dataset) 
   > If you simply rename it, every label is now wrong.

4. More classes in new datasets.

   **This is fine:**

   DatasetA
   ```
   nc: 2
   names: ['fire', 'smoke']
   ```
   DatasetB
   ```
   nc: 3
   names: ['fire', 'smoke', 'water']
   ```
   
   **This is NOT fine:**
   
   DatasetA
   ```
   nc: 2
   names: ['fire', 'smoke']
   ```
   DatasetB
   ```
   nc: 3
   names: ['fire', 'water', 'smoke']
   ```
   

   > A dataset can have fewer or more classes than your list, but it can never *disagree on the numbering*.

<br><br>

# WHY USE BUILD_DATASET.PY?
Roboflow splits each dataset into folders named train, valid, and test. This works for one dataset, but YOLO cannot be directed towards multiple folders. It would also be tedious and unrealistic for one to manually move the contents of new datasets into one combined folder (see [the complicated file structure](#FILE-STRUCTURE)) AND split it 80/10/10, especially when there are thousands of images and txt files with *very* interesting file names.

```build_dataset.py``` deletes and rebuilds ```combined_split/``` from scratch each run so it's freshly split 80/10/10 each time you add something.

<br><br>

# BRAIN MANAGEMENT
## To find every brain you have at once:
```
find runs -name best.pt
```

## Create a new brain (keeps all old ones)
Change ```name=```. New name -> new folder -> old brains untouched.
```
yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v3
```
This will put the brain in ```runs/detect/fire_v3/weights/best.pt```

## Overwrite an existing brain
1. Reuse the name and force it with `exist_ok=True`:
   
   ```
   yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v2 exist_ok=True
   ```
2. **OR** delete the old folder, and then train normally

<br><br>

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
│       ├── images/   labels/             ← annotations
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

<br><br>

# Datasets used (this is for my own sake this shouldn't matter to whoever's reading lol)
1. https://universe.roboflow.com/peter-malak-j25xh/wildfire-detection-5fgxd
2. https://universe.roboflow.com/waleed-azzi-o5bzp/wildfire-detection-3vcvr
