from PIL import Image
import os

# ============================================================
# The Cleaner — NPC Sprite Recolor Script v2
# ============================================================

SPRITE_SHEET = '/Users/aryachakraborty/Downloads/Game Boy Advance - Grand Theft Auto Advance - Miscellaneous - Mike.png'
OUTPUT_DIR   = '/Users/aryachakraborty/GameBuilding/The Cleaner/sprites'

# ============================================================
# Original Mike colors (sampled directly from sprite sheet)
# ============================================================
COAT_LIGHT   = (144, 176, 176)  # #90b0b0
COAT_MID     = (104, 128, 160)  # #6880a0
COAT_DARK    = ( 88,  80, 120)  # #585078
TROUSER_1    = (248, 176,   0)  # #f8b000
TROUSER_2    = (248, 248,   0)  # #f8f800
TROUSER_3    = (255, 255,   0)  # #ffff00
SKIN_DARK    = (128,  96,  72)  # #806048
SKIN_MID     = (192, 152, 112)  # #c09870
SKIN_LIGHT   = (248, 208, 144)  # #f8d090
SKIN_WARM    = (248, 184, 136)  # #f8b888

CHARACTERS = {
    'vincent': {
        COAT_LIGHT:  ( 36,  48,  96),
        COAT_MID:    ( 26,  35,  64),
        COAT_DARK:   ( 15,  20,  45),
        TROUSER_1:   ( 58,  90, 140),
        TROUSER_2:   ( 74, 111, 165),
        TROUSER_3:   ( 90, 130, 180),
        SKIN_DARK:   (160,  90,  40),
        SKIN_MID:    (198, 134,  66),
        SKIN_LIGHT:  (220, 160,  90),
        SKIN_WARM:   (210, 150,  80),
    },
    'sal': {
        COAT_LIGHT:  ( 55,  55,  55),
        COAT_MID:    ( 35,  35,  35),
        COAT_DARK:   ( 20,  20,  20),
        TROUSER_1:   ( 30,  30,  30),
        TROUSER_2:   ( 40,  40,  40),
        TROUSER_3:   ( 50,  50,  50),
        SKIN_DARK:   (150,  85,  35),
        SKIN_MID:    (185, 125,  60),
        SKIN_LIGHT:  (205, 150,  80),
        SKIN_WARM:   (195, 138,  70),
    },
    'dena': {
        COAT_LIGHT:  (160, 100,  50),
        COAT_MID:    (120,  70,  25),
        COAT_DARK:   ( 80,  45,  15),
        TROUSER_1:   ( 90,  60,  35),
        TROUSER_2:   (110,  75,  45),
        TROUSER_3:   (125,  88,  55),
        SKIN_DARK:   (175, 120,  70),
        SKIN_MID:    (215, 170, 120),
        SKIN_LIGHT:  (235, 195, 150),
        SKIN_WARM:   (225, 182, 135),
    },
    'caruso': {
        COAT_LIGHT:  (110, 110, 130),
        COAT_MID:    ( 85,  85, 105),
        COAT_DARK:   ( 60,  60,  80),
        TROUSER_1:   ( 75,  75,  90),
        TROUSER_2:   ( 90,  90, 108),
        TROUSER_3:   (105, 105, 122),
        SKIN_DARK:   (155,  95,  45),
        SKIN_MID:    (192, 138,  68),
        SKIN_LIGHT:  (215, 162,  90),
        SKIN_WARM:   (205, 150,  78),
    },
    'enzo': {
        COAT_LIGHT:  ( 70,  95,  60),
        COAT_MID:    ( 50,  72,  42),
        COAT_DARK:   ( 32,  50,  28),
        TROUSER_1:   ( 28,  28,  28),
        TROUSER_2:   ( 38,  38,  38),
        TROUSER_3:   ( 48,  48,  48),
        SKIN_DARK:   (140,  80,  30),
        SKIN_MID:    (175, 115,  52),
        SKIN_LIGHT:  (198, 140,  72),
        SKIN_WARM:   (188, 128,  62),
    },
}

def recolor(image, color_map):
    img = image.convert('RGBA')
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if (r, g, b) in color_map:
                nr, ng, nb = color_map[(r, g, b)]
                pixels[x, y] = (nr, ng, nb, a)
    return img

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Loading sprite sheet...")
    sheet = Image.open(SPRITE_SHEET)
    print(f"Sheet size: {sheet.size}")

    for name, color_map in CHARACTERS.items():
        print(f"Generating {name}...")
        result = recolor(sheet, color_map)
        out_path = os.path.join(OUTPUT_DIR, f'{name}_sheet.png')
        result.save(out_path)
        print(f"  Saved → {out_path}")

    print(f"\nDone. {len(CHARACTERS)} character sheets saved to {OUTPUT_DIR}")

if __name__ == '__main__':
    main()
