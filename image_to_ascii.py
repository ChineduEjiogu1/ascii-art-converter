# image_to_ascii.py
import sys

# ─────────────────────────────────────────
# Step 1: Define the character ramp (lightest to darkest)
# ─────────────────────────────────────────
ramp = " .:-=+*#%@"

# ─────────────────────────────────────────
# Step 2: Read the entire PPM file into one string
# ─────────────────────────────────────────

if len(sys.argv) != 2:
    print("Usage: python image_to_ascii.py <filename>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    contents = f.read()

# ─────────────────────────────────────────
# Step 3: Parse the contents into a list of integers
# (skip non-numeric tokens like "P3")
# ─────────────────────────────────────────
num_list = [int(x) for x in contents.split() if x.isdigit()]

# ─────────────────────────────────────────
# Step 4: Unpack the header values from the pixel data
# ─────────────────────────────────────────
width, height, max_val, *pixel_data = num_list

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
    print(character * 2, end="")

    pixel_count += 1
    if (pixel_count % width) == 0:
        print()