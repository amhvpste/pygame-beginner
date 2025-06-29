from PIL import Image

image = Image.open("player.png").convert("RGBA")
datas = image.getdata()
new_data = []

for item in datas:
    r, g, b, a = item
    if r > 240 and g > 240 and b > 240:
        new_data.append((255, 255, 255, 0))  # прозорий
    else:
        new_data.append(item)

image.putdata(new_data)
image.save("teen_walk_sprite_clean.png")