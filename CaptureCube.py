import cv2
import numpy as np
import time
from grid_detection import detect_grid, make_grid
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from Cube import *
import Display



def show_webcam(mirror=False):
    choice = input("Scan real cube? (y/n)\n")
    if choice != "y":
        cube = getScrambledCube()
        Display.plotCube(cube)
        return cube
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    # cam.set(cv2.CAP_PROP_EXPOSURE,0.01)

    delay_max = 25
    delay_cntr = 0
    face_cntr = 0
    messages = [
        "Front Face Captured",
        "Top Face Captured",
        "Bottom Face Captured",
        "Left Face",
        "Right Face",
        "Back Face Captured"
    ]

    faces_order = ['front', 'top', 'bottom', 'left', 'right', 'back']

    face_data_dict = {
        'front':[],
        'top':[],
        'bottom': [],
        'left': [],
        'right': [],
        'back':[]

    }

    face_data_array = []
    x_mean_save = []
    y_mean_save = []

    cube_in_view = False
    image_save = []
    capture_images = True
    new_center_dots = None
    previous_dots = []

    cube_detection_delay=0
    cube_detection_delay_max = 10

    """
    The instructions for cube orientation are printed here.
    This applies to a standard cube.
    """

    print("Position the cube so that the red face is towards the camera and the white face is down")
    print("tldr: Red Forward, White Down/Yellow Up")

    while capture_images:
        ret_val, img = cam.read()

        if mirror:
            img = cv2.flip(img, 1)

        height, width, channels = img.shape

        img_focus = img.copy()
        w = int(height / 4)
        h = w
        x_focus = int(width / 2 - w / 2)
        y_focus = int(height / 2 - h / 2)
        cv2.rectangle(img_focus, (x_focus, y_focus),
                      (x_focus + w, y_focus + h), (0, 255, 0), 2)

        focus = img[y_focus: y_focus + h, x_focus:x_focus + w]
        # cv2.imshow('webcam', focus)  # focus window

        # try to find when the cube is in optimal position
        edges = cv2.Canny(focus, 50, 100)
        imgray = edges
        # imgray = cv2.cvtColor(focus, cv2.COLOR_RGB2GRAY)
        # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        blurred = cv2.GaussianBlur(imgray, (19, 19), 0)
        # thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        im2, contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        big_cnts = sorted(contours, key=cv2.contourArea, reverse=True)[1: 12]  # get 9 biggest contours
        img_contours = np.zeros((focus.shape))
        # Find the index of the largest contour
        img_centers = img_contours.copy()

        centers = []
        for cnt in big_cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if w / h > .85 and w / h < 1.15:
                cv2.rectangle(img_centers, (x, y),
                              (x + w, y + h), (0, 0, 255), 2)
                c_x = int(x + w / 2)
                c_y = int(y + h / 2)
                cv2.circle(img_centers, (c_x, c_y), 2, (255, 0, 0), 2)
                centers.append((c_x, c_y))
        # cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3)
        # cv2.imshow("contours", img_contours)

        # Grid detection Jerome
        # length, std_dev, angle1, angle2, center_point=detect_grid(centers)
        # if len(centers) > 5 and std_dev < 10 and length > 15:  # we have a face
        #     delay_cntr=0
        #     new_center_dots=make_grid(
        #         length, angle1, angle2, center_point)
        #     # assert len(new_center_dots)==9
        #     for cd in new_center_dots:
        #         cv2.circle(
        #             img_focus, (x_focus+int(round(cd[0])), y_focus+int(round(cd[1]))), 2, (255, 255, 255), 2)
        #
        #     previous_dots.append(new_center_dots)
        #     if len(previous_dots) == 10 and not cube_in_view:
        #         center_dots = np.mean(previous_dots, axis=0)
        #         colour_names = get_colours_pointwise(img, center_dots, x_focus, y_focus)
        #         print("I see a cube!")
        #         print(colour_names)
        #         cube_in_view= True
        #
        # elif delay_cntr < delay_max and new_center_dots is not None: # draw the circles if were still in delay
        #     for cd in new_center_dots:
        #         cv2.circle(
        #             img_focus, (x_focus + int(round(cd[0])), y_focus + int(round(cd[1]))), 2, (255, 255, 255), 2)
        #     delay_cntr += 1
        #
        # elif delay_cntr >= delay_max and cube_in_view==True: #cube just left view
        #     cube_in_view=False
        #     previous_dots= []
        #     print("Cube is gone")

        # Peters Grid detection
        if len(centers) == 9:  # 9 centers
            x_points = [x for x, y in centers]
            y_points = [y for x, y in centers]
            x_points.sort()
            y_points.sort()
            stdx = []
            stdy = []
            for i in range(3):
                stdx.append(np.std(x_points[i * 3:(i + 1) * 3]))
                stdy.append(np.std(y_points[i * 3:(i + 1) * 3]))
            tol = 4
            if np.max(stdx) < tol and np.max(stdy) < tol:  # we see a cube
                mean_x = []
                mean_y = []

                for i in range(3):  # get grid center points
                    mean_x.append(int(np.mean(x_points[i * 3:(i + 1) * 3])))
                    mean_y.append(int(np.mean(y_points[i * 3:(i + 1) * 3])))

                for x in mean_x:  # draw center points
                    for y in mean_y:
                        cv2.circle(img_focus, (int(x + x_focus), int(y + y_focus)), 2, (0, 0, 255), 2)
                        x_mean_save = mean_x
                        y_mean_save = mean_y
                        delay_cntr = 0
                if cube_in_view == False:
                    if cube_detection_delay<cube_detection_delay_max: # give a buffer time for cube detection
                        cube_detection_delay+=1
                        continue
                    cube_in_view = True
                    print("I see a cube!")
                    # save data at pixel points
                    image_save = focus

                    """
                    Get the colours here 
                    """
                    names = get_colours(image_save, x_mean_save, y_mean_save)
                    print(names)
                    good = 'a'
                    while not(good == 'y' or good == 'n'):
                        good = input("Colours good? y/n \n")
                    if good == 'n':
                        # redo image
                        print("Redoing image")
                        continue

                    face_data_array.append(names)
                    face_cntr+=1
                    if face_cntr==6:
                        print("All faces captured!")
                        break;
                    else:
                        print(f"show me the {faces_order[face_cntr]} next!")

        elif delay_cntr < delay_max and len(x_mean_save) > 0 and len(
                y_mean_save) > 0:  # draw the circles if were still in delay
            for x in mean_x:
                for y in mean_y:
                    cv2.circle(img_focus, (x + x_focus, y + y_focus), 2, (0, 0, 255), 2)
            delay_cntr += 1

        elif delay_cntr >= delay_max and cube_in_view == True:  # cube just left view
            cube_in_view = False
            cube_detection_delay = 0
            print("Cube is gone")
            print()

        cv2.imshow("box", img_focus)  # image with box
        cv2.imshow("squares", img_centers)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    #cv2.destroyAllWindows()

    #convert my faces to Mathieu's faces
    faces_mathieu_notation = []

    for colour_names in face_data_array:
        correct_names = []
        for name in colour_names:
            correct_name = ''
            if name=='Yellow':
                correct_name = CubeColor.YELLOW
            elif name=='Red':
                correct_name = CubeColor.RED
            elif name=='Blue':
                correct_name = CubeColor.BLUE
            elif name == 'White':
                correct_name = CubeColor.WHITE
            elif name=='Green':
                correct_name = CubeColor.GREEN
            elif name ==  'Orange':
                correct_name = CubeColor.ORANGE
            else:
                print("invalid name passed to look up")
            correct_names.append(correct_name)
        correct_names = np.asarray(correct_names).reshape(3, 3)
        #print(correct_names)
        faces_mathieu_notation.append(correct_names)

    cube = Cube()

    for face in faces_mathieu_notation:
        side = face[1][1]
        cube.setSide(side, face)

    Display.plotCube(cube)
    return cube


    # print("Press any key to exit...")
    # cv2.waitKey(0)


