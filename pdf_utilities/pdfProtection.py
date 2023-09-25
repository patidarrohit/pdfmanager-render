import PyPDF2 as p
import os


def pdf_add_password(pdf, passwd, output_pdf):
    pdf_reader = p.PdfFileReader(pdf)
    pdf_writer = p.PdfFileWriter()

    try:
        pdf_nums = pdf_reader.numPages
    except p.errors.PdfReadError:
        print(f'PDF file {pdf} is already encrypted. Please upload the file which is not password protected.')
        exit()

    for i in range(pdf_nums):
        page = pdf_reader.getPage(i)
        pdf_writer.addPage(page)

    if passwd is not None:
        if pdf_reader.isEncrypted:
            print(f'PDF file {pdf} is already encrypted. Please upload the file which is not password protected.')
        else:
            pdf_writer.encrypt(passwd)
            output_file = output_pdf

    with open(output_file, 'wb') as f:
        pdf_writer.write(f)

    return True

def pdf_remove_password(pdf, passwd, output_pdf):
    pdf_reader = p.PdfFileReader(pdf)
    pdf_writer = p.PdfFileWriter()

    if pdf_reader.isEncrypted:
        pdf_reader.decrypt(passwd)
        output_file = output_pdf
    else:
        print(f'PDF file {pdf} is not encrypted. please pass correct file which is password protected.')

    try:
        pdf_nums = pdf_reader.numPages
    except p.errors.PdfReadError:
        print(f'PDF file {pdf} is already encrypted. Please upload the file which is not password protected.')
        return False

    for i in range(pdf_nums):
        page = pdf_reader.getPage(i)
        pdf_writer.addPage(page)

    with open(output_file, 'wb') as f:
        pdf_writer.write(f)

    return True


if __name__ == "__main__":
    pdf = '/Users/rohitmac/Downloads/JEE_Score_encrypted.pdf'
    op =  '/Users/rohitmac/Downloads/JEE_Score_decrypted.pdf'
    pdf_remove_password(pdf, '1234', op)
