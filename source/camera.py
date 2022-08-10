import cv2
import numpy as np

lower_bound = [110, 110, 110]
higher_bound = [200, 200, 200]
curve_array = []
avg_size = 5
points = [[62, 150], [480 - 62, 150], [0, 189], [480 - 0, 189]]

def thresholding(img):
    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    lower_white = np.array(lower_bound)
    upper_white = np.array(higher_bound)
    mask_white = cv2.inRange(img_lab, lower_white, upper_white)
    return mask_white

def warp_image(img, w, h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warp = cv2.warpPerspective(img, matrix, (w, h))
    return img_warp

def get_histogram(img, min_per=0.1):
    histogram_val = np.sum(img, axis=0)
    max_val = np.max(histogram_val)
    min_val = min_per * max_val

    index_array = np.where(histogram_val >= min_val)
    center_point = np.average(index_array)
    return center_point,img


def detect_lane(frame):
    img = thresholding(frame)
    h, w, c = frame.shape

    warp_img = warp_image(img, w, h)
    curve_point,warp_img = get_histogram(warp_img, min_per=0.9)
    curve_rate = curve_point  - h

    # draw the camera image
    cv2.imshow("img",img)
    cv2.imshow("warp",warp_img) # warped image

    # smoothening the curve rate
    curve_array.append(curve_rate)
    if len(curve_array) >= avg_size:
        curve_array.pop(0)

    curve = int(sum(curve_array)/len(curve_array))
    return curve