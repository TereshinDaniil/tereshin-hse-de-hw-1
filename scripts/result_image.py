from PIL import Image, ImageDraw, ImageFont


def draw_result(total, unique, preview):
    """Render the SQL result used both in the last cell and in the README."""
    canvas = Image.new("RGB", (870, 354), "white")
    draw = ImageDraw.Draw(canvas)
    title = ImageFont.load_default(size=25)
    body = ImageFont.load_default(size=19)
    draw.rectangle((0, 0, 870, 70), fill="#15354c")
    draw.text((24, 19), "stg.population", font=title, fill="white")
    draw.text((482, 24), f"Rows: {total}     Unique keys: {unique}", font=body, fill="white")
    positions = (24, 245, 360, 655)
    headers = ("country_code", "year", "country_name", "population")
    for x, label in zip(positions, headers):
        draw.text((x, 90), label, font=body, fill="#1f5770")
    for index, (country, year, name, count) in enumerate(preview):
        top = 128 + 43 * index
        if index % 2 == 0:
            draw.rectangle((10, top - 4, 860, top + 32), fill="#f0f5f7")
        for x, value in zip(positions, (country, str(year), name, f"{count:,}")):
            draw.text((x, top), value, font=body, fill="#15354c")
    return canvas
