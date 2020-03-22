from datetime import datetime
from PIL import Image, ImageChops

import pathlib
import subprocess

SET_TO_WALLPAPER = False  # Only works with GNOME

def render_greyline_composite(day_image, night_image, mask_image, render_filename, hour=None, callsign_image=None, callsign_dim=(0,0)):
    """
    Create a new composite image based off time of day.

    day_image (str): filepath to daytime map
    night_image (str): filepath to nighttime map
    mask_image (str): filepath to mask image
    render_filename (str): filepath to save output

    hour (float): hour of the day (can be left blank for UTC)   

    callsign_image (str): optional string of callsign filename
    callsign_dim (int tuple of length 3): (scale, x, y) location and scale of callsign
    """

    if hour is None: 
        time = datetime.utcnow()
        hour = time.hour + time.minute / 60

    day = Image.open(get_path(day_image))
    night = Image.open(get_path(night_image))

    mask = Image.open(get_path(mask_image)).convert('L')
    mask_width = mask.size[0]
    shift = -(mask_width/24)*(hour+12)
    mask = ImageChops.offset(mask, int(shift), 0)
    im = Image.composite(day, night, mask)

    if callsign_image:
        callsign = Image.open(get_path(callsign_image))
        call_x = int(callsign.size[0]/callsign_dim[0])
        call_y = int(callsign.size[1]/callsign_dim[0])

        callsign = callsign.resize((call_x, call_y), Image.LANCZOS)
        im.paste(callsign, (callsign_dim[1], callsign_dim[2]), callsign)

    im.save(get_path(render_filename))

def get_path(filename):
    path = pathlib.Path(__file__).parent.absolute()
    uri = "{}/{}".format(path, filename)
    return uri

def set_wallpaper(filename):
    """
    Set desktop wallpaper to image (GNOME ONLY)

    filename (str): path to image to be set as wallpaper
    """

    uri = get_path(filename)
    args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
    subprocess.Popen(args)

if __name__ == "__main__":
    render_greyline_composite("day_low.png", "night_low.png", "mask_low.png", "render.png", None, "callsign.png", (2.5, 970, 660))
    if SET_TO_WALLPAPER: set_wallpaper("render.png")