def get_colours_pointwise(image, points, x_offset, y_offset):
    boundaries = [  # Colours in BRG
        [75, 150, 101],  # YELLOW
        [72, 45, 155],  # RED
        [125, 51, 15],  # BLUE
        [140, 127, 110],  # WHITE
        [67, 96, 11],  # GREEN
        [70, 70, 170]  # ORANGE
    ]
    # boundaries = [
    #     [50 * 180/360, 63 * 255/100, 71 * 255/100],  # YELLOW
    #     [8 * 180/360, 63 * 255/100, 49 * 255/100],  # RED
    #     [222 * 180/360, 41 * 255/100, 48 * 255/100],  # BLUE
    #     [29 * 180/360, 14 * 255/100, 68 * 255/100],  # WHITE
    #     [87 * 180/360, 43 * 255/100, 45 * 255/100],  # GREEN
    #     [18 * 180/360, 71 * 255/100, 76 * 255/100]  # ORANGE
    # ]
    cv2.imwrite("test_vector.png", image)
    colours_list = ['Yellow', 'Red', 'Blue', 'White', 'Green', 'Orange']
    colours = np.zeros((3, 3), dtype='uint8')

    # convert RGB to better norm taking space
    image = cv2.cvtColor(image, cv2.COLOR_RGB2Lab)
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.imshow(image)
    # plt.show()
    boundaries_cvt = cv2.cvtColor(np.expand_dims(np.array(boundaries, dtype='uint8'), 1), cv2.COLOR_BGR2LAB)
    boundaries_cvt = np.squeeze(boundaries_cvt, 1)
    # boundaries_cvt = boundaries
    colour_names = []

    for j, (x, y) in enumerate(points):
        colour_ind = 0  # default
        x = int(round(x)) + x_offset
        y = int(round(y)) + y_offset
        best_dist = np.inf
        pixels_ave = np.mean(image[x - 1:x + 1, y - 1:y + 1], axis=(0, 1))
        # pixels_ave = image[x, y]
        for i, bound in enumerate(boundaries_cvt):
            dist = np.linalg.norm(bound[:2] - pixels_ave[:2])
            if dist < best_dist:
                best_dist = dist
                colour_ind = i
        colour_names.append(colours_list[colour_ind])
        # colour_names.append((pixels_ave[0] * 2, pixels_ave[1] * 100/255, pixels_ave[2] * 100/255))
        # colour_names.append((pixels_ave[0], pixels_ave[1], pixels_ave[2]))

    return colour_names


