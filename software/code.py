from adafruit_hid.keyboard import Keyboardfrom adafruit_hid.keycode import Keycodefrom adafruit_hid.consumer_control import ConsumerControlfrom adafruit_hid.consumer_control_code import ConsumerControlCode
import adafruit_ssd1306


#pins
BTN_PREV = board.GP3
BTN_NEXT = board.GP4
BTN_VOL_UP = board.GP5
BTN_VOL_DOWN = board.GP6

BTN_APP1 = board.GP7  # DiscordBTN_APP2 = board.GP8  # SpotifyBTN_APP3 = board.GP9  # ChromeBTN_APP4 = board.GP10 # VS Code
BUTTONS = {
    "mute": BTN_MUTE,
    "prev": BTN_PREV,
    "next": BTN_NEXT,
    "vol_up": BTN_VOL_UP,
    "vol_down": BTN_VOL_DOWN,
    "app1": BTN_APP1,
    "app2": BTN_APP2,
    "app3": BTN_APP3,
    "app4": BTN_APP4,
}

cc = ConsumerControl()

i2c = busio.I2C(board.GP0, board.GP1)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
def make_button(pin):
    b = digitalio.DigitalInOut(pin)
    b.direction = digitalio.Direction.INPUT
    b.pull = digitalio.Pull.UP
    return b

buttons = {name: make_button(pin) for name, pin in BUTTONS.items()}
states = {name: True for name in buttons}
last_press = {name: 0 for name in buttons}
def was_pressed(name):
    btn = buttons[name]
    pressed = not btn.value
    now = time.monotonic() * 1000if pressed and states[name] and (now - last_press[name] > 200):
        last_press[name] = now
        states[name] = Falsereturn Trueelif not pressed and not states[name]:
        states[name] = Truereturn False# ---- Mikrofon stav z NVM ---- try:
    mic_state = bool(microcontroller.nvm[0])except:
    mic_state = Falsedef toggle_mic():
    global mic_state
    try:
        kbd.press(Keycode.CONTROL, Keycode.SHIFT, Keycode.M)
        time.sleep(0.05)
        kbd.release_all()
    except:
        pass    mic_state = not mic_state
    microcontroller.nvm[0] = int(mic_state)


#app opening
    try:
        kbd.press(Keycode.CONTROL, Keycode.ALT, keycode)
        time.sleep(0.05)
        kbd.release_all()
    except:
        pass# ---- Display funkce ---- def update_display(uptime):
    oled.fill(0)
    oled.text("MIC: {}".format("MUTED" if mic_state else "ON"), 0, 0, 1)
    oled.text("UP: {:02}:{:02}:{:02}".format(
        uptime//3600, (uptime//60)%60, uptime%60), 0, 16, 1)
    oled.text("Mute Prev Next", 0, 32, 1)
    oled.text("Vol- Vol+ Apps", 0, 48, 1)
    oled.show()

start_time = time.monotonic()


#main loop
    if was_pressed("mute"): toggle_mic()
    if was_pressed("prev"): cc.send(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
    if was_pressed("next"): cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)
    if was_pressed("vol_up"): cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    if was_pressed("vol_down"): cc.send(ConsumerControlCode.VOLUME_DECREMENT)

    if was_pressed("app1"): launch_app(Keycode.D)  # Discordif was_pressed("app2"): launch_app(Keycode.S)  # Spotifyif was_pressed("app3"): launch_app(Keycode.C)  # Chromeif was_pressed("app4"): launch_app(Keycode.V)  # VS Code
    uptime = int(time.monotonic() - start_time)
    update_display(uptime)
    time.sleep(0.05)