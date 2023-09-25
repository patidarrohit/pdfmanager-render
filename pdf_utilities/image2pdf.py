from django.conf import settings
import img2pdf
import os


base_dir = str(settings.BASE_DIR)
#ts = str(int(round(datetime.now().timestamp())))


def image_to_pdf (img, output):
    fmt = {'jpg': 'JPEG',
           'png': 'PNG'}
    with open(output, 'wb') as f:
        f.write(img2pdf.convert(base_dir + img))
    return output

if __name__ == '__main__':
    pdf = "/Users/rohitmac/Downloads/0photoengrave.jpeg"
    output = "/Users/rohitmac/MyMAC/Projects/repo/pdfproject/pdf_project/output/pdfmerge/pdf_image"
    #pdf_to_image_low(pdf, base_dir + '/media/temp/pdf_rotate/'+output)
    image_to_pdf(pdf, '/Users/rohitmac/Downloads/test.pdf')