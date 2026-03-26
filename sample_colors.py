from PIL import Image
from collections import Counter

SPRITE_SHEET = '/Users/aryachakraborty/Downloads/Game Boy Advance - Grand Theft Auto Advance - Miscellaneous - Mike.png'

img = Image.open(SPRITE_SHEET).convert('RGBA')
pixels = list(img.getdata())

# Count all non-transparent, non-background colors
color_counts = Counter()
for r, g, b, a in pixels:
    if a == 0:
        continue
    # Skip the purple background color
    if r > 100 and b > 100 and g < 80:
        continue
    color_counts[(r, g, b)] += 1

print("Top 20 colors in sprite sheet (excluding background):")
print(f"{'Hex':>10}  {'RGB':>20}  {'Count':>8}")
print("-" * 45)
for (r, g, b), count in color_counts.most_common(20):
    print(f"  #{r:02x}{g:02x}{b:02x}   ({r:3d},{g:3d},{b:3d})   {count:>8}")
