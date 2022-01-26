MMK - My Mechanical Keyboard
======================
Hand-wired wireless keyboard, run Python on it. To be more difficult use ESP32.
The Tap-key feature, which is holding a key down to activate an alternate function.
### Using <kbd>D</kbd> for Navigation
Taping <kbd>d</kbd> outputs <kbd>d</kbd> (press & release quickly), holding <kbd>d</kbd> down activates navigation functions.

![](img/d-for-navigation.png)

+ <kbd>d</kbd> + <kbd>h</kbd> as <kbd>←</kbd>
+ <kbd>d</kbd> + <kbd>j</kbd> as <kbd>↓</kbd>
+ <kbd>d</kbd> + <kbd>k</kbd> as <kbd>↑</kbd>
+ <kbd>d</kbd> + <kbd>l</kbd> as <kbd>→</kbd>
+ <kbd>d</kbd> + <kbd>u</kbd> as <kbd>PageUp</kbd>
+ <kbd>d</kbd> + <kbd>m</kbd> as <kbd>PageDown</kbd>

### Using <kbd>;</kbd> as <kbd>Ctrl</kbd>
Use <kbd>;</kbd> as a MODS_TAP key, taping <kbd>;</kbd> outputs <kbd>;</kbd>, holding <kbd>;</kbd> down outputs <kbd>Ctrl</kbd>.

### Using Pair-keys
Simultaneously pressing two keys (interval less than 10ms) activates an alternate function.

## Todo
- [ ] add system keys
- [ ] add mouse keys

## Credits
+ [python keyboard by Yihui Xiong](https://gitee.com/makerdiary/python-keyboard)
+ [MicroPython](https://github.com/micropython/micropython)
+ [CircuitPython](https://github.com/adafruit/circuitpython)
+ [TMK](https://github.com/tmk/tmk_keyboard)
+ [Toward a more useful keyboard](https://github.com/jasonrudolph/keyboard)
