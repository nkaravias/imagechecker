import logging
import time
from skimage.measure import compare_ssim

from config import CsvConfig
from image import Image

LOGGER = logging.getLogger(__name__)
CFG_PATH = 'examples/input.csv'
OUTPUT_PATH = 'examples/output.csv'


class ImageChecker:
    """
    Accepts a CSV file as input and calculates the SSIM value for each image pair provided.
    Generates report that contains the SSIM value & the processing time elapsed (ms)
    """
    def __init__(self):
        """ Probably load the configuration from another file here """
        NotImplemented

    def main():
        csv_input = CsvConfig(CFG_PATH, OUTPUT_PATH)
        csv_input.validate()
        csv_input.report('w', 'image1', 'image2', 'similarity', 'elapsed')

        for line in csv_input.contents:
            start_time = int(round(time.time() * 1000))
            image1 = Image(line[0])
            image2 = Image(line[1])
            (score, diff) = compare_ssim(image1.grayscale, image2.grayscale, full=True)
            bjorn_score = round(score.item(), 3)
            if bjorn_score > 0.99:
                bjorn_score = 0
            time_diff = int(round(time.time() * 1000)) - start_time
            csv_input.report('a', image1.path, image2.path, bjorn_score, time_diff)


if __name__ == '__main__':
    FORMAT = "%(asctime)s:%(levelname)s:%(name)s: [%(filename)s:%(lineno)d] %(message)s"
    logging.basicConfig(format=FORMAT, level='INFO')
    try:
        ImageChecker.main()
    except Exception as e:
        LOGGER.info('Caught an unexpected exception: {}'.format(e))
        exit(1)
