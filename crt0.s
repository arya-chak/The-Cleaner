@ GBA crt0 — correct 192-byte header, then init code
    .section .text.start
    .arm
    .align 2
    .global _start

_start:
    @ Byte 0x000: branch to _gba_init at byte 0x0C0
    b       _gba_init

    @ Byte 0x004: Nintendo logo (156 bytes) — gbafix patches this
    .fill   156, 1, 0x00

    @ Byte 0x0A0: Game title (12 bytes)
    .ascii  "THE CLEANER "

    @ Byte 0x0AC: Game code (4 bytes)
    .ascii  "ACLG"

    @ Byte 0x0B0: Maker code (2 bytes)
    .ascii  "00"

    @ Byte 0x0B2: Fixed value
    .byte   0x96

    @ Byte 0x0B3: Unit code
    .byte   0x00

    @ Byte 0x0B4: Device type
    .byte   0x00

    @ Byte 0x0B5: Reserved (7 bytes)
    .fill   7, 1, 0x00

    @ Byte 0x0BC: Version
    .byte   0x00

    @ Byte 0x0BD: Complement check (patched by gbafix)
    .byte   0x00

    @ Byte 0x0BE: Reserved (2 bytes)
    .fill   2, 1, 0x00

    @ Byte 0x0C0: _gba_init — branch lands exactly here
_gba_init:
    .arm

    @ Set IRQ stack pointer
    mov     r0, #0x12
    msr     cpsr_c, r0
    ldr     sp, =__sp_irq

    @ Set system/user stack pointer
    mov     r0, #0x1F
    msr     cpsr_c, r0
    ldr     sp, =__sp_usr

    @ Copy .data from ROM to EWRAM
    ldr     r0, =__data_lma
    ldr     r1, =__data_start
    ldr     r2, =__data_end
    cmp     r1, r2
    bge     bss_clear

data_copy:
    ldr     r3, [r0], #4
    str     r3, [r1], #4
    cmp     r1, r2
    blt     data_copy

bss_clear:
    @ Zero out .bss
    ldr     r0, =__bss_start
    ldr     r1, =__bss_end
    mov     r2, #0
    cmp     r0, r1
    bge     call_main

bss_loop:
    str     r2, [r0], #4
    cmp     r0, r1
    blt     bss_loop

call_main:
    @ Switch to Thumb and call main
    ldr     r0, =main+1
    bx      r0

hang:
    b       hang