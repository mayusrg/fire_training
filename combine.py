cd ~/projects/fire-detect

cat > build_dataset.py << 'EOF'
import os, sys, random, shutil

random.seed(42)
sources = sys.argv[1:]
if not sources:
    print("Usage: python build_dataset.py folder1 folder2 ...")
    sys.exit(1)
#for example, fire1, fire2, fire3...

OUT = "combined_split"
IMG_EXT = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

# 1. collect every image+label pair from all sources
pairs = []
for src in sources:
    found = 0
    for sp in ["train", "valid", "test"]:
        idir = os.path.join(src, sp, "images")
        ldir = os.path.join(src, sp, "labels")
        if not os.path.isdir(idir):
            continue
        for img in os.listdir(idir):
            if not img.lower().endswith(IMG_EXT):
                continue
            stem = os.path.splitext(img)[0]
            lbl = os.path.join(ldir, stem + ".txt")
            if os.path.exists(lbl):
                pairs.append((os.path.join(idir, img), lbl))
                found += 1
    print(f"  {src}: {found} pairs")

if not pairs:
    print("No image+label pairs found. Check folder structure.")
    sys.exit(1)

# 2. shuffle + split 80/10/10
random.shuffle(pairs)
n = len(pairs)
a, b = int(n * 0.8), int(n * 0.9)
split = {"train": pairs[:a], "valid": pairs[a:b], "test": pairs[b:]}

# 3. wipe old output, rebuild fresh (collision-safe: image+label keep same stem)
# always called combined_folder; when training again, still use combined_folder
if os.path.exists(OUT):
    shutil.rmtree(OUT)
for sp, items in split.items():
    idir = f"{OUT}/{sp}/images"; ldir = f"{OUT}/{sp}/labels"
    os.makedirs(idir, exist_ok=True); os.makedirs(ldir, exist_ok=True)
    for ip, lp in items:
        stem, ext = os.path.splitext(os.path.basename(ip))
        final, k = stem, 1
        while os.path.exists(f"{idir}/{final}{ext}"):
            final = f"{stem}_{k}"; k += 1
        shutil.copy(ip, f"{idir}/{final}{ext}")
        shutil.copy(lp, f"{ldir}/{final}.txt")

# 4. write yaml with absolute paths
root = os.path.abspath(OUT)
with open(f"{OUT}/data.yaml", "w") as f:
    f.write(f"train: {root}/train/images\n")
    f.write(f"val: {root}/valid/images\n")
    f.write(f"test: {root}/test/images\n")
    f.write("nc: 2\n")
    f.write("names: ['fire', 'smoke']\n")

print(f"total {n} -> " + str({k: len(v) for k, v in split.items()}))
print(f"yaml: {root}/data.yaml")
EOF
