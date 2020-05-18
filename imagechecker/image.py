import cv2


class Image:
    def __init__(self, path):
        self.path = path
        self.value = cv2.imread(self.path)
        self.grayscale = cv2.cvtColor(self.value, cv2.COLOR_BGR2GRAY)
