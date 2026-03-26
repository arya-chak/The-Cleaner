from PIL import Image
import os

# ============================================================
# The Cleaner — NPC Sprite Recolor Script v3
# Range-based color matching — handles all shade variations
# ============================================================

SPRITE_SHEET = '/Users/aryachakraborty/Downloads/Game Boy Advance - Grand Theft Auto Advance - Miscellaneous - Mike.png'
OUTPUT_DIR   = '/Users/aryachakraborty/GameBuilding/The Cleaner/sprites'

def is_yellow(r, g, b):
    """Catch all yellow/yellow-green trouser shades."""
    return r > 140 and g > 140 and b < 110

def is_coat_light(r, g, b):
    """Light blue-grey coat highlight."""
    return 120 <= r <= 165 and 155 <= g <= 200 and 155 <= b <= 200 and abs(g - b) < 30

def is_coat_mid(r, g, b):
    """Medium blue coat."""
    return 85 <= r <= 125 and 110 <= g <= 150 and 140 <= b <= 180 and b > g > r

def is_coat_dark(r, g, b):
    """Dark blue-purple coat shadow."""
    return 70 <= r <= 110 and 65 <= g <= 100 and 100 <= b <= 140 and b > r and b > g

def is_skin_dark(r, g, b):
    """Dark skin shadow."""
    return 110 <= r <= 150 and 75 <= g <= 115 and 50 <= b <= 90 and r > g > b

def is_skin_mid(r, g, b):
    """Mid skin tone."""
    return 170 <= r <= 215 and 130 <= g <= 170 and 90 <= b <= 130 and r > g > b

def is_skin_light(r, g, b):
    """Light skin highlight."""
    return 230 <= r <= 255 and 190 <= g <= 220 and 125 <= b <= 165 and r > g > b

def is_skin_warm(r, g, b):
    """Warm skin tone."""
    return 230 <= r <= 255 and 165 <= g <= 200 and 115 <= b <= 150 and r > g > b

# ============================================================
# Character color output definitions
# Each character maps a category to its new RGB color
# ============================================================
CHARACTERS = {
    'vincent': {
        'coat_light': ( 36,  48,  96),
        'coat_mid':   ( 26,  35,  64),
        'coat_dark':  ( 15,  20,  45),
        'trouser_1':  ( 58,  90, 140),
        'trouser_2':  ( 74, 111, 165),
        'skin_dark':  (160,  90,  40),
        'skin_mid':   (198, 134,  66),
        'skin_light': (220, 160,  90),
        'skin_warm':  (210, 150,  80),
    },
    'sal': {
        'coat_light': ( 55,  55,  55),
        'coat_mid':   ( 35,  35,  35),
        'coat_dark':  ( 20,  20,  20),
        'trouser_1':  ( 28,  28,  28),
        'trouser_2':  ( 42,  42,  42),
        'skin_dark':  (150,  85,  35),
        'skin_mid':   (185, 125,  60),
        'skin_light': (205, 150,  80),
        'skin_warm':  (195, 138,  70),
    },
    'dena': {
        'coat_light': (160, 100,  50),
        'coat_mid':   (120,  70,  25),
        'coat_dark':  ( 80,  45,  15),
        'trouser_1':  ( 90,  60,  35),
        'trouser_2':  (115,  80,  48),
        'skin_dark':  (175, 120,  70),
        'skin_mid':   (215, 170, 120),
        'skin_light': (235, 195, 150),
        'skin_warm':  (225, 182, 135),
    },
    'caruso': {
        'coat_light': (110, 110, 130),
        'coat_mid':   ( 85,  85, 105),
        'coat_dark':  ( 60,  60,  80),
        'trouser_1':  ( 72,  72,  88),
        'trouser_2':  ( 92,  92, 110),
        'skin_dark':  (155,  95,  45),
        'skin_mid':   (192, 138,  68),
        'skin_light': (215, 162,  90),
        'skin_warm':  (205, 150,  78),
    },
    'enzo': {
        'coat_light': ( 70,  95,  60),
        'coat_mid':   ( 50,  72,  42),
        'coat_dark':  ( 32,  50,  28),
        'trouser_1':  ( 28,  28,  28),
        'trouser_2':  ( 42,  42,  42),
        'skin_dark':  (140,  80,  30),
        'skin_mid':   (175, 115,  52),
        'skin_light': (198, 140,  72),
        'skin_warm':  (188, 128,  62),
    },
}

def classify_pixel(r, g, b):
    """Return the category name for a pixel, or None if unmatched."""
    if is_yellow(r, g, b):
        # Map brightness to trouser shade
        brightness = (r + g + b) / 3
        return 'trouser_1' if brightness < 200 else 'trouser_2'
    if is_coat_light(r, g, b):  return 'coat_light'
    if is_coat_mid(r, g, b):    return 'coat_mid'
    if is_coat_dark(r, g, b):   return 'coat_dark'
    if is_skin_dark(r, g, b):   return 'skin_dark'
    if is_skin_mid(r, g, b):    return 'skin_mid'
    if is_skin_light(r, g, b):  return 'skin_light'
    if is_skin_warm(r, g, b):   return 'skin_warm'
    return None

def recolor(image, palette):
    img = image.convert('RGBA')
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            category = classify_pixel(r, g, b)
            if category and category in palette:
                nr, ng, nb = palette[category]
                pixels[x, y] = (nr, ng, nb, a)
    return img

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Loading sprite sheet...")
    sheet = Image.open(SPRITE_SHEET)
    print(f"Sheet size: {sheet.size}")

    for name, palette in CHARACTERS.items():
        print(f"Generating {name}...")
        result = recolor(sheet, palette)
        out_path = os.path.join(OUTPUT_DIR, f'{name}_sheet.png')
        result.save(out_path)
        print(f"  Saved → {out_path}")

    print(f"\nDone. {len(CHARACTERS)} character sheets saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
