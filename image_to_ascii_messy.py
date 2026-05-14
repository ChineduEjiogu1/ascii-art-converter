# image_to_ascii.py
import sys



# ─────────────────────────────────────────
# Step 2: Read the entire PPM file into one string
# ─────────────────────────────────────────

if len(sys.argv) != 2:
    print("Usage: python image_to_ascii.py <filename>")
    sys.exit(1)


# ─────────────────────────────────────────
# Step 1: Define the character ramp (lightest to darkest)
# ─────────────────────────────────────────

ramp = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

with open(sys.argv[1], "rb") as f:
    magic_line = f.readline()
    magic = magic_line.strip().decode()    
    
    if magic == "P6":
        # New P6 path:
        # - read 2 more header lines
        # - read rest as binary pixel data
        # - convert to ints
        dimensions_line = f.readline()
        maxval_line = f.readline()
        pixel_bytes = f.read()


        width, height = map(int, dimensions_line.strip().decode().split())
        max_val = int(maxval_line.strip().decode())
        pixel_data = list(pixel_bytes)

    elif magic == "P3":
        # Old P3 path:
        # - read the rest of the file
        # - combine with magic_line (so we don't lose it)
        # - parse as before
        rest = f.read()
        all_text = (magic_line + rest).decode()
        num_list = [int(x) for x in all_text.split()]
        width, height, max_val, *pixel_data = num_list

    else:
        print(f"Unsupported format: {magic}")
        sys.exit(1)

# ─────────────────────────────────────────
# Step 3: Parse the contents into a list of integers
# (skip non-numeric tokens like "P3")
# ─────────────────────────────────────────


# ─────────────────────────────────────────
# Step 4: Unpack the header values from the pixel data
# ─────────────────────────────────────────


# ─────────────────────────────────────────
# Step 5: Walk the pixel data, 3 numbers at a time,
# and print one character per pixel.
# ─────────────────────────────────────────

# Assuming 'ramp' is your string of characters ordered from light to dark 
# (e.g., ramp = " .:-=+*#%@")

pixel_count = 0

for i in range(0, len(pixel_data), 3):
    # 5a. Extract R, G, B from this pixel
    r = pixel_data[i]
    g = pixel_data[i+1]
    b = pixel_data[i+2]
    
    # 5b. Compute brightness (simple average)
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    
    # 5c. Compute darkness fraction (0.0 = white, 1.0 = black)
    darkness_fraction = (255 - brightness) / 255
    
    # 5d. Find the index into the ramp
    index = int(darkness_fraction * (len(ramp) - 1))
    
    # 5e. Print the character (no newline yet)
    character = ramp[index]
    print(f"\033[38;2;{r};{g};{b}m{character * 2}\033[0m", end="")

    pixel_count += 1
    if (pixel_count % width) == 0:
        print()