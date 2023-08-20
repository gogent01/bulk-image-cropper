# bulk-image-cropper
A tiny Python script using cv2 to crop images on white background, leaving only a white border of a specified width around the images. Builds up missing white background to the specified width, if there is not enough one on an original image. Supports PNG, JPEG, and TIFF images. Can be run from a command line. Examples of input and output images can be viewed in corresponding folders.

### How to run
```
cropper.py [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-p PADDING_PX] [-e [{png,jpg,tiff} [{png,jpg,tiff} ...]]]
```
All arguments are optional. Called without arguments the script will crop all images from an `./input` folder and put the result in an `./output` folder, leaving the white border of `10 px` around the content on each image.

Details on arguments:
```
-h, --help            show this help message and exit
-i INPUT_DIR, --input-dir INPUT_DIR
                      A path to a directory with images to crop. 
                      Defaults to an 'input' folder in the script location.
-o OUTPUT_DIR, --output-dir OUTPUT_DIR
                      A path to an output directory to place cropped images. 
                      Defaults to an 'output' folder in the script location.
-p PADDING_PX, --padding PADDING_PX
                      A width of a white background padding around an object in pixels. 
                      Defaults to 10 px.
-e [{png,jpg,tiff} [{png,jpg,tiff} ...]], --extensions [{png,jpg,tiff} [{png,jpg,tiff} ...]]
                      Extensions of images to crop. 
                      Defaults to png, jpg and tiff altogether.
```