import cv2
import numpy as np


def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)

    delay_max = 20
    delay_cntr = 0

    x_mean_save = []
    y_mean_save = []

    cube_in_view = False
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        height, width, channels = img.shape

        img_focus = img.copy()
        w = int(height / 4)
        h = w
        x_focus = int(width / 2 - w / 2)
        y_focus = int(height / 2-h/2)
        cv2.rectangle(img_focus, (x_focus, y_focus), (x_focus + w, y_focus + h), (0, 255, 0), 2)


        focus = img[y_focus:y_focus + h, x_focus:x_focus + w]
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

        centers = []
        for cnt in big_cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if w/h >.85 and w/h<1.15:
                cv2.rectangle(img_centers, (x, y), (x + w, y + h), (0, 0, 255), 2)
                c_x = int(x + w / 2)
                c_y = int(y + h / 2)
                cv2.circle(img_centers, (c_x, c_y), 2, (255, 0, 0), 2)
                centers.append((c_x, c_y))
        #cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)
        #cv2.imshow("contours", img_contours)
        if len(centers)==9: # 9 centers
            x_points = [x for x,y in centers]
            y_points = [y for x,y in centers]

            x_points.sort()
            y_points.sort()
            stdx = []
            stdy = []
            for i in range(3):
                stdx.append( np.std(x_points[i*3:(i+1)*3]))
                stdy.append(np.std(y_points[i*3:(i+1)*3]))

            tol = 5
            if np.max(stdx)<tol and np.max(stdy)<tol: # we see a cube
                mean_x = []
                mean_y = []

                for i in range(3): #get grid center points
                    mean_x.append(np.mean(x_points[i * 3:(i + 1) * 3]))
                    mean_y.append(np.mean(y_points[i * 3:(i + 1) * 3]))

                for x in mean_x: #draw center points
                    for y in mean_y:
                        cv2.circle(img_focus, (int(x+x_focus), int(y+y_focus)), 2, (0, 0, 255), 2)
                        x_mean_save=mean_x
                        y_mean_save=mean_y
                        delay_cntr = 0
                if cube_in_view==False:
                    cube_in_view=True
                    print("I see a cube!")

        elif delay_cntr<delay_max and len(x_mean_save)>0 and len(y_mean_save)>0: # draw the circles if were still in delay
            for x in mean_x:
                for y in mean_y:
                    cv2.circle(img_focus, (int(x + x_focus), int(y + y_focus)), 2, (0, 0, 255), 2)
            delay_cntr+=1

        elif delay_cntr>=delay_max and cube_in_view==True: #cube just left view
            cube_in_view=False
            print("Cube is gone")

        cv2.imshow("box", img_focus)  # image with box
        cv2.imshow("squares", img_centers)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
