import csv
import logging
import imghdr
import os.path
import argparse
import yaml

LOGGER = logging.getLogger(__name__)


class AppConfig:
    """
        Represents the imagechecker configuration
    """
    def __init__(self):
        self.REQUIRED_CFG_SETTINGS = ['input_csv_path', 'output_csv_path', 'allowed_image_types']
        self.config_path = self.parse_input().config
        self.input, self.output, self.image_whitelist = self.load_app_config(self.config_path)
        LOGGER.info('ImageChecker config set to: {}'.format(self.config_path))

    def parse_input(self):
        """ Use argparser to allow the user to override the default ImageChecker configuration """
        parser = argparse.ArgumentParser(description='ImageChecker')
        parser.add_argument('-c',
                            '--config',
                            default=os.path.abspath('./conf/config.yaml'),
                            help='Specify the path of the ImageChecker configuration')
        return parser.parse_args()

    def load_app_config(self, path):
        """ Load the ImageChecker configuration and return the values from the YAML """
        with open(path) as f:
            cfg_props = yaml.safe_load(f)
        self.validate(cfg_props)
        return [cfg_props[setting] for setting in self.REQUIRED_CFG_SETTINGS]

    def validate(self, cfg_props):
        """ Ensure that the required fields are present in the ImageChecker configuration """
        if not all(elem in cfg_props for elem in self.REQUIRED_CFG_SETTINGS):
            exit((LOGGER.error(
                'Exiting... - Required properties {} missing from configuration at: {}'
                .format(self.REQUIRED_CFG_SETTINGS, self.config_path))))


class CsvConfig:
    """
        Represents the input & output configuration
    """
    def __init__(self, app_cfg):
        self.path = app_cfg.input
        self.output_path = app_cfg.output
        self.image_whitelist = app_cfg.image_whitelist
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
        if image_type not in self.image_whitelist:
            LOGGER.error('Line {} is not a supported image type'.format(path))
            LOGGER.error('Allowed types: {}'.format(self.image_whitelist))
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
