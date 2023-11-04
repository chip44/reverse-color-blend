#!/usr/bin/env python3

from argparse import ArgumentParser
from math import ceil

from PIL import Image


def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return r, g, b


def reverse_blend(pixel, color):
    # Convention:
    # R, G, B are in the range 0 to 255 inclusive
    # alpha is in the range 0 to 1 inclusive

    # Stop if the pixel is already fully transparent
    if pixel[3] == 0:
        return (0, 0, 0, 0)

    # Red channel
    alpha = 0
    if pixel[0] > color[0]:
        alpha = (pixel[0] - color[0]) / (255 - color[0])
    elif pixel[0] < color[0]:
        alpha = (color[0] - pixel[0]) / color[0]

    # Green channel
    alpha2 = 0
    if pixel[1] > color[1]:
        alpha2 = (pixel[1] - color[1]) / (255 - color[1])
    elif pixel[1] < color[1]:
        alpha2 = (color[1] - pixel[1]) / color[1]
    if alpha2 > alpha:
        alpha = alpha2

    # Blue channel
    alpha2 = 0
    if pixel[2] > color[2]:
        alpha2 = (pixel[2] - color[2]) / (255 - color[2])
    elif pixel[2] < color[2]:
        alpha2 = (color[2] - pixel[2]) / color[2]
    if alpha2 > alpha:
        alpha = alpha2

    if alpha > 0:  # if not fully transparent
        # Color removal
        # Use of ceiling guarantees reproducibility of blended image.
        alpha = ceil(255 * alpha)
        result = (
            ceil((255 * pixel[0] - (255 - alpha) * color[0]) / alpha),
            ceil((255 * pixel[1] - (255 - alpha) * color[1]) / alpha),
            ceil((255 * pixel[2] - (255 - alpha) * color[2]) / alpha),
            alpha,
        )
        return result

    # Fully transparent, result is undefined
    return (0, 0, 0, 0)


if __name__ == "__main__":
    parser = ArgumentParser(description="Unblend a color from an image")
    parser.add_argument("input", type=str, help="Input file path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file path")
    parser.add_argument("-c", "--color", type=str, required=True, help="Color to unblend (hex)")
    args = parser.parse_args()

    src = Image.open(args.input)
    if src.mode == "RGB":
        src = src.convert("RGBA")
    color = hex_to_rgb(args.color)

    dst = Image.new("RGBA", src.size)
    for y in range(src.height):
        for x in range(src.width):
            pixel = src.getpixel((x, y))
            result = reverse_blend(pixel, color)
            dst.putpixel((x, y), result)
    dst.save(args.output)

    src.close()
