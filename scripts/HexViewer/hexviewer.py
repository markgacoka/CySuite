def gif_header_data():
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

def hex_viewer(out_file):
    contents = gif_header_data()
    original_length = len(contents)
    new_bytes  = b'\x2f\x2f\x2f\x2f\x2f'
    byte_index = original_length + len(new_bytes)

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
        return(hexdump(malicious_image[0:128]) + '\n' + '*' + '\n' + hexdump(malicious_image[byte_index-13:byte_index+128]))
    else:
        return(hexdump(malicious_image))