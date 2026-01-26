# Images Directory

This directory contains image assets for SEO and branding.

## Required Images for Production

For optimal social media sharing, convert the SVG files to PNG/JPG:

### og-image.png (1200x630px)
Used for Open Graph (Facebook, LinkedIn) and Twitter Cards.

```bash
# Using ImageMagick
convert -background none -density 300 og-image.svg -resize 1200x630 og-image.png

# Using Inkscape
inkscape --export-type=png --export-width=1200 --export-height=630 og-image.svg -o og-image.png

# Using rsvg-convert
rsvg-convert -w 1200 -h 630 og-image.svg > og-image.png
```

### apple-touch-icon.png (180x180px)
```bash
# From the root favicon.svg
convert -background none ../favicon.svg -resize 180x180 apple-touch-icon.png
```

### favicon.ico
```bash
convert -background none ../favicon.svg -resize 32x32 favicon.ico
# Move to frontend root
mv favicon.ico ../
```

## Online Alternatives
- https://cloudconvert.com/svg-to-png
- https://svgtopng.com/
- Figma/Canva export

## Current Files
- `og-image.svg` - Source for Open Graph image
- `logo.svg` - AiInPocket logo
