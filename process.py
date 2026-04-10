import os
import sys

try:
    from PIL import Image
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

img_path = r'c:\Users\siyaa\OneDrive\Documents\cicada\CICADA\app\static\images\cclg.jpeg'
out_path = r'c:\Users\siyaa\OneDrive\Documents\cicada\CICADA\app\static\images\cclg_transparent.png'

if not os.path.exists(img_path):
    print("Cannot find:", img_path)
    sys.exit(1)

img = Image.open(img_path).convert('RGBA')
datas = img.getdata()
newData = []
# Make any near-white transparent
# Or, if the background of cclg.jpeg is something else, we can pick the top-left pixel color
bg_col = datas[0]
bg_r, bg_g, bg_b = bg_col[:3]
# threshold
thresh = 30
for item in datas:
    r, g, b = item[:3]
    if abs(r - bg_r) < thresh and abs(g - bg_g) < thresh and abs(b - bg_b) < thresh:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save(out_path, 'PNG')
print("Saved transparent image to", out_path)
