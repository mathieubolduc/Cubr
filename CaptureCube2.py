import cv2
import numpy as np


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        edges = cv2.Canny(img, 50, 100)

        # img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_grey = edges
        blurred = cv2.GaussianBlur(img_grey, (5, 5), 0)
        # thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[1]
        # cv2.drawContours(img, cnts[1], 0, (0, 255, 0))
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)

        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            # M = cv2.moments(c)
            # cX = int(M["m10"] / M["m00"])
            # cY = int(M["m01"] / M["m00"])

            # draw the contour and center of the shape on the image
            cv2.drawContours(img, [c], -1, (0, 255, 0), 2)
            # cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)
            # cv2.putText(img, "center", (cX - 20, cY - 20),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1 * peri, True)
            if peri > 50 and len(approx) == 4:  # Detect only squares/rectangles
                # compute the bounding box of the contour and use the
                # bounding box to compute the aspect ratio
                (x, y, w, h) = cv2.boundingRect(approx)
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3)

            # show the image
            cv2.imshow("Image", img)

        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
