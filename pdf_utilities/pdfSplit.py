import os
import PyPDF2 as p
import zipfile
import pathlib


def pdf_split_old(pdf, splits):
    pdf_reader = p.PdfFileReader(pdf)
    if len(splits) >= pdf_reader.getNumPages() or splits[-1] >= pdf_reader.getNumPages():
        raise Exception('Number of splits are more than pages in pdf.')

    start = 0
    end = splits[0]

    for i in range(len(splits) + 1):
        pdf_writer = p.PdfFileWriter()
        output_pdf = pdf.split('.pdf')[0] + str(i) + '.pdf'

        for page in range(start, end):
            pdf_writer.addPage(pdf_reader.getPage(page))

        with open(output_pdf, 'wb') as f:
            pdf_writer.write(f)

        start = end
        try:
            end = splits[i+1]
        except IndexError:
            end = pdf_reader.numPages


def pdf_split_zip(pdf, splits, op_dir):
    pdf_reader = p.PdfFileReader(pdf)
    if len(splits) >= pdf_reader.getNumPages() or splits[-1] >= pdf_reader.getNumPages():
        raise Exception('Number of splits are more than pages in pdf.')

    start = 0
    end = splits[0] + 1

    for i in range(len(splits) + 1):
        pdf_writer = p.PdfFileWriter()
        op_file_nme = os.path.basename(pdf).split(".")[0]
        output_pdf = op_dir + '/' + op_file_nme + "_" + str(i) + '.pdf'

        for page in range(start, end):
            pdf_writer.addPage(pdf_reader.getPage(page))

        with open(output_pdf, 'wb') as f:
            pdf_writer.write(f)

        start = end
        try:
            end = splits[i+1]
        except IndexError:
            end = pdf_reader.numPages

    return create_zip_file(op_dir)


def create_zip_file(op_dir):
    src_dir = pathlib.Path(op_dir)
    tgt_dir = os.path.dirname(os.path.dirname(op_dir)) + '/zip'
    os.system(f"mkdir -p {tgt_dir}")
    tgt_file = f"{tgt_dir}/output.zip"

    with zipfile.ZipFile(tgt_file, mode="w") as z:
        for file in src_dir.iterdir():
            z.write(file, arcname=file.name)

    return tgt_file


def main():
    pdf = '/Users/rohitmac/Downloads/Rental_Application.pdf'
    # Splits is list of pages from where you want to split the pdf
    splits = [3]
    pdf_split_old(pdf, splits)


if __name__ == "__main__":
    main()
