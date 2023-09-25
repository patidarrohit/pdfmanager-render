import PyPDF2 as p


def pdfextract(inp_file, pages_to_extract, op_file):
    pdf_file_obj = inp_file  # open(inp_file, 'rb')
    pdf_reader = p.PdfFileReader(pdf_file_obj)
    pdf_writer = p.PdfFileWriter()
    print(type(pdf_file_obj))
    page_nums = [int(i.split(".")[0].split("_")[2]) for i in pages_to_extract]
    print(page_nums)
    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        if page_nums:
            x = page_nums[0]
            if page == x:
                pdf_writer.addPage(page_obj)
                page_nums.pop(0)

    with open(op_file, 'wb') as f:
        pdf_writer.write(f)

    pdf_file_obj.close()


if __name__ == "__main__":
    inp = '/Users/rohitmac/Downloads/00 Sedgwick U.S. Leave of Absence Process Document - FINAL.pdf'
    op = '/Users/rohitmac/Downloads/test.pdf'
    with open(inp, 'rb') as f:
        pages = ['abc_abc_1.pdf']
        pdf_extract(f, pages, op)
