from PIL import Image
import numpy as np
from collections import Counter
from os import system, name

img = Image.open("exp.png", "r")
pixels = list(img.getdata())
pixels = [pixel[:3] for pixel in pixels]

o_ld = 44
ld = o_ld

pixel_slices = [pixels[0 + i * 320 : 320 + i * 320] for i in range(200)]

print(len(pixel_slices))

colors = []

for slice in pixel_slices:
    ld = o_ld
    c_counter = Counter(slice)
    c_sorted = c_counter.most_common()
    slice_colors = []
    cur_top = 0
    while len(slice_colors) < 16:
        if slice_colors == []:
            slice_colors.append(c_sorted[cur_top][0])
            cur_top += 1
            continue
        c = c_sorted[cur_top][0]
        dist = []
        for color in slice_colors:
            p1, p2 = np.array(c), np.array(color)
            dist.append(np.sqrt(np.sum((p1 - p2)**2, axis=0)))
        cur_top += 1
        if not (min(dist) < ld):
            slice_colors.append(c)
        if cur_top == len(c_sorted) and len(slice_colors) < 16:
            cur_top = 0
            ld -= 2

    if name == 'nt': system('cls')
    else: system('clear')
    progress = (int((pixel_slices.index(slice)/200) * 20) * "█") + (20 - int((pixel_slices.index(slice)/200) * 20)) * "."
    print(f"Found suitable colors for slice!\n  {slice_colors}\nProgress: {round((pixel_slices.index(slice)/200) * 100, 2)}% [{progress}]")
    colors.append(slice_colors)

print(colors)

new_pixels = pixel_slices

for i in range(len(pixel_slices)):
    slice = pixel_slices[i]
    slice_colors = colors[i]
    for j in range(len(slice)):
        min_dist = False
        p1 = np.array(slice[j])
        for color in slice_colors:
            p2 = np.array(color)
            dist = np.sqrt(np.sum((p1 - p2)**2, axis=0))
            if (not min_dist) or dist < min_dist[0]:
                min_dist = (dist, color)
        new_pixels[i][j] = min_dist[1]

out_file = Image.new('RGB', (320, 200))
out_file.putdata([pixel for slice in new_pixels for pixel in slice])
print("New image generated, saving...")
out_file.save('res.png')