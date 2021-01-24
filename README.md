# Vaonis-Stellina-Tools
Tools for Vaonis Stellina Image Handling


Bayer Convert:

FITS file series taken with an Stellina Vaonis telescope sometimes will have different bayer patterns depending on the sensor orientation. The sensor is sometimes rotated to an upside down position but internally the images are then rotated to have all image in same orientation. This causes the rotated images to have a different bayer pattern (RGGB becomes BGGR). To process the images further this has to be done in separate session.

BayerConvert allows to select a folder and a target bayer matrix conversion. All fits files in the folder will be examined and those with the selected bayer-matrix will be selected, rotated 180° and the bayer-matrix header will be set correctly.

Images are now not all in same direction, but that is no problem for most stacking and processing software. You can the process the complete series in one go.

Use at your own risk.


Requires: 

python 3.0
requires following imports:
- astropy
- pysimplegui
