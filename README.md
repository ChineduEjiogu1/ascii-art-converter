# ASCII Art Converter

A pure-Python image-to-ASCII converter — no Pillow, no NumPy, no third-party libraries. Reads PPM image files (both ASCII `P3` and binary `P6` variants) and renders them as colored ASCII art in the terminal, or saves them to a plain text file.

## Usage

First, convert any image to PPM format using ImageMagick:

```
magick photo.jpg -resize 70x50 photo.ppm
```

Then run the script:

```
# Print colored ASCII art to terminal
python image_to_ascii.py photo.ppm

# Save plain ASCII art to a text file (no color codes)
python image_to_ascii.py photo.ppm output.txt
```

## Features

- **Both PPM variants**: ASCII (`P3`) and binary (`P6`), auto-detected from the file's magic number.
- **Perceptual luminance**: uses ITU-R BT.601 weights (`0.299·R + 0.587·G + 0.114·B`) instead of naive averaging, accounting for the human eye's higher sensitivity to green light.
- **70-character density ramp** for smooth tonal gradients.
- **ANSI truecolor output**: each character is rendered in the original pixel's color when printing to a terminal. Requires a truecolor-capable terminal (Windows Terminal, modern macOS Terminal, iTerm2). Will not render colors in legacy `cmd.exe`.
- **Optional file output**: pass a second filename to save plain ASCII (color codes stripped) to a text file. Output is written as UTF-8.
- **Aspect-ratio compensation**: each character is printed twice horizontally to counteract terminal cells being roughly twice as tall as they are wide.

## How it works

1. Reads the PPM file in binary mode and auto-detects the format from the magic number.
2. Parses the header (width, height, max color value).
3. For `P3`: parses the rest as whitespace-separated ASCII integers. For `P6`: reads the rest as raw bytes (each byte = one R, G, or B value).
4. For each pixel, computes brightness using the luminance formula, then maps that brightness to a position in the character ramp.
5. Outputs each character either to the terminal (with ANSI color escape codes) or to a buffer that gets written to a file at the end.

## Limitations / possible next steps

- No CLI flag system yet (e.g., `--no-color`); arguments are positional only.
- Relies on external tools (like ImageMagick) for converting JPEG/PNG to PPM.
- Future ideas: generate PPM files programmatically (gradients, Mandelbrot fractals), add dithering, support PGM (grayscale) input.
