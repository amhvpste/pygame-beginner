from PIL import Image

image = Image.open("sprite_sheet.png").convert("RGBA")

cols, rows = 4, 3
frame_width = image.width // cols
frame_height = image.height // rows

standard_size = (frame_width, frame_height)  # повертаємось до 256×192

frame_num = 0
for row in range(rows):
    for col in range(cols):
        left = col * frame_width
        upper = row * frame_height
        right = left + frame_width
        lower = upper + frame_height

        frame = image.crop((left, upper, right, lower))

        # Обрізаємо зайвий простір
        bbox = frame.getbbox()
        if not bbox:
            continue

        cropped = frame.crop(bbox)

        # Вставляємо в центр нового прозорого полотна
        result = Image.new("RGBA", standard_size, (255, 255, 255, 0))
        offset_x = (standard_size[0] - cropped.width) // 2
        offset_y = (standard_size[1] - cropped.height) // 2
        result.paste(cropped, (offset_x, offset_y))

        frame_num += 1
        result.save(f"frame_fixed_{frame_num:02}.png")