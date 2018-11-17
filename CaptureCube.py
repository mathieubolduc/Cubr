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
        w = int(height / 4)
        h = w
        x = int(width / 2 - w / 2)
        y = int(height / 2-h/2)
        cv2.rectangle(img_focus, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("box", img_focus)  # image with box

        focus = img[y:y + h, x:x + w]
        #cv2.imshow('webcam', focus)  # focus window

        # try to find when the cube is in optimal position
        edges = cv2.Canny(focus, 50, 100)
        imgray = edges
        # imgray = cv2.cvtColor(focus, cv2.COLOR_RGB2GRAY)
        # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        blurred = cv2.GaussianBlur(imgray, (19, 19), 0)
        # thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        big_cnts = sorted(contours, key=cv2.contourArea, reverse=True)[1:12]  # get 9 biggest contours
        img_contours = np.zeros((focus.shape))
        # Find the index of the largest contour
        img_centers = img_contours.copy()
        for cnt in big_cnts:

            x, y, w, h = cv2.boundingRect(cnt)
            if w/h >.85 and w/h<1.15:
                cv2.rectangle(img_centers, (x, y), (x + w, y + h), (0, 0, 255), 2)
                c_x = int(x + w / 2)
                c_y = int(y + h / 2)
                cv2.circle(img_centers, (c_x, c_y), 2, (255, 0, 0), 2)

        cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)

        #cv2.imshow("contours", img_contours)
        cv2.imshow("squares", img_centers)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
