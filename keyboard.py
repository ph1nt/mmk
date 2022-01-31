import analogio
import microcontroller
from matrix import Matrix
from keycode import *

# Pins for ESP32
Matrix.ROWS = (microcontroller.pin.GPIO19, microcontroller.pin.GPIO23,
               microcontroller.pin.GPIO18, microcontroller.pin.GPIO5)
Matrix.COLS = (microcontroller.pin.GPIO25, microcontroller.pin.GPIO26,
               microcontroller.pin.GPIO27, microcontroller.pin.GPIO14,
               microcontroller.pin.GPIO12, microcontroller.pin.GPIO13,
               microcontroller.pin.GPIO15, microcontroller.pin.GPIO2,
               microcontroller.pin.GPIO0, microcontroller.pin.GPIO4)
Matrix.ROW2COL = False

# fmt: off
COORDS = (
    0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13,
    27,26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14,
    28,29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,     40,
    52,51, 50, 49, 48, 47, 46, 45, 44, 43, 42,         41,
    53,  54, 55,             56,           57, 58, 59, 60
)

KEY_NAME =  (
    'ESC', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'BACKSPACE',
    'TAB', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '|',
    'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '"', 'ENTER',
    'LSHIFT', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'RSHIFT',
    'LCTRL', 'LGUI', 'LALT', 'SPACE', 'RALT', 'MENU', 'FN', 'RCTRL'
)

KEYS_MAP = [
    [KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P,
     KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, KC_SCLN,
     KC_Z, KC_X, KC_C, KC_V, KC_B, KC_N, KC_M, KC_COMMA, KC_DOT, KC_SLASH,
     KC_ESC, KC_TAB, KC_ENTER, KC_SPACE, TO(2, KC_BSPACE)],
    [KC_1, ],
    [KC_EXLM, S(2)],
]
# fmt: on


def key_name(key):
    return KEY_NAME[COORDS[key]]
