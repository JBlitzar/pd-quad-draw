# pd-quad-draw

Draw your favorite images as quadtrees in GIMP! Uses the pi pico for keyboard automation.

> _Video is sped up 10x_

https://github.com/user-attachments/assets/fd9713f4-1233-4af2-821a-e803b6bfa806

I thought this would be a fun way to explore the quadtree algorithm and play around with the pico. In the end, it's actually quite elegant. The pseudocode looks something like this:

```python
def quadtree(img, x, y, size, threshold):
    if is_uniform(img, x, y, size, threshold):
        draw_rect(x, y, size, avg_color(img, x, y, size))
    else:
        half = size // 2
        quadtree(img, x, y, half, threshold)                # NW
        quadtree(img, x + half, y, half, threshold)         # NE
        quadtree(img, x, y + half, half, threshold)         # SW
        quadtree(img, x + half, y + half, half, threshold)  # SE
```

Anyone can run the code themselves. (even if you don't have a pico!)

Just clone and `uv run quadtree_demo.py`. You'll see the output image at `output_quadtree.png`. Want to try a different image? Swap image.png for your favorite 512x512 png.

To run on the pico, `uv run gen_quadtree.py` and then run `install.command`. The rest should be handled for you! Note that this is a mac-only script and requires GIMP.

PRs welcome! The quadtree algorithm is a bit fragile at the moment and drawing takes _way_ too long with the pico (~one rectangle per second). I'm thinking about experimenting with pasting rather than typing, but that requires a few more moving parts with communication between the pico and the computer.
