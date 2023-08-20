import glob
import pathlib
import subprocess
import cv2


min_padding_px = 10
input_extension = '.png'
output_extension = '.png'

current_path = pathlib.Path(__file__).parent.absolute()
load_path = str(current_path) + '/input/*{}'.format(input_extension)
save_path = str(current_path) + '/output/'


def main():
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
    files = sorted(glob.glob(load_path, recursive = True))

    for file in files:
        # Load the image in black and white (0 - b/w, 1 - color).
        img_bw = cv2.imread(file, 0)
        img_col = cv2.imread(file, 1)

        # Make <min_padding_px> border around both images.
        img_bw = cv2.copyMakeBorder(
            img_bw,
            top = min_padding_px,
            bottom = min_padding_px,
            left = min_padding_px,
            right = min_padding_px,
            borderType = cv2.BORDER_CONSTANT,
            value = [255, 255, 255]
        )

        img_col = cv2.copyMakeBorder(
            img_col,
            top = min_padding_px,
            bottom = min_padding_px,
            left = min_padding_px,
            right = min_padding_px,
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
        top_x = min([x for (x, y, w, h) in rects]) - min_padding_px
        top_y = min([y for (x, y, w, h) in rects]) - min_padding_px
        bottom_x = max([x + w for (x, y, w, h) in rects]) + min_padding_px
        bottom_y = max([y + h for (x, y, w, h) in rects]) + min_padding_px

        # Crop the colored image by the rectangle
        output = img_col[top_y:bottom_y, top_x:bottom_x]
        filename = pathlib.Path(file).stem

        # Save it as out.jpg
        cv2.imwrite(save_path + filename + output_extension, output)

    print('Done!')


if __name__ == '__main__':
    main()
