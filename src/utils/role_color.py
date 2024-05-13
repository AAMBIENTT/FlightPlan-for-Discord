import io

from PIL import Image, ImageDraw  # type: ignore
import nextcord  # type:ignore
from nextcord.ext import commands  # type: ignore

from config import *

@commands.Cog.listener()
async def on_ready(self):
    print(self.__qualname__ + " STARTED")

async def change_color_role(guild, role_id, color):
    role = guild.get_role(role_id)
    if role:
        try:
            await role.edit(color=nextcord.Color.from_rgb(*color))
        except Exception as e:
            print(f"Failed to change color of role {role.name}: {e}")
    else:
        print(f"Role with ID {role_id} not found in guild {guild.name}")

async def generate_color_comparison_image(old_color, new_color):
    # Create a PIL image with the old and new colors side by side
    width, height = 150, 80
    image = Image.new("RGB", (width * 2, height), "white")
    draw = ImageDraw.Draw(image)

    # Draw rectangles for the old and new colors
    draw.rectangle([0, 0, width, height], fill=old_color)
    draw.rectangle([width, 0, width * 2, height], fill=new_color)

    # Save the image to bytes
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format="PNG")
    img_byte_array.seek(0)
    
    return img_byte_array.read()
