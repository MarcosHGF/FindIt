def calculate_distance(obj1, obj2):
    x1, y1 = obj1["position"]["x_center"], obj1["position"]["y_center"]
    x2, y2 = obj2["position"]["x_center"], obj2["position"]["y_center"]
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def infer_region(position):
    x_center, y_center = position["x_center"], position["y_center"]

    if x_center < 300 and y_center < 300:
        return "top-left corner"
    elif x_center > 300 and y_center < 300:
        return "top-right corner"
    elif x_center < 300 and y_center > 300:
        return "bottom-left corner"
    elif x_center > 300 and y_center > 300:
        return "bottom-right corner"
    else:
        return "center"