def get_colours(image, x_mean, y_mean):
    # colour boundarues
    boundaries = [  # BGR
        ([85, 95, 95], [255, 255, 255]),  # WHITE
        ([35, 130, 100], [95, 174, 150]),  # YELLOW
        ([86, 31, 4], [220, 88, 50]),  # BLUE
        ([40, 60, 5], [110, 150, 56]),  # GREEN
        ([35, 35, 125], [120, 120, 200]),  # ORANGE
        ([60, 30, 85], [120, 75, 140])  # RED
    ]

    # boundaries = [  # RGB
    #     ([100, 100, 30], [150, 174, 95]),  # YELLOW
    #     ([90, 30, 60], [140, 60, 85]),  # RED
    #     ([4, 31, 86], [50, 88, 220]),  # BLUE
    #     ([103, 103, 103], [255, 255, 255]),  # WHITE
    #     ([5, 70, 40], [56, 150, 110]),  # GREEN
    #     ([120, 40, 40], [200, 120, 120])  # ORANGE
    # ]

    colours_list = ['White', 'Yellow', 'Blue', 'Green', 'Orange', 'Red']
    colours = np.zeros((3, 3), dtype='uint8')

    cv2.imwrite("test.png", image)

    for i, bounds in enumerate(boundaries):  # build masks, then check the values at points
        _image = image.copy()  # might not have to do this
        lower = np.array(bounds[0], dtype='uint8')
        upper = np.array(bounds[1], dtype='uint8')
        mask = cv2.inRange(_image, lower, upper)
        # print(colours_list[i])
        # plt.imshow(mask)
        # plt.show()
        for j, x in enumerate(x_mean):
            for k, y in enumerate(y_mean):
                if np.mean(mask[x - 1:x + 1, y - 1:y + 1]) > 150:
                    colours[j, k] = i  # set the colour index in the array

    colours_names = [colours_list[i] for i in colours.flatten()]

    return colours_names


def get_colours_vector(image, x_mean, y_mean):
    boundaries = [  # Colours in BRG
        [101, 150, 75],  # YELLOW
        [115, 45, 72],  # RED
        [15, 51, 125],  # BLUE
        [110, 127, 140],  # WHITE
        [11, 96, 67],  # GREEN
        [170, 70, 70]  # ORANGE
    ]
    cv2.imwrite("test_vector.png", image)
    colours_list = ['Red', 'Blue', 'Yellow', 'White', 'Green', 'Orange']
    colours = np.zeros((3, 3), dtype='uint8')

    # convert RGB to better norm taking space
    _image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    boundaries_cvt = cv2.cvtColor(np.expand_dims(np.array(boundaries, dtype='uint8'), 1), cv2.COLOR_RGB2Lab)
    boundaries_cvt = np.squeeze(boundaries_cvt, 1)
    plt.imshow(_image)
    plt.show()
    print(boundaries_cvt[0])
    for j, x in enumerate(x_mean):
        for k, y in enumerate(y_mean):
            best_dist = np.inf
            colour_ind = 4 # default to green, we miss it often
            for i, bound in enumerate(boundaries_cvt):
                pixels_ave = np.mean(image[x - 1:x + 1, y - 1:y + 1])
                dist = np.linalg.norm(bound - pixels_ave)
                if dist < best_dist:
                    best_dist = dist
                    colour_ind = i

            colours[j, k] = colour_ind

    colour_names = [colours_list[i] for i in colours.flatten()]

    return colour_names


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
