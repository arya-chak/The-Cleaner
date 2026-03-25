# ========================
# The Cleaner — GBA Makefile
# ========================

TARGET    := build/thecleaner
SOURCES   := src
INCLUDES  := include $(LIBGBA)/include $(LIBTONC)/include

# Toolchain
PREFIX    := arm-none-eabi-
CC        := $(PREFIX)gcc
AS        := $(PREFIX)as
OBJCOPY   := $(PREFIX)objcopy

# GBA-specific compiler flags
ARCH      := -mthumb-interwork -mthumb
CFLAGS    := $(ARCH) -O2 -Wall -Wextra \
             -mcpu=arm7tdmi -mtune=arm7tdmi \
             -fomit-frame-pointer -ffast-math \
             $(foreach dir, $(INCLUDES), -I$(dir))

# Linker — use our own script, no specs file needed
LDFLAGS   := -mthumb-interwork \
             -mcpu=arm7tdmi \
             -nostartfiles \
             -T gba.ld

# Source files
CFILES    := $(foreach dir, $(SOURCES), $(wildcard $(dir)/*.c))
OFILES    := $(CFILES:%.c=build/%.o) build/crt0.o

# ========================
# Targets
# ========================

.PHONY: all clean

all: $(TARGET).gba

# Link ELF
$(TARGET).elf: $(OFILES) gba.ld
	@mkdir -p $(dir $@)
	$(CC) $(LDFLAGS) $(OFILES) -o $@

# Convert ELF to GBA ROM and fix header
$(TARGET).gba: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@
	gbafix $@
	@echo "Built: $@"

# Compile C files
build/src/%.o: src/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Assemble crt0
build/crt0.o: crt0.s
	@mkdir -p $(dir $@)
	$(CC) -mcpu=arm7tdmi -marm -xassembler-with-cpp -c $< -o $@

clean:
	rm -rf build