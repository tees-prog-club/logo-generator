# Logo Generator
Generates the Teesside University Programming Club logo using Sutherland-Hodgman clipping.

Moves a mask across a logo shape to generate stripes on it using the [Sutherland-Hodgman](https://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm) polygon clipping algorithm. In the end, outputs an SVG of the logo to `logo.svg` in the same directory.  

## Render
Here's the logo that the program produces, rendered as a PNG.

![Logo](logo.png)

## Usage
This program is written in the scripting language Python. You'll need Python installed on your machine to run it. Call it like this:

```
python logo.py <number_of_stripes> <stripe_spacing>
```

So to create the logo as you see it in this repo, run it like this:

```
python logo.py 4 4.0
```

## Files
There is a base polygon (`base.poly`) which is just a list of vertex coordinates drawing out the outline of the logo and a clipping polygon (`clip.poly`) which the program moves (or *translates*) downwards to create the stripes. The colour palette is in `colours.txt` in hexadecimal format (one per line, no blank lines). These colours are applied cyclically to the stripes. 

A skeleton SVG file is located in `outline.svg`. It's **not** actually the logo outline (that's in `base.poly`) but rather an outline of an SVG document ready for the program to fill in.

The file `logo.svg` is an example render generated by the program. The file `logo.png` is what the render looks like rasterised as a PNG image.

## Limitations
If you give a stripe count or stripe spacing that causes the clipping polygon to fall completely outside the bounds of the base shape, you'll get an error when the program tries to apply the clipping algorithm. Try adjusting the command line arguments you provide.
