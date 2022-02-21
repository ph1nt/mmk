from keycode import *

KC____ = KC_TRANSPARENT
KM_ESC = MT(KC_LGUI, KC_ESC)
KM_TILD = MT(KC_LCTRL, KC_NONUS_HASH)
KM_ENTER = MT(KC_LSHIFT, KC_ENTER)
KM_SPACE = MT(KC_LALT, KC_SPACE)
KM_PLUS = S(KC_EQUAL)
KM_UNDR = S(KC_MINUS)
KM_PIPE = S(KC_BSLS)
KM_VUP = KC__VOLUP
KM_VDN = KC__VOLDOWN
UPPER = LT(1, KC_BSPACE)
LOWER = LT(2, KC_TAB)
# fmt: off
KEYS_MAP = (
# defaults
    #KC_1234, KC_1234, KC_1234, KC_1234, KC_1234, KC_1234, KC_1234, KC_1234, KC_1234, KC_1234
    [KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,    KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,
     KC_A,    KC_S,    KC_D,    KC_F,    KC_G,    KC_H,    KC_J,    KC_L,    KC_K,    KC_SCLN,
     KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,    KC_N,    KC_M,    KC_COMMA,KC_DOT,  KC_SLASH,
     KM_TILD, KM_ESC,  LOWER,   KC_NO,   KM_ENTER,KM_SPACE,KC_NO,   UPPER,   KC_MUTE, KC_POWER],
# numbers
    [KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    KC_6,    KC_7,    KC_8,    KC_9,    KC_0,
     KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_LBRC, KC_RBRC, KM_PLUS, KC_MINUS,KC_EQUAL,
     KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,  KC_F13,  KM_UNDR, KM_PIPE,
     KC_NO,   KC____,  KC____,  KC____,  KC____,  KC____,  KC____,  KC____,  KC____,  KC_NO],
# symbols
    [S(KC_1), S(KC_2), S(KC_3), S(KC_4), S(KC_5), S(KC_6), S(KC_7), S(KC_8), S(KC_9), S(KC_0),
     KC_BRIU, KM_VUP,  KC_NO,   KC_NO,   KC_NO,   KC_LEFT, KC_DOWN, KC_UP, KC_RIGHT, KC_QUOT,
     KC_BRID, KM_VDN,  KC_MPRV, KC_MPLY, KC_MNXT, KC_HOME, KC_PGDN, KC_PGUP, KC_END, KC_BSLS,
     KC_NO,   KC____,  KC____,  KC____,  KC____,  KC____,  KC____,  KC____,  KC____,  KC_NO],
)
# fmt: on


def key(layer, index):
    return KEYS_MAP[layer][index]
