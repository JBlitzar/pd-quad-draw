import time
import usb_cdc  # type: ignore
import usb_hid  # type: ignore
from adafruit_hid.keyboard import Keyboard  # type: ignore
from adafruit_hid.keycode import Keycode  # type: ignore
from adafruit_hid.mouse_abs import Mouse  # type: ignore
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS  # type: ignore

WIDTH = 1728
HEIGHT = 1117


keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

mouse = Mouse(usb_hid.devices)


def mouse_move(x, y):
    scaled_x = int(x * (32767 / WIDTH))
    scaled_y = int(y * (32767 / HEIGHT))
    mouse.move(scaled_x, scaled_y, 0)


def setup():
    keyboard.press(Keycode.GUI, Keycode.SPACE)
    keyboard.release_all()
    time.sleep(0.1)

    layout.write("gimp")
    time.sleep(0.25)

    keyboard.press(Keycode.ENTER)
    keyboard.release_all()
    time.sleep(6.7)

    mouse_move(667, 20)
    time.sleep(0.1)
    mouse.click(1)
    layout.write("script-fu c")
    time.sleep(1)
    keyboard.press(Keycode.DOWN_ARROW)
    keyboard.release_all()
    time.sleep(1)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()

    time.sleep(1.5)

    layout.write(
        """(define img (car (gimp-image-new 512 512 RGB))) (define layer (car (gimp-layer-new img "bg" 512 512 RGB-IMAGE 100 LAYER-MODE-NORMAL))) (gimp-image-insert-layer img layer 0 0) (gimp-context-set-background '(255 255 255)) (gimp-drawable-fill layer FILL-BACKGROUND) (gimp-display-new img) (gimp-displays-flush)"""
    )
    time.sleep(0.1)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()


#


def draw_rect(x, y, size, color):
    layout.write(
        f"""(gimp-image-select-rectangle img CHANNEL-OP-REPLACE {x} {y} {size} {size}) (gimp-context-set-foreground '({color[0]} {color[1]} {color[2]})) (gimp-drawable-edit-fill layer FILL-FOREGROUND) (gimp-selection-none img)"""
    )
    time.sleep(0.05)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()


setup()

with open("img.txt", "r") as f:
    line = f.readline()
    while line:
        x, y, size, color = line.strip().split(";")
        x = int(x)
        y = int(y)
        size = int(size)
        color = tuple(color.split(","))
        color = (int(color[0]), int(color[1]), int(color[2]))
        draw_rect(x, y, size, color)
        line = f.readline()
