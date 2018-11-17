from typing import Tuple, List
import math
import numpy as np


def detect_grid(center_points: List[Tuple[float, float]]):
    if len(center_points) < 4:
        return None, None, None, None, None

    # 1. Get vectors of the closest points (that are also not too close)
    total_vectors = []
    for i in range(len(center_points)):
        p1 = center_points[i]

        p2s = list(
            map(lambda p2: (p2[0] - p1[0], p2[1] - p1[1]), center_points))
        vectors = sorted(p2s, key=lambda v: math.hypot(
            v[0], v[1]) if math.hypot(v[0], v[1]) > 8 else np.inf)[:4]

        # 2.a get the angle spanned by the vectors
        angle_diffs = []
        for j in range(len(vectors)):
            v1 = vectors[j]
            a1 = math.atan2(v1[0], v1[1])
            for k in range(j + 1, len(vectors)):
                v2 = vectors[k]
                a2 = math.atan2(v2[0], v2[1])
                angle_diffs.append(get_angle_diff(a1, a2))

        angle_span = np.sum(sorted(angle_diffs)[:3])

        # 2.a (Cont'd) Take only the smallest vectors, based on the angle spanned (1 per 90 degrees)
        vectors = vectors[:max(int(round(angle_span / (math.pi / 2))), 2)]
        total_vectors += vectors

    # 3. Take the median length, the 2 most common angles
    lengths = list(map(lambda v: math.hypot(v[0], v[1]), total_vectors))
    median_length = np.median(lengths)
    std_dev = np.std(lengths)
    angles = list(map(lambda v: math.atan2(v[1], v[0]), total_vectors))
    # Group angles based on the differences between angles
    ref_angles = []
    for i in range(len(angles)):
        angle_diffs = []
        in_ref_angles = False
        for ra in ref_angles:
            if get_angle_diff(angles[i], ra) < math.pi / 6:
                in_ref_angles = True
                break

        if not in_ref_angles:
            ref_angles.append(angles[i])

    if len(ref_angles) < 2:
        ref_angles.append(angles[-1])

    # Finally, pick the 2 ref angles with the largest difference
    ref_angle_diffs_pairs = []
    for i in range(len(ref_angles)):
        ra1 = ref_angles[i]
        for j in range(i + 1, len(ref_angles)):
            ra2 = ref_angles[j]
            ref_angle_diffs_pairs.append(
                (get_weird_angle_diff(ra1, ra2), ra1, ra2))

    _, a1, a2 = sorted(ref_angle_diffs_pairs,
                       key=lambda ra: ra[0], reverse=True)[0]

    if a1 < 0:
        a1 += math.pi
    if a2 < 0:
        a2 += math.pi

    # 4. Find the center point of the cube by taking the closest point to the x average and y average
    x_avg = 0
    y_avg = 0
    for c in center_points:
        x_avg += c[0]
        y_avg += c[1]
    x_avg /= len(center_points)
    y_avg /= len(center_points)

    distances_points_pairs = []
    for c in center_points:
        distances_points_pairs.append(
            (math.hypot(c[0] - x_avg, c[1] - y_avg), c))
    center_point_pair = sorted(distances_points_pairs, key=lambda d: d[0])[0]

    # Safety: just use the average if the closest point does not make sense
    center_point = center_point_pair[1] if center_point_pair[0] < 5 else (
        x_avg, y_avg)

    return median_length, std_dev, a1, a2, center_point


def make_grid(length, angle1, angle2, center_point):
    v1 = (length * math.cos(angle1), length * math.sin(angle1))
    v2 = (length * math.cos(angle2), length * math.sin(angle2))
    top_left_point = (center_point[0] - v1[0] -
                      v2[0], center_point[1] - v1[1] - v2[1])
    points = [top_left_point]
    last_x_point = top_left_point
    for i in range(2):
        new_point = (last_x_point[0] + v1[0], last_x_point[1] + v1[1])
        points.append(new_point)
        last_x_point = new_point
        last_y_point = new_point
        for j in range(2):
            new_point = (last_y_point[0] + v2[0], last_y_point[1] + v2[1])
            points.append(new_point)
            last_y_point = new_point

    return points


def get_angle_diff(a: float, b: float) -> float:
    return min((2 * math.pi) - abs(a - b), abs(a - b))


def get_weird_angle_diff(a: float, b: float) -> float:
    '''
    This one should return something less than 90 degrees:
    Make sure a and b are in the positive plane by adding math.pi
    AND make sure a and b are in the first quadrant by flipping around the y axis (math.pi - a)
    '''
    if a < 0:
        a += math.pi
    if b < 0:
        b += math.pi
    if a > math.pi / 2:
        a = math.pi - a
    if b > math.pi / 2:
        b = math.pi - b
    return abs(a - b)


if __name__ == '__main__':
    # center_points = [(58, 26), (28, 55), (57, 86), (29, 26), (28, 86), (87, 57), (87, 87), (86, 27), (43, 103)]
    center_points = [(57, 87), (58, 26), (28, 55), (29, 25),
                     (87, 57), (28, 85), (87, 27), (87, 86)]
    median_length, a1, a2 = detect_grid(center_points)
    print(f"Median length: {median_length}, Angle 1: {a1}, Angle 2: {a2}")
