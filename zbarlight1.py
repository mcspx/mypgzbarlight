from PIL import Image
import zbarlight

file_path = 'qrcode1.png'
with open(file_path, 'rb') as image_file:
    image = Image.open(image_file)
    image.load()

codes = zbarlight.scan_codes('qrcode', image)
print('QR codes: %s' % codes)
