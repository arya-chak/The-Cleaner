from PIL import Image
from collections import Counter

SPRITE_SHEET = '/Users/aryachakraborty/Downloads/Game Boy Advance - Grand Theft Auto Advance - Miscellaneous - Mike.png'

img = Image.open(SPRITE_SHEET).convert('RGBA')
width, height = img.size

color_counts = Counter()
for y in range(height):
    for x in range(width):
        r, g, b, a = img.getpixel((x, y))
        if a == 0:
            continue
        # Catch anything that looks yellow or yellow-green
        # High red + high green + low blue = yellow family
        if r > 150 and g > 150 and b < 100:
            color_counts[(r, g, b)] += 1

print("Yellow/green family colors in sprite sheet:")
print(f"{'Hex':>10}  {'RGB':>25}  {'Count':>8}")
print("-" * 50)
for (r, g, b), count in color_counts.most_common(30):
    print(f"  #{r:02x}{g:02x}{b:02x}   ({r:3d},{g:3d},{b:3d})   {count:>8}")
