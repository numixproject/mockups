from PIL import Image, ImageDraw, ImageColor

import StringIO
import colorsys
import re


NUMIX = '#f1544d'


def clamp(x):
    return max(0, min(x, 255.0)) * 1.0


def parse(color):
    if re.match('numix(\s+(hex|red))?', color, re.IGNORECASE):
        color = NUMIX

    try:
        c = ImageColor.getrgb(color)
    except ValueError:
        return

    return (clamp(c[0]), clamp(c[1]), clamp(c[2]))


def formathex(rgb):
    return '#{0:02x}{1:02x}{2:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def tohex(color):
    c = parse(color)

    if c:
        return formathex(c)


def torgb(color):
    c = parse(color)

    if c:
        return 'rgb({0}, {1}, {2})'.format(c[0], c[1], c[2])


def tohsl(color):
    c = parse(color)

    if c:
        hls = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

        return 'hsl({0}, {1}%, {2}%)'.format(round(hls[0] * 360, 2), round(hls[2] * 100, 2), round(hls[1] * 100, 2))


def tohsv(color):
    c = parse(color)

    if c:
        hsv = colorsys.rgb_to_hsv(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)

        return 'hsv({0}, {1}%, {2}%)'.format(round(hsv[0] * 360, 2), round(hsv[1] * 100, 2), round(hsv[2] * 100, 2))


def lighten(color, percentage):
    c = parse(color)

    if c:
        hls1 = colorsys.rgb_to_hls(c[0] / 255.0, c[1] / 255.0, c[2] / 255.0)
        hls2 = (hls1[0], (hls1[1] + (percentage * 1.0 / 100)), hls1[2])
        rgb = colorsys.hls_to_rgb(hls2[0], hls2[1], hls2[2])

        return formathex((clamp(rgb[0] * 255.0), clamp(rgb[1] * 255.0), clamp(rgb[2] * 255.0)))


def darken(color, percentage):
    return lighten(color, percentage * -1)


def image(color):
    if re.match('numix(\s+(hex|red))?', color, re.IGNORECASE):
        color = NUMIX

    img = Image.new('RGB', (120, 120))
    draw = ImageDraw.Draw(img)

    try:
        draw.rectangle((0, 0, 120, 120), fill=color)
    except ValueError:
        return

    output = StringIO.StringIO()

    img.save(output, 'JPEG')

    return output.getvalue()
