/* GBA Linker Script */
OUTPUT_FORMAT("elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(_start)

MEMORY {
    ROM  (rx)  : ORIGIN = 0x08000000, LENGTH = 32M
    EWRAM (rwx): ORIGIN = 0x02000000, LENGTH = 256K
    IWRAM (rwx): ORIGIN = 0x03000000, LENGTH = 32K
}

SECTIONS {
    .text : {
        *(.text.start)
        *(.text*)
        *(.rodata*)
        . = ALIGN(4);
    } > ROM

    .data : {
        __data_start = .;
        *(.data*)
        . = ALIGN(4);
        __data_end = .;
    } > EWRAM AT > ROM

    .bss : {
        __bss_start = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        __bss_end = .;
    } > EWRAM

    __data_lma = LOADADDR(.data);
    __sp_irq  = ORIGIN(IWRAM) + LENGTH(IWRAM) - 0x60;
    __sp_usr  = __sp_irq - 0x100;
    __heap_start = __bss_end;
    __heap_end   = ORIGIN(EWRAM) + LENGTH(EWRAM);
}
