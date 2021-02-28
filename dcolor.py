import requests

from colorthief import ColorThief
from colormap import rgb2hex
from PIL import Image
from io import BytesIO
 
async def dominant_color(link):

    response = requests.get(link)
    data = BytesIO(response.content)
    color_thief = ColorThief(data)
    dc = color_thief.get_color(quality=1)    
    hex = rgb2hex(dc[0], dc[1], dc[2])

    return hex
    