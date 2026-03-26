// ============================================================
// The Cleaner — Step 2: Sprite + 8-directional movement
// Mode 0, OAM hardware sprites, keypad input
// ============================================================

typedef unsigned short     u16;
typedef unsigned int       u32;

#define REG_DISPCNT     (*(volatile u16*)0x04000000)
#define DCNT_MODE0      0x0000
#define DCNT_OBJ        0x1000
#define DCNT_OBJ_1D     0x0040

#define REG_VCOUNT      (*(volatile u16*)0x04000006)

#define REG_KEYINPUT    (*(volatile u16*)0x04000130)
#define KEY_RIGHT       0x0010
#define KEY_LEFT        0x0020
#define KEY_UP          0x0040
#define KEY_DOWN        0x0080

#define VRAM_OBJ_TILES  ((volatile u16*)0x06010000)
#define OBJ_PALETTE     ((volatile u16*)0x05000200)
#define OAM             ((volatile u16*)0x07000000)

#define SCREEN_W        240
#define SCREEN_H        160

// OAM helpers
#define OBJ_Y(y)        ((y) & 0xFF)
#define OBJ_SHAPE_SQ    (0 << 14)
#define OBJ_X(x)        ((x) & 0x1FF)
#define OBJ_HFLIP       (1 << 12)
#define OBJ_SIZE_8      (0 << 14)
#define OBJ_TILE(t)     ((t) & 0x3FF)
#define OBJ_PRIO(p)     ((p) << 10)
#define OBJ_PALBANK(b)  ((b) << 12)
#define OBJ_HIDE_Y      160

static inline void oam_set(int idx, u16 attr0, u16 attr1, u16 attr2) {
    volatile u16 *e = OAM + idx * 4;
    e[0] = attr0;
    e[1] = attr1;
    e[2] = attr2;
    e[3] = 0;
}

static inline void vsync(void) {
    while (REG_VCOUNT >= 160) {}
    while (REG_VCOUNT <  160) {}
}

static inline int key_held(u16 mask) {
    return !(REG_KEYINPUT & mask);
}

// 8x8 sprite, 4bpp palette bank 0
// PIX(a,b): a = left pixel, b = right pixel
// Palette: 0=transparent, 1=dark coat, 2=skin, 3=coat highlight
#define PIX(a,b) ((u16)(((b) << 4) | (a)))

static const u16 vincent_gfx[32] = {
    // Row 0:  . . @ @ | @ @ . .
    PIX(0,0), PIX(2,2), PIX(2,2), PIX(0,0),
    // Row 1:  . . @ * | @ @ . .
    PIX(0,0), PIX(2,3), PIX(2,2), PIX(0,0),
    // Row 2:  . . @ @ | @ @ . .
    PIX(0,0), PIX(2,2), PIX(2,2), PIX(0,0),
    // Row 3:  . # # # | # # # .
    PIX(0,1), PIX(1,1), PIX(1,1), PIX(1,0),
    // Row 4:  . # # # | # # # .
    PIX(0,1), PIX(1,1), PIX(1,1), PIX(1,0),
    // Row 5:  . # # @ | @ # # .
    PIX(0,1), PIX(1,1), PIX(2,2), PIX(1,0),
    // Row 6:  . . # # | # # . .
    PIX(0,0), PIX(1,1), PIX(1,1), PIX(0,0),
    // Row 7:  . . # . | . # . .
    PIX(0,0), PIX(1,0), PIX(0,1), PIX(0,0),
};

static void load_palette(void) {
    OBJ_PALETTE[0] = 0x0000;
    OBJ_PALETTE[1] = (u16)((6) | (6 << 5) | (7 << 10));    // dark charcoal
    OBJ_PALETTE[2] = (u16)((22) | (15 << 5) | (12 << 10)); // warm tan
    OBJ_PALETTE[3] = (u16)((18) | (18 << 5) | (19 << 10)); // mid-grey
}

static void load_tiles(void) {
    for (int i = 0; i < 32; i++) {
        VRAM_OBJ_TILES[i] = vincent_gfx[i];
    }
}

// Fixed-point movement (1/256 pixel units)
#define SUBPX           256
#define SPEED_WALK      (2 * SUBPX)
#define SPEED_DIAG      (SUBPX + SUBPX/2)

#define START_X         ((SCREEN_W / 2 - 4) * SUBPX)
#define START_Y         ((SCREEN_H / 2 - 4) * SUBPX)
#define MIN_X           (0)
#define MAX_X           ((SCREEN_W - 8) * SUBPX)
#define MIN_Y           (0)
#define MAX_Y           ((SCREEN_H - 8) * SUBPX)

static inline int clamp(int v, int lo, int hi) {
    if (v < lo) return lo;
    if (v > hi) return hi;
    return v;
}

int main(void) {
    REG_DISPCNT = DCNT_MODE0 | DCNT_OBJ | DCNT_OBJ_1D;

    load_palette();
    load_tiles();

    // Hide all 128 sprites on startup — prevents garbage
    for (int i = 0; i < 128; i++) {
        oam_set(i, OBJ_HIDE_Y, 0, 0);
    }

    int vx = START_X;
    int vy = START_Y;
    int hflip = 0;

    while (1) {
        vsync();

        // Input
        int dx = 0, dy = 0;
        if (key_held(KEY_LEFT))  { dx = -1; hflip = 1; }
        if (key_held(KEY_RIGHT)) { dx =  1; hflip = 0; }
        if (key_held(KEY_UP))      dy = -1;
        if (key_held(KEY_DOWN))    dy =  1;

        // Move
        int speed = (dx != 0 && dy != 0) ? SPEED_DIAG : SPEED_WALK;
        vx = clamp(vx + dx * speed, MIN_X, MAX_X);
        vy = clamp(vy + dy * speed, MIN_Y, MAX_Y);

        // Update OAM
        int px = vx >> 8;
        int py = vy >> 8;
        u16 attr0 = (u16)(OBJ_Y(py) | OBJ_SHAPE_SQ);
        u16 attr1 = (u16)(OBJ_X(px) | OBJ_SIZE_8 | (hflip ? OBJ_HFLIP : 0));
        u16 attr2 = (u16)(OBJ_TILE(0) | OBJ_PRIO(0) | OBJ_PALBANK(0));
        oam_set(0, attr0, attr1, attr2);
    }

    return 0;
}