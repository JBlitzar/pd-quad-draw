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


def draw_rect(x, y, size, color):
    with open("pd-src/img.txt", "a") as f:
        c = ",".join([str(i) for i in color.tolist()])
        f.write(f"{x};{y};{size};{c}\n")


def quadtree(img, x, y, size, threshold):
    if is_uniform(img, x, y, size, threshold) or size == 1:
        draw_rect(x, y, size, average_color(img, x, y, size))
    else:
        half = size // 2
        quadtree(img, x, y, half, threshold)  # NW
        quadtree(img, x + half, y, half, threshold)  # NE
        quadtree(img, x, y + half, half, threshold)  # SW
        quadtree(img, x + half, y + half, half, threshold)  # SE


if __name__ == "__main__":
    input_image_path = "image.png"
    threshold = 15

    with open("pd-src/img.txt", "w+") as f:
        f.write("")

    img = Image.open(input_image_path).convert("RGB")
    img_np = np.array(img)
    width, height = img.size
    size = width

    quadtree(img_np, 0, 0, size, threshold)
