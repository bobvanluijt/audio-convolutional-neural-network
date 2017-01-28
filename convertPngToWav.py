#####################
#
#
#
#
#####################

from PIL import Image
import wave, struct, sys, soundfile as Sndfile, numpy as np, math

##
# Collect input
##
if sys.argv[1][-4:] != '.png':
    sys.exit("First argument should be a .png file")

if sys.argv[2][-4:] != '.wav':
    sys.exit("Second argument should be a .wav file")

##
# Conversion:
##

# Open image
with Image.open(sys.argv[1]) as pngFile:
    # Load image
    pngAllPixels = pngFile.load()
    # Set the counters that create the image
    countX = 0
    countY = 0
    count = pngFile.size[0] * pngFile.size[1]
    # Create the array which will contain all the bits
    bitArray = list()
    # Loop through the individual pixels
    while count > 0:
        # Set the location of the pixel that should be loaded
        singlePixel = pngAllPixels[countX, countY]
        # Get RGB vals and convert them to hex
        singlePixelToHexString = '%02x%02x%02x' % (singlePixel[0], singlePixel[1], singlePixel[2])
        # Convert hex string into actual hex
        if singlePixelToHexString == "000000":
            break # break because audio is < 44100 bit 
        singlePixelToHex = hex(int("0x" + singlePixelToHexString.lstrip("0"), 16) + int("0x0", 16))
        # This adds 16bit/2 (=32768) to the data and converts hex into a bit
        singleBit = int(singlePixelToHex, 16) - 32768 
        # Append the single bit to the array
        bitArray.append(singleBit)
        # Run through the image and set x and y vals (goes to next row when ready)
        if countX == (pngFile.size[0] - 1):
            countX = 0
            countY += 1
        else:
            countX += 1
        count -= 1
    # Convert the array into a Numpy array
    bitArrayNp = np.array(bitArray, dtype=np.int16)
    # Output the file
    Sndfile.write(sys.argv[2], bitArrayNp, 44100, 'PCM_16')