from datetime import datetime
from PIL import Image, ImageChops

import pathlib
import subprocess

def render_greyline_composite(day_image, night_image, mask_image, render_filename, hour=None):
    """
    Create a new composite image based off time of day.

    day_image (str): filepath to daytime map
    night_image (str): filepath to nighttime map
    mask_image (str): filepath to mask image
    render_filename (str): filepath to save output

    hour (float): hour of the day (can be left blank for UTC)
    """

    if hour is None: 
        time = datetime.utcnow()
        hour = time.hour + time.minute / 60

    day = Image.open(day_image)
    night = Image.open(night_image)

    mask = Image.open(mask_image).convert('L')
    mask_width = mask.size[0]
    shift = -(mask_width/24)*(hour+12)
    mask = ImageChops.offset(mask, int(shift), 0)
    im = Image.composite(day, night, mask)

    im.save(render_filename)

def set_wallpaper(filename):
    """
    Set desktop wallpaper to image (GNOME ONLY)

    filename (str): path to image to be set as wallpaper
    """

    path = pathlib.Path().absolute()
    uri = "{}/{}".format(path, filename)

    args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
    subprocess.Popen(args)

if __name__ == "__main__":
    render_greyline_composite("day_low.png", "night_low.png", "mask_low.png", "render.png")
    #set_wallpaper("render.png") # Only uncomment if you're running GNOME
