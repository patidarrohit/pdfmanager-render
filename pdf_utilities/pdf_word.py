from pdf2docx import parse


def convert_pdf_to_word(pdf, op_file):
    parse(pdf, op_file)


# def convert_word_to_pdf(doc, op_file):
#     convert(doc, op_file)


if __name__ == "__main__":
    pdf = '/Users/rohitmac/Downloads/new.pdf'
    op_file = '/Users/rohitmac/Downloads/pdf_to_word_1654204764.docx'
    #convert_pdf_to_word(pdf, op_file)
    #convert_word_to_pdf(op_file, pdf)
