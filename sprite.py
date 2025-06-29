from PIL import Image

# Завантаження великого спрайт-листа
image = Image.open("player2.png").convert("RGBA")

cols, rows = 4, 2
frame_width = image.width // cols
frame_height = image.height // rows
target_size = (128, 128)

frame_num = 0
for row in range(rows):
    for col in range(cols):
        # Обрізаємо один великий кадр
        left = col * frame_width
        upper = row * frame_height
        right = left + frame_width
        lower = upper + frame_height
        big_frame = image.crop((left, upper, right, lower))

        # 🔧 Масштабуємо з збереженням пропорцій
        scale = min(target_size[0] / big_frame.width, target_size[1] / big_frame.height)
        new_size = (int(big_frame.width * scale), int(big_frame.height * scale))
        scaled = big_frame.resize(new_size, resample=Image.BICUBIC)

        # 🔲 Вставляємо в центр прозорого 128×128 кадру
        result = Image.new("RGBA", target_size, (255, 255, 255, 0))
        offset_x = (target_size[0] - new_size[0]) // 2
        offset_y = (target_size[1] - new_size[1]) // 2
        result.paste(scaled, (offset_x, offset_y))

        result.save(f"frame_{frame_num:02}.png")
        frame_num += 1