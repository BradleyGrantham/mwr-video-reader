"""Optical Character Recognition (OCR) using pytesseract and some pre-processing."""
import cv2
import pytesseract

import mwrvr.constants


def pre_process(image):
    """Pre-processing step to increase accuracy of tesseract OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    bordersize = 2
    border = cv2.copyMakeBorder(gray, top=bordersize, bottom=bordersize,
                                left=0, right=0,
                                borderType=cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return border


def ocr_string(image):
    """Given an image, return the text from the image as a string."""
    return pytesseract.image_to_string(
        pre_process(image), lang="eng", config=mwrvr.constants.TESSERACT_CONFIG
    )
