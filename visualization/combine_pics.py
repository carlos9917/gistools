import os
from PIL import Image
import matplotlib.pyplot as plt


def paste_images(fig1:str, fig2:str,outfig:str ,imgsize=(3000,1000)) -> None:
    coords_fig1 = (0, 0)
    coords_fig2 = (500,0)
    # opening up of images
    img1 = Image.open(fig1)
    img2 = Image.open(fig2)
    # creating a new image and pasting the
    # images
    img = Image.new("RGB",imgsize,"white") #Image.new("RGB", (250, 180), "white")

    # pasting the first image (image_name,
    # (position))
    img.paste(img1, coords_fig1)
    # pasting the second image (image_name,
    # (position))
    img.paste(img2, coords_fig2)
    #plt.imshow(img2)
    img.save(outfig)

if __name__=="__main__":
    fig1 = "stations_fyn_20220301.png"
    fig2 = "stations_fyn_20220303.png"
    out = "stations_fyn_increase_202203.png"

    #fig1 = "stations_mju_20230101.png"
    #fig2 = "stations_mju_20230118.png"
    #out = "stations_mju_increase_202301.png"

    #fig1 = "stations_nwz_20230101.png"
    #fig2 = "stations_nwz_20230120.png"
    #out = "stations_nwz_increase_202301.png"
    paste_images(fig1,fig2,out,(1200,500))
