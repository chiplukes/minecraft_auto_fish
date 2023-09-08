import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui
import time


##### Bobber Color Mask, uncomment one of the mask groups below
# This can change depeding on fishing location, texture packs, etc.
# If you need to figure out a new mask you can take a screenshot of the bobber and then use hsv_thresh.py to figure out the HSV thresholds.
# the hsv colorspace works well for filtering a specific color in a large range of brightness.
# however, red exists on both ends of the hue spectrum, so 2 different masks are needed.
# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv

# Tested on Java + Optifine
hue_lhs_lower_red = np.array([0,100,100])
hue_lhs_upper_red = np.array([5,255,255])
hue_rhs_lower_red = np.array([165,100,100])
hue_rhs_upper_red = np.array([180,255,255])

# # TODO: Tested on Java
# hue_lhs_lower_red = np.array([0,100,100])
# hue_lhs_upper_red = np.array([5,255,255])
# hue_rhs_lower_red = np.array([165,100,100])
# hue_rhs_upper_red = np.array([180,255,255])

# # TODO: Tested on Bedrock
# hue_lhs_lower_red = np.array([0,100,100])
# hue_lhs_upper_red = np.array([5,255,255])
# hue_rhs_lower_red = np.array([165,100,100])
# hue_rhs_upper_red = np.array([180,255,255])


# Establish coordinates for a window around area where bobber will be
input(f"Move mouse pointer to upper left coordinate of a window where bobber is expected, then press enter>")
bobber_ul_x, bobber_ul_y = pyautogui.position() # Get the XY position of the mouse.
input(f"Move mouse pointer to lower right coordinate of a window where bobber is expected, then press enter>")
bobber_lr_x, bobber_lr_y = pyautogui.position() # Get the XY position of the mouse.
input(f"Move mouse where you want to cast (crosshairs if you have already cast) then press enter>")
bobber_x, bobber_y = pyautogui.position() # Get the XY position of the mouse.

# Establish location for bobber view window
input(f"Move mouse pointer to upper left coordinate where you would like the bobber view window located (somewhere next to the minecraft window), then press enter button>")
window_x, window_y = pyautogui.position() # Get the XY position of the mouse.
bobwin = "Bobber window"
cv2.namedWindow(bobwin)        # Create a named window
cv2.moveWindow(bobwin, window_x,window_y)
window_w = bobber_lr_x - bobber_ul_x
window_h = bobber_lr_y - bobber_ul_y
monitor = {'top': bobber_ul_y, 'left': bobber_ul_x, 'width': window_w, 'height': window_h}

print(f"You have ten seconds to get your fishing set up.  After auto fishing starts, you can cancel fishing pressing escape key and then moving mouse pointer onto bobber view window")
time.sleep(10)

sct = mss()
bobber_down_cnt = 0
check_rod_exists = False
while 1:

    # move mouse to where bobber window is to stop program running (since errant clicking is bad!)
    mouse_x, mouse_y = pyautogui.position() # Get the XY position of the mouse.
    if mouse_x >= window_x:
        print("stopping fishing, since mouse moved to bobber window.")
        break

    # capture rectangle around bobber
    img = Image.frombytes('RGB', (window_w,window_h), sct.grab(monitor).rgb)
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # apply color mask
    mask_hue_lhs = cv2.inRange(img_hsv, hue_lhs_lower_red, hue_lhs_upper_red)
    mask_hue_rhs = cv2.inRange(img_hsv, hue_rhs_lower_red, hue_rhs_upper_red)
    mask = mask_hue_lhs + mask_hue_rhs # join masks
    result = cv2.bitwise_and(img_hsv, img_hsv, mask = mask)
    img_filt = result # this shoule only have red part of the bobber shown and nothing else

    # when bobber goes under most/all of red goes away
    sum_pix = img_filt.sum()
    print(img_filt.sum())

    if sum_pix < 50 :
        bobber_down_cnt +=1
        if bobber_down_cnt > 3 and not check_rod_exists:
            bobber_down_cnt = 0
            #bobber went under, so right click mouse
            pyautogui.rightClick()
            time.sleep(1.5)  # if you cast again too fast, the bobber can hit the item flying back
            pyautogui.moveTo(bobber_x, bobber_y)      # Move the mouse to the dBuv Y box
            pyautogui.rightClick() # cast
            time.sleep(1)  # wait a second for bobber to get back on surface
            check_rod_exists = True # make sure rod still exists
        elif check_rod_exists:
            if bobber_down_cnt > 100:
                print("stopping fishing, since no red bobber can be found.")
                break
    else:
        bobber_down_cnt = 0
        check_rod_exists = False

    # display bobber view
    filt_bgr = cv2.cvtColor(img_filt, cv2.COLOR_HSV2BGR)
    cv2.imshow(bobwin, filt_bgr)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break