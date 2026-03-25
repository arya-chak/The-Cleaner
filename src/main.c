// GBA hardware registers — direct memory-mapped I/O
#define REG_DISPCNT  (*(volatile unsigned short*)0x04000000)
#define MODE_3       0x0003
#define BG2_ON       0x0400

typedef unsigned short u16;
typedef unsigned int   u32;

#define VRAM         ((volatile u16*)0x06000000)
#define SCREEN_W     240
#define SCREEN_H     160

#define RGB5(r,g,b)  (((r) & 0x1F) | (((g) & 0x1F) << 5) | (((b) & 0x1F) << 10))

// Plot a single pixel in Mode 3
static inline void plot(int x, int y, u16 color) {
    VRAM[y * SCREEN_W + x] = color;
}

int main(void) {
    // Set Mode 3, BG2 enabled
    REG_DISPCNT = MODE_3 | BG2_ON;

    // Fill screen — dark blue-grey, 1973 NYC night
    u16 bg = RGB5(4, 6, 10);
    for (int y = 0; y < SCREEN_H; y++) {
        for (int x = 0; x < SCREEN_W; x++) {
            plot(x, y, bg);
        }
    }

    // White dot at center — proof of life
    plot(120, 80, RGB5(31, 31, 31));

    // Halt
    while (1) {}
    return 0;
}
