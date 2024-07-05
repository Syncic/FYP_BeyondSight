def get_center(box):
    x, y, w, h = box
    return (x + w // 2, y + h // 2)

def get_location(center, width, height):
    center_x, center_y = center
    if center_x < width // 4:
        return "Left"
    elif center_x > width * 3 // 4:
        return "Right"
    else:
        return "Center"
