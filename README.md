# Training YOLOv11 to accurately recognize images of fire and smoke
train yolov11 with images of fire and smoke

## key terms:
- dataset: a folder of images plus matching label files (the boxes)
- yolo11n.pt: the starter brain everyone trains from; knows general shapes, not fire yet. auto-downloads on first use
- model / brain / "best.pt" : the trained result. stored in 'runs/detect/<name>/weights/.
- epoch: one full pass over all training images.

> This guide uses `device=mps`, which is **Apple Silicon (M1/M2/M3/M4) only**.
> Windows/Linux with an NVIDIA GPU → use `device=0`. No GPU → use `device=cpu` (slow).

## you need:
- A Mac with Apple Silicon (this guide), or adjust `device` as above.
- **Python 3.11+** installed.


# things to do, in order
1. create a folder
2. download your datasets
3. activate environment
4. train



# specific instructions

## create a folder
where your downloaded datasets will go. *yolo11n.pt is here.*

for this guide, the folder is called *fire-detect*.
```bash
mkdir -p ~/projects/fire-detect
cd ~/projects/fire-detect
```

## set up the environment (first-timers only)
create the environment:
```bash
python3 -m venv .venv
```
install YOLO
```
pip install --upgrade pip
pip install ultralytics
```

When the venv is on, your prompt starts with `(.venv)`. Confirm it works:

```bash
yolo checks
```


## activate your environment (every time, before you can do anything)
go to your folder full of datasets
```
cd ~/projects/fire-detect
```

activate:
```
source .venv/bin/activate
```

## download datasets
should at least include: data.yaml, test (folder), train (folder), valid (folder)
* i personally renamed every one to fire[number] (ex. fire1, fire2, ... fireN)
* if you do not do this, you must manually list out every folder name when building.

build the dataset
```
python build_dataset.py fire1 fire2
```

if you have a lot of dataset folders named in a specific format:
```
python build_dataset.py fire*
```

## train the new brain


```
yolo detect train model=yolo11n.pt data=combined_split/data.yaml epochs=100 imgsz=640 patience=20 device=mps name=fire_v2
```

# Datasets used
1. https://universe.roboflow.com/peter-malak-j25xh/wildfire-detection-5fgxd
2. https://universe.roboflow.com/waleed-azzi-o5bzp/wildfire-detection-3vcvr
