# ASCII Art Converter

A tiny image-to-ASCII converter written in pure vanilla Python — no Pillow, no NumPy, no third-party libraries. Reads PPM (P3) image files and renders them to the terminal using a character density ramp.

## Usage

1. Convert any image to PPM format with ImageMagick:
2. Run the script with the PPM file as an argument:
3. Run: python image_to_ascii.py photo.ppm

## How it works

- Parses the PPM header to extract width, height, and max color value.
- Walks the pixel data three numbers at a time (R, G, B per pixel).
- Computes brightness as the average of R, G, B.
- Maps brightness to a position in a character ramp (` .:-=+*#%@`) — darker pixels get denser characters.
- Each character is printed twice horizontally to compensate for terminal cells being taller than they are wide.

## Limitations / next steps

- Only supports the ASCII variant of PPM (P3), not the binary variant (P6).
- Filename is hardcoded; no CLI argument support yet.
- Simple brightness average; doesn't use perceptual luminance weighting.

## Supported formats

Handles both PPM variants:
- **P3** (ASCII text) — bigger files, human-readable.
- **P6** (binary) — smaller files, the default ImageMagick produces.

No need to pass `-compress none` to ImageMagick anymore — either format works:
```
magick photo.jpg -resize 70x50 photo.ppm
```
