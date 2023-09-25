import PyPDF2 as p


def get_info(path):
    with open(path, 'rb') as f:
        pdf = p.PdfFileReader(f)
        info = pdf.getDocumentInfo()
        num_of_pages = pdf.getNumPages()

    print(info)
    author = info.author
    creator = info.creator
    producer = info.producer
    subject = info.subject
    title = info.title


if __name__ == "__main__":
    path = '/Users/rohitmac/Downloads/Rental_Application.pdf'
    get_info(path)