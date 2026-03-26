from PIL import Image
import os

# ============================================================
# The Cleaner — NPC Sprite Recolor Script
# ============================================================
# Reads the original Mike sprite sheet and outputs one
# recolored PNG per character into the sprites/ output folder.
# ============================================================

SPRITE_SHEET = '/Users/aryachakraborty/Downloads/Game Boy Advance - Grand Theft Auto Advance - Miscellaneous - Mike.png'
OUTPUT_DIR   = '/Users/aryachakraborty/GameBuilding/The Cleaner/sprites'

# Original Vincent colors (from your GIMP work)
ORIGINAL = {
    'coat':       (26,  35,  64),   # #1a2340 navy coat
    'coat_hi':    (36,  48,  96),   # #243060 coat highlight
    'jeans':      (74, 111, 165),   # #4a6fa5 denim blue
    'skin':       (198, 134,  66),  # #c68642 tan skin
    'outline':    (13,  13,  13),   # #0d0d0d near black outline
}

# ============================================================
# Character color mappings
# Each entry maps original color → new color
# Only the colors you want to change need to be listed
# ============================================================
CHARACTERS = {
    'vincent': {
        # Vincent is the baseline — no changes, just outputs clean version
    },
    'sal': {
        # Underboss — black suit, grey shirt, distinguished
        ORIGINAL['coat']:    (20,  20,  20),   # black suit jacket
        ORIGINAL['coat_hi']: (35,  35,  35),   # black suit highlight
        ORIGINAL['jeans']:   (25,  25,  25),   # black suit trousers
        ORIGINAL['skin']:    (180, 120,  55),   # slightly older skin tone
    },
    'dena': {
        # Bookkeeper — warm brown coat, practical
        ORIGINAL['coat']:    (100,  60,  20),  # brown coat
        ORIGINAL['coat_hi']: (130,  80,  30),  # brown coat highlight
        ORIGINAL['jeans']:   (80,   50,  30),  # dark brown skirt/trousers
        ORIGINAL['skin']:    (210, 160, 110),  # lighter skin tone
    },
    'caruso': {
        # Plainclothes detective — muted grey suit
        ORIGINAL['coat']:    (65,  65,  90),   # grey suit jacket
        ORIGINAL['coat_hi']: (85,  85, 110),   # grey suit highlight
        ORIGINAL['jeans']:   (55,  55,  75),   # grey suit trousers
        ORIGINAL['skin']:    (195, 140,  70),  # standard skin
    },
    'enzo': {
        # Freelancer — dark olive/green jacket, cold
        ORIGINAL['coat']:    (35,  55,  35),   # dark olive jacket
        ORIGINAL['coat_hi']: (50,  75,  50),   # olive highlight
        ORIGINAL['jeans']:   (25,  25,  25),   # black trousers
        ORIGINAL['skin']:    (170, 110,  50),  # darker, weathered skin
    },
}

def recolor(image, color_map):
    """Replace each pixel color according to color_map {old_rgb: new_rgb}."""
    img = image.convert('RGBA')
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue  # skip transparent pixels
            rgb = (r, g, b)
            if rgb in color_map:
                nr, ng, nb = color_map[rgb]
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
