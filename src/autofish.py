import numpy as np
import cv2
from mss import mss
from PIL import Image
import pyautogui
import time

#https://www.kdnuggets.com/2022/08/perform-motion-detection-python.html
#https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv

input(f"hover mouse where you want bobber window located, then press enter button>")
window_x, window_y = pyautogui.position() # Get the XY position of the mouse.
print(window_x, window_y)
bobwin = "Bobber window"
cv2.namedWindow(bobwin)        # Create a named window
cv2.moveWindow(bobwin, window_x,window_y)
w, h = 256, 1024

input(f"hover mouse where you want to cast then press enter>")
bobber_x, bobber_y = pyautogui.position() # Get the XY position of the mouse.
print(bobber_x, bobber_y)

print(f"You have ten seconds to get your fishing set up.")
time.sleep(10)

sct = mss()
#prev_frame =None
bobber_down_cnt = 0
check_rod_exists = False
while 1:

    # move mouse to where bobber window is to stop program running (since errant clicking is bad!)
    mouse_x, mouse_y = pyautogui.position() # Get the XY position of the mouse.
    if mouse_x >= window_x:
        print("stopping fishing, since mouse moved to bobber window.")
        break

    monitor = {'top': bobber_y-h//2, 'left': bobber_x-w//2, 'width': w, 'height': h}
    img = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)
    #img_np = np.asarray(img)
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # use hsv_thresh.py to figure out thresholds
    # lower red mask (0-10)
    lower_red = np.array([0,100,100])
    upper_red = np.array([5,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)
    # upper red mask (170-180)
    lower_red = np.array([165,100,100])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)
    mask = mask0 + mask1 # join masks

    result = cv2.bitwise_and(img_hsv, img_hsv, mask = mask)
    img_filt = result

    # when bobber goes under
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
                print("stopping fishing, since pole is likely broken")
                break
    else:
        bobber_down_cnt = 0
        check_rod_exists = False

    # # Defining 'motion' variable equal to zero as initial frame
    # var_motion = 0
    # gray_image = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # # To find the changes creating a GaussianBlur from the gray scale image
    # #gray_frame = cv2.GaussianBlur(gray_image, (21, 21), 0)

    # # For the first iteration checking the condition
    # # we will assign grayFrame to initalState if is none
    # if prev_frame is None:
    #    #initialState = gray_frame
    #    prev_frame = gray_image

    # # Calculation of difference between static or initial and gray frame we created
    # #differ_frame = cv2.absdiff(initialState, gray_frame)
    # differ_frame = cv2.absdiff(prev_frame, gray_image)

    # # the change between static or initial background and current gray frame are highlighted
    # thresh_frame = cv2.threshold(differ_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    # # For the moving object in the frame finding the coutours
    # cont,_ = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for cur in cont:
    #     if cv2.contourArea(cur) < 10000:
    #         continue
    #     var_motion = 1
    #     (cur_x, cur_y,cur_w, cur_h) = cv2.boundingRect(cur)

    #     # To create a rectangle of green color around the moving object
    #     cv2.rectangle(img_np, (cur_x, cur_y), (cur_x + cur_w, cur_y + cur_h), (0, 255, 0), 3)

    # #from the frame adding the motion status
    # motionTrackList.append(var_motion)
    # motionTrackList = motionTrackList[-2:]
    # # Adding the Start time of the motion
    # if motionTrackList[-1] == 1 and motionTrackList[-2] == 0:
    #     motionTime.append(datetime.now())

    # # Adding the End time of the motion
    # if motionTrackList[-1] == 0 and motionTrackList[-2] == 1:
    #     motionTime.append(datetime.now())


    # # In the gray scale displaying the captured image
    # #cv2.imshow("The image captured in the Gray Frame is shown below: ", gray_frame)
    # cv2.imshow("The image captured in the Gray Frame is shown below: ", gray_image)

    # # To display the difference between inital static frame and the current frame
    # cv2.imshow("Difference between the  inital static frame and the current frame: ", differ_frame)

    # # To display on the frame screen the black and white images from the video
    # cv2.imshow("Threshold Frame created from the PC or Laptop Webcam is: ", thresh_frame)

    # Through the colour frame displaying the contour of the object
    filt_bgr = cv2.cvtColor(img_filt, cv2.COLOR_HSV2BGR)
    #cv2.imshow("original", img_bgr)
    #cv2.imshow("hsv", img_hsv)
    #cv2.imshow("img filt hsv", img_hsv)
    #cv2.imshow("img filt bgr", filt_bgr)
    cv2.imshow(bobwin, filt_bgr)

    #cv2.imshow('test', cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    #prev_frame = gray_image

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
