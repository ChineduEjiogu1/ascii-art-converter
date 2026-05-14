import sys

# Validate args
if len(sys.argv) not in (2, 3):
    print("Usage: python image_to_ascii.py <filename> [output_file]")
    sys.exit(1)

output_file = sys.argv[2] if len(sys.argv) == 3 else None

# Character ramp
ramp = " .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

# ─── Phase 1: Read the file and parse it (format-dependent) ───
with open(sys.argv[1], "rb") as f:
    magic_line = f.readline()
    magic = magic_line.strip().decode()
    
    if magic == "P6":
        dimensions_line = f.readline()
        maxval_line = f.readline()
        pixel_bytes = f.read()
        
        width, height = map(int, dimensions_line.strip().decode().split())
        max_val = int(maxval_line.strip().decode())
        pixel_data = list(pixel_bytes)
    
    elif magic == "P3":
        # Read the rest of the file, combine with magic_line (already consumed),
        # decode to text, then parse the old way.
        rest = f.read()
        all_text = (magic_line + rest).decode()
        num_list = [int(x) for x in all_text.split() if x.isdigit()]
        width, height, max_val, *pixel_data = num_list
    
    else:
        print(f"Unsupported format: {magic}")
        sys.exit(1)

# ─── Phase 2: Render the pixels (same for both formats) ───

output_buffer = []

pixel_count = 0

for i in range(0, len(pixel_data), 3):
    r = pixel_data[i]
    g = pixel_data[i+1]
    b = pixel_data[i+2]
    
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    darkness_fraction = (255 - brightness) / 255
    index = int(darkness_fraction * (len(ramp) - 1))
    character = ramp[index]

    if output_file is None:
        # 1. Print colored version directly to terminal
        print(f"\033[38;2;{r};{g};{b}m{character * 2}\033[0m", end="")
    else:
        # 2. Add plain characters to buffer for file writing
        output_buffer.append(character * 2)
    
    pixel_count += 1
    if pixel_count % width == 0:
        if output_file is None:
            print()  # Standard terminal newline
        else:
            output_buffer.append("\n")

if output_file is not None:
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("".join(output_buffer))
    print(f"Saved to {output_file}")