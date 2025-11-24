# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
#     "pillow",
# ]
# ///
import numpy as np
from PIL import Image


def average_color(img, x, y, size):
    region = img[y : y + size, x : x + size]
    mean_color = np.mean(region, axis=(0, 1))

    return mean_color.astype(int)


def is_uniform(img, x, y, size, threshold):
    region = img[y : y + size, x : x + size]
    mean_color = np.mean(region, axis=(0, 1))
    diff = np.abs(region - mean_color)
    return np.all(diff <= threshold)


def quadtree(img, x, y, size, threshold, min_size=1):
    if is_uniform(img, x, y, size, threshold) or size <= min_size:
        return [(x, y, size, average_color(img, x, y, size))]
    else:
        half = size // 2
        rects = []
        rects.extend(quadtree(img, x, y, half, threshold, min_size))  # NW
        rects.extend(quadtree(img, x + half, y, half, threshold, min_size))  # NE
        rects.extend(quadtree(img, x, y + half, half, threshold, min_size))  # SW
        rects.extend(quadtree(img, x + half, y + half, half, threshold, min_size))  # SE
        return rects


if __name__ == "__main__":
    input_image_path = "image.png"

    with open("pd-src/img.txt", "w+") as f:
        f.write("")

    img = Image.open(input_image_path).convert("RGB")
    img_np = np.array(img)
    width, height = img.size
    img_size = width

    for threshold in range(40, 30, -10):
        draw = quadtree(img_np, 0, 0, img_size, threshold, min_size=16)
        draw = sorted(draw, key=lambda item: item[2], reverse=True)
        with open("pd-src/img.txt", "a") as f:
            for x, y, s, color in draw:
                f.write(f"{x};{y};{s};{color[0]},{color[1]},{color[2]}\n")
        print(f"Threshold {threshold} done, {len(draw)} rects")
        # print(draw)
        # print(img_size, width, height, threshold)
