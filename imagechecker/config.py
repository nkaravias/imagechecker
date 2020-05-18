import csv
import logging
import imghdr
import os.path

LOGGER = logging.getLogger(__name__)
ALLOWED_IMAGE_TYPES = ['gif', 'pbm', 'pgm', 'ppm', 'tiff', 'webp', 'rast', 'xbm', 'jpeg', 'bmp', 'png', 'exr']


class AppConfig:
    def __init__(self, path):
        self.input_path = ''
        self.output_path = ''


class CsvConfig:
    """
        Represents the user provided input configuration & also handles the output
    """
    def __init__(self, path, output_path):
        self.path = path
        self.output_path = output_path
        self.name = ''
        self.contents = []
        FORMAT = "%(asctime)s:%(levelname)s:%(name)s: [%(filename)s:%(lineno)d] %(message)s"
        logging.basicConfig(format=FORMAT, level='INFO')

    def file_exists(self, path):
        """ Checks if the path belongs to a file """
        if not os.path.exists(path):
            LOGGER.error('The file {} does not exist'.format(path))
            return False
        return True

    def is_allowed_image(self, path):
        """ Checks if the image type is valid as per the configuration type whitelist """
        image_type = imghdr.what(path)
        if image_type not in ALLOWED_IMAGE_TYPES:
            LOGGER.error('Line {} is not a supported image type'.format(path))
            LOGGER.error('Allowed types: {}'.format(ALLOWED_IMAGE_TYPES))
            return False
        return True

    def validate(self):
        """
            Ensure the input csv has the proper contents so it can be parsed without issues:
            - Does each line have 2 fields?
            - Does each field represent a string?
            - Does each field point to a valid file? Is it an image?
        """
        with open(self.path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            line_count = 0
            self.contents = [rows for rows in csv_reader]
            for row in self.contents:
                if (len(row)) != 2:
                    LOGGER.error('CSV Line should have 2 fields only - {} has :{}'.format(row, len(row)))
                    exit(LOGGER.error('Exiting... - Invalid input configuration:{}'.format(self.path)))
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                for field in row:
                    if not self.file_exists(field) or not self.is_allowed_image(field):
                        exit(LOGGER.error('Exiting... - Invalid input configuration:{}'.format(self.path)))
            LOGGER.info('Valid input configuration:{}'.format(self.path))

    def report(self, csv_mode, image_a, image_b, similarity, effort_ms):
        """ Write image comparison results to the output (csv & stdout) """
        LOGGER.info('Writing to ouput: {} {} {} {}'.format(
            os.path.basename(image_a), os.path.basename(image_b), similarity,
            effort_ms))
        with open(self.output_path, mode=csv_mode) as output_file:
            csv_writer = csv.writer(output_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([image_a, image_b, similarity, effort_ms])
