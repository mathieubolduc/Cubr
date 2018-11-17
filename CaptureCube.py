import cv2
import numpy as np

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        height, width, channels = img.shape

        img_focus = img.copy()
        w = int(height/2)
        h = w
        x = int(width/2-w/2)
        y= int(height/4)
        cv2.rectangle(img_focus, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("box", img_focus)


        focus = img[y:y+h, x:x+w]
        cv2.imshow('webcam', focus)

        # try to find when the cube is in optimal position

        imgray = cv2.cvtColor(focus, cv2.COLOR_RGB2GRAY)
        #ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
        # thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the index of the largest contour
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img_contours = np.zeros((focus.shape))
        cv2.drawContours(img_contours, contours,-1, (0,255,0),3 )

        cv2.imshow("contours",img_contours)


        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()