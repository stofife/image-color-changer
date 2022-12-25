from PIL import Image
import numpy as np
from collections import Counter

img = Image.open("exp.png", "r")
pixels = list(img.getdata())
pixels = [pixel[:3] for pixel in pixels]

ld = 46**2

c_counter = Counter(pixels)
c_sorted = c_counter.most_common()
colors = []
cur_top = 0

while len(colors) < 16:
    if colors == []:
        colors.append(c_sorted[cur_top][0])
        cur_top += 1
        continue
    c = c_sorted[cur_top][0]
    dist = []
    for color in colors:
        p1, p2 = np.array(c), np.array(color)
        dist.append(np.sum((p1 - p2)**2, axis=0))
    cur_top += 1
    if not (min(dist) < ld):
        colors.append(c)
        print(f"Suitable color found!\n  RGB: ({c})")

print(colors)

new_pixels = pixels

for i in range(len(pixels)):
    min_dist = False
    p1 = np.array(pixels[i])
    for color in colors:
        p2 = np.array(color)
        dist = np.sum((p1 - p2)**2, axis=0)
        if (not min_dist) or dist < min_dist[0]:
            min_dist = (dist, color)
    new_pixels[i] = min_dist[1]

out_file = Image.new('RGB', (320, 200))
out_file.putdata(new_pixels)
print("New image generated, saving...")
out_file.save('res.png')
