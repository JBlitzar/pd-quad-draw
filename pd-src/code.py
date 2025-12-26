import time
import usb_cdc  # type: ignore
import usb_hid  # type: ignore
from adafruit_hid.keyboard import Keyboard  # type: ignore
from adafruit_hid.keycode import Keycode  # type: ignore
from adafruit_hid.mouse_abs import Mouse  # type: ignore
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS  # type: ignore
import board  # type: ignore
import digitalio  # type: ignore


BUTTON_PIN = board.GP11
button = digitalio.DigitalInOut(BUTTON_PIN)
button.switch_to_input(pull=digitalio.Pull.UP)


WIDTH = 1728
HEIGHT = 1117


keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

mouse = Mouse(usb_hid.devices)


CHAR_TO_KEYCODE = {
    "r": Keycode.R,
    "f": Keycode.F,
    "(": Keycode.NINE,
    ")": Keycode.ZERO,
    "0": Keycode.ZERO,
    "1": Keycode.ONE,
    "2": Keycode.TWO,
    "3": Keycode.THREE,
    "4": Keycode.FOUR,
    "5": Keycode.FIVE,
    "6": Keycode.SIX,
    "7": Keycode.SEVEN,
    "8": Keycode.EIGHT,
    "9": Keycode.NINE,
    " ": Keycode.SPACE,
}
SHIFT_CHARS = set("()")


def fast_type(string: str):
    prev = []
    for c in string:
        if c in SHIFT_CHARS:
            keyboard.press(Keycode.LEFT_SHIFT)
        keyboard.press(CHAR_TO_KEYCODE[c])
        prev.append(c)
        if c in SHIFT_CHARS or c in prev:
            keyboard.release_all()
            prev = []
    keyboard.release_all()


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
        """(define img (car (gimp-image-new 1024 1024 RGB))) (define layer (car (gimp-layer-new img "bg" 1024 1024 RGB-IMAGE 100 LAYER-MODE-NORMAL))) (gimp-image-insert-layer img layer 0 0) (gimp-context-set-background '(255 255 255)) (gimp-drawable-fill layer FILL-BACKGROUND) (gimp-display-new img) (gimp-displays-flush)"""
    )
    time.sleep(0.1)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()

    layout.write(
        """(define (rf x y s r g b) (gimp-image-select-rectangle img CHANNEL-OP-REPLACE x y s s) (gimp-context-set-foreground (list r g b)) (gimp-drawable-edit-fill layer FILL-FOREGROUND) (gimp-selection-none img))"""
    )
    time.sleep(0.1)
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()


# Called several thousand times!
# much too slow atm
def draw_rect(x, y, size, color):
    fast_type(f"(rf {x} {y} {size} {color[0]} {color[1]} {color[2]})")
    keyboard.press(Keycode.ENTER)
    keyboard.release_all()
    time.sleep(0.01)


while True:
    if not button.value:  # Button pressed
        break
    time.sleep(0.05)
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
