import PyPDF2 as p


def pdfrotate(inp_file, output_file, rotation):
    pdf_file_obj = open(inp_file, 'rb')
    pdf_reader = p.PdfFileReader(pdf_file_obj)
    pdf_writer = p.PdfFileWriter()

    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        page_obj.rotateClockwise(rotation)

        pdf_writer.addPage(page_obj)
    
    output = open(output_file, 'wb')

    pdf_writer.write(output)
    pdf_file_obj.close()
    output.close()


def pdf_rotate_selected(inp_file, pages_to_rotate, op_file, rotation):
    pdf_file_obj = inp_file # open(inp_file, 'rb')
    pdf_reader = p.PdfFileReader(pdf_file_obj)
    pdf_writer = p.PdfFileWriter()
    print(type(pdf_file_obj))
    page_nums = [int(i.split(".")[0].split("_")[2]) for i in pages_to_rotate]
    print(page_nums)
    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        if page_nums:
            x = page_nums[0]
            if page == x:
                page_obj.rotateClockwise(rotation)
                page_nums.pop(0)
        pdf_writer.addPage(page_obj)

    with open(op_file, 'wb') as f:
        pdf_writer.write(f)

    pdf_file_obj.close()


if __name__ == "__main__":
    origFileName = '/Users/rohitmac/Downloads/Hardik_10th.pdf'
    newFileName = '/Users/rohitmac/Downloads/Hardik_10th_90.pdf'
    rotation = 90
    pdfrotate(origFileName, newFileName, rotation)
    
