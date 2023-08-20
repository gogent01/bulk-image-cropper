from glob import glob
from pathlib import Path
import argparse
import subprocess
import cv2

def parseArguments():
    script_directory = Path(__file__).parent.absolute()
    parser = argparse.ArgumentParser(description = 'A tool to crop excessive white background around objects on images (or to grow some white background around if not enough).')
    parser.add_argument(
        '-i', 
        '--input-dir',
        action = 'store',
        dest = 'input_dir', 
        default = Path(script_directory / 'input').resolve(),
        help = 'A path to a directory with images to crop.'
    )
    parser.add_argument(
        '-o', 
        '--output-dir',
        action = 'store',
        dest = 'output_dir', 
        default = Path(script_directory / 'output').resolve(),
        help = 'A path to an output directory to place cropped images.'
    )
    parser.add_argument(
        '-p', 
        '--padding',
        action = 'store',
        dest = 'padding_px', 
        type = int,
        default = 10,
        help = 'A width of a white background padding around an object on an image in pixels.'
    )
    parser.add_argument(
        '-e', 
        '--extensions',
        action = 'append',
        dest = 'extensions',
        type = str,
        nargs = '*',
        choices = ['png', 'jpg', 'tiff'],
        default = ['png', 'jpg', 'tiff'],
        help = 'Extensions of images to crop.'
    )

    args = parser.parse_args()

    if 'jpg' in args.extensions:
        args.extensions += ['jpeg', 'jpe']

    if 'tiff' in args.extensions:
        args.extensions += ['tif']

    return args


def main():
    args = parseArguments()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))

    files = []
    for extension in args.extensions:
        files += glob('{}/*.{}'.format(args.input_dir, extension), recursive = True)

    for file in files:
        # Load the image in black and white (0 - b/w, 1 - color).
        img_bw = cv2.imread(file, 0)
        img_col = cv2.imread(file, 1)

        # Make <args.padding_px> border around both images.
        img_bw = cv2.copyMakeBorder(
            img_bw,
            top = args.padding_px,
            bottom = args.padding_px,
            left = args.padding_px,
            right = args.padding_px,
            borderType = cv2.BORDER_CONSTANT,
            value = [255, 255, 255]
        )

        img_col = cv2.copyMakeBorder(
            img_col,
            top = args.padding_px,
            bottom = args.padding_px,
            left = args.padding_px,
            right = args.padding_px,
            borderType = cv2.BORDER_CONSTANT,
            value = [255, 255, 255]
        )

        # Get height and width of the images.
        h, w = img_bw.shape[:2]

        # Invert the image to be white on black for compatibility with findContours.
        img_bw_inverted = cv2.morphologyEx(255 - img_bw, cv2.MORPH_OPEN, kernel)

        # Binarize the image and make thresholding.
        ret, thresh = cv2.threshold(img_bw_inverted, 10, 255, cv2.THRESH_BINARY)

        # Find all the contours in thresh.
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Calculate bounding rectangles for each contour.
        rects = [cv2.boundingRect(cnt) for cnt in contours]

        # Calculate the combined bounding rectangle points.
        top_x = min([x for (x, y, w, h) in rects]) - args.padding_px
        top_y = min([y for (x, y, w, h) in rects]) - args.padding_px
        bottom_x = max([x + w for (x, y, w, h) in rects]) + args.padding_px
        bottom_y = max([y + h for (x, y, w, h) in rects]) + args.padding_px

        # Crop the colored image by the rectangle
        output = img_col[top_y:bottom_y, top_x:bottom_x]
        filename = Path(file).name

        # Save the image with same name and extension
        cv2.imwrite(str(args.output_dir / filename), output)

    print('Done!')


if __name__ == '__main__':
    main()
