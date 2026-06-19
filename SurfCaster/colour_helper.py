def interpolate_colour(c1, c2, f):

    return tuple(int(c1[i] + (c2[i] - c1[i]) * f) for i in range(3))

def get_gradient(value, minV=0, maxV=100):

    red = (242, 13, 45)
    yellow = (238, 216, 17)
    green = (24, 231, 60)

    value = max(minV, min(value, maxV))

    percent = (value - minV) / (maxV - minV)

    if percent < 0.5:
        factor = percent / 0.5
        color = interpolate_colour(green, yellow, factor)
    else:
        factor = (percent - 0.5) / 0.5
        color = interpolate_colour(yellow, red, factor)

    return f"rgb({color[0]}, {color[1]}, {color[2]})"