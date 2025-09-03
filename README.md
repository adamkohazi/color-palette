# 🌈 Color palette generator and analyzer 📊
The goal of this app was to better understand how different color palette generation methods work in different color spaces or different color models.

## 🏗️ Current State
This project is still a work in progress. Some features may be untested, buggy, or completely missing.

## 📜 Color models
At this time the following color models are supported:
- CIEXYZ
- CIERGB
- sRGB (float)
- sRGB (8-bit)
- Oklab
- HSV

## 🧠 Analysis
Individual color component values can be viewed and compared in any of the supported color models in a table view.

Additionally, these values can be plotted against each other in either 2D or 3D scatter plots.

## 🖨️ Generation
Palette size can be increased or decreased, by adding or removing colors. Colors can be modified manually by adjusting any of their components (currently broken).

A few generation methods are implemented for creating a completely new palette. These are:
- Random (in any color model)
- Cosine (only in RGB)
- Monochrome (to be added)
