from PIL import Image, ImageDraw, ImageFont
import os

def make_image(foto, x, y_dict, text_dict):
    img= Image.open(foto)
    l_y = list(y_dict.keys())
    l_text = list(text_dict.keys())
    d1 = ImageDraw.Draw(img)
    for i in range(1, len(l_y) + 1):
        d1.text((x, y_dict["y" + str(i)]), text_dict["text_" + str(i)], fill =(2, 0, 0))
    img.show()
    return img

y_dictionary = dict()
for i in range(1, 12):
    y_dictionary["y" + str(i)] = 69 + (i-1) * 45.5


text_dictionary = dict()
for i in range(1, 12):
    text_dictionary["text_" + str(i)] = str(round(0.09 - (i -1) * (0.09 + 0.09) / 10, 3))




x = 45

for i in [-2.5, -2.0, -1.8, -1.6, -1.5, -1.4, -1.2, -1.0, -0.5, 0.0]:
    os.chdir("/home/thodoris/Downloads/pics_CH3NH3_side")
    pic = "CH3NH3_side_" + str(i) + ".png"
    im = make_image(foto = pic, x = x, y_dict = y_dictionary, text_dict = text_dictionary)
    os.chdir("/home/thodoris/Downloads/pics_CH3NH3_side/pics_with_numbers")
    im.save("CH3NH3_side_" + str(i) + "_numbers.png")

