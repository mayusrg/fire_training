# Training YOLOv11 to accurately recognize images of fire and smoke
train yolov11 with images of fire and smoke

# things to do, in order
1. create a folder (example here is fire-detect)
2. download your datasets
3. activate environment
4. train 

# specific instructutions

## create a folder
where your downloaded datasets will go. _yolo11n.pt is here._

## activate your environment
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
* i personally renamed every one to fire[number] (ex. fire1, fire2, ... fire_n_ )

build the dataset
```
python build_dataset.py fire1 fire2
```


# Datasets used
1. https://universe.roboflow.com/peter-malak-j25xh/wildfire-detection-5fgxd
2. https://universe.roboflow.com/waleed-azzi-o5bzp/wildfire-detection-3vcvr
