import PyPDF2 as p


def get_text(path, output):
    with open(path, 'rb') as f:
        pdf = p.PdfFileReader(f)
        for i in range(pdf.getNumPages()):
            page = pdf.getPage(i)
            text = page.extractText()
            with open(output, 'w+') as out:
                out.write(text)


if __name__ == '__main__':
    path = '/Users/rohitmac/Downloads/Rental_Application.pdf'
    output = '/Users/rohitmac/Downloads/extracted.txt'
    get_text(path, output)