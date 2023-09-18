from PIL import Image, ImageDraw, ImageFont


def make_image(foto, x, y_dict, text_dict):
    img= Image.open(foto)
    l_y = list(y_dict.keys())
    l_text = list(text_dict.keys())
    d1 = ImageDraw.Draw(img)
    for i in range(1, len(l_y) + 1):
        d1.text((x, y_dict["y" + str(i)]), text_dict["text_" + str(i)], fill =(2, 0, 0))
        #print(y_dict["y" + str(i)])
        #print(text_dict["text_" + str(i)])
    img.show()


y_dictionary = dict()
for i in range(1, 11):
    y_dictionary["y" + str(i)] = 69 + (i-1) * 44


text_dictionary = dict()
for i in range(1, 11):
    text_dictionary["text_" + str(i)] = str(round(0.09 - (i -1) * 0.02, 3))




x = 45
pic = "NH4_top_-2.5.png"

make_image(foto = pic, x = x, y_dict = y_dictionary, text_dict = text_dictionary)


