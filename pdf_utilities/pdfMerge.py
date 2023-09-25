import PyPDF2 as p
import os
from datetime import datetime


src_dir = '/Users/rohitmac/Downloads'


def pdf_merge(pdfs, output, ts):
    pdf_merger = p.PdfFileMerger()
    for f in pdfs:
        #file = os.path.join('/Users/rohitmac/Downloads', f)
        pdf_merger.append(f)
    op_dir = f'./media/temp/pdf_merge/{ts}'
    os.system(f'mkdir -p {op_dir}')
    op_file_name = op_dir + '/' + output + '.pdf'
    with open(op_file_name, 'wb') as f:
        pdf_merger.write(f)
    return op_dir, output+'.pdf'


if __name__ == "__main__":
    pdf_files = ['/Users/rohitmac/Downloads/Additional Tips for the Interview.pdf', '/Users/rohitmac/Downloads/Additional Tips for the Interview.pdf']
    output = '/Users/rohitmac/test.pdf'
    pdf_merge(pdfs=pdf_files, output=output)
