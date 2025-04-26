from paddleocr import PaddleOCR

# Initialize the OCR engine
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Test with a sample image
print("PaddleOCR is installed and ready to use!")