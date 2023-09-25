import PyPDF2 as p


def pdf_compress(pdf, output):
    reader = p.PdfFileReader(pdf)
    writer = p.PdfFileWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.addPage(page)

    with open(output, "wb") as f:
        writer.write(f)


if __name__ == "__main__":
    pdf = "/Users/rohitmac/MyMAC/Projects/repo/pdfproject/pdf_project/output/pdfmerge/pdf_merge_1653327541.pdf"
    output = "/Users/rohitmac/MyMAC/Projects/repo/pdfproject/pdf_project/output/pdfmerge/test.pdf"
    pdf_compress(pdf, output)
