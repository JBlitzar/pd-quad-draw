from PIL import Image, ImageDraw
import numpy as np


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
    draw.rectangle([x, y, x + size, y + size], fill=tuple(color))


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
    output_image_path = "output_quadtree.png"
    threshold = 15

    img = Image.open(input_image_path).convert("RGB")
    img_np = np.array(img)
    width, height = img.size
    size = width

    global draw
    output_img = Image.new("RGB", (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(output_img)

    quadtree(img_np, 0, 0, size, threshold)

    output_img = output_img.crop((0, 0, width, height))
    output_img.save(output_image_path)
