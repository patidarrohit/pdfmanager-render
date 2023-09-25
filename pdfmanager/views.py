from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.core.files import File
from pdf_utilities.image2pdf import image_to_pdf
from pdf_utilities.pdfMerge import pdf_merge as pm
from pdf_utilities.pdfImage import pdf_to_image_low, pdf_to_image
from pdf_utilities.pdfRotate import pdf_rotate_selected
from pdf_utilities.pdfExtract import pdfextract
from pdf_utilities.pdfSplit import pdf_split_zip
from pdf_utilities.pdf_word import convert_pdf_to_word #, convert_word_to_pdf
from pdf_utilities.pdfProtection import pdf_add_password, pdf_remove_password
from django.conf import settings
from datetime import datetime
import os
import mimetypes
from django.http import FileResponse, Http404


base_dir = str(settings.BASE_DIR)
temp_dir = '/Users/rohitmac/MyMAC/Projects/repo/pdfproject/pdf_project/output/temp'


def get_curr_dir():
    curr_dir_name = str(int(round(datetime.now().timestamp())))
    os.system(f"mkdir {temp_dir}/{curr_dir_name}")
    curr_dir = temp_dir + '/' + curr_dir_name
    return curr_dir

def home(request):
    return render(request, "pdfmanager/home.html")


def about(request):
    return render(request, "pdfmanager/about.html")


# def pdf_merge(request):
#     op_file_name = 'pdf_merge_' + str(int(round(datetime.now().timestamp())))
#     if request.method == 'POST':
#         my_files = request.FILES
#         # with open('/Users/rohitmac/test.pdf', 'wb+') as destination:
#         #     for chunk in my_file.chunks():
#         #         destination.write(chunk)
#         file_list = []
#         for k, v in my_files.items():
#             file_list.append(v)
#         file_dir, file_name = pm(file_list, op_file_name)
#         with open(file_dir+'/'+file_name, 'rb') as f:
#             mime_type, _ = mimetypes.guess_type(file_dir+'/'+file_name)
#             print(mime_type)
#             response = HttpResponse(f, content_type=mime_type)
#             response['Content-Disposition'] = "attachment; filename=%s" % file_name
#             print(response)
#         return redirect("/pdfmergedownload/")
#     return render(request, "pdfmanager/pdfmerge.html")

def pdf_merge(request):
    return render(request, "pdfmanager/pdfmerge.html")


def pdf_merge_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_name = 'pdf_merge_' + ts
    if request.method == 'POST':
        my_files = request.FILES
        file_list = []
        for k, v in my_files.items():
            file_list.append(v)
        file_dir, file_name = pm(file_list, op_file_name, ts)
        path = Path(file_dir + '/' + file_name)
        fs = FileSystemStorage()
        path = '/' + os.path.relpath(path, './media')
        fileurl = fs.url(path)
        return render(request, "pdfmanager/pdfmerge_download.html", {'fileurl': fileurl})


def pdf_split(request):
    return render(request, "pdfmanager/pdfsplit.html")


def pdf_split_show(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'pdf_split_img_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/pdf_split/{ts}/pdf/' + op_file_prefix + '.pdf', my_file)  # Arguments-> filename, file object
        res = pdf_to_image_low(fs.url(file),  f'/media/temp/pdf_split/{ts}/pdf' + op_file_prefix + '/', ts, 'pdf_split')

        ts = res[0]
        img_dir = res[1]
        img_rel = os.path.relpath(img_dir, '.')
        img_rel = '/' + img_rel + '/'
        # Read images and pass it to template for selection.
        img_list = [img_rel + p for p in os.listdir(img_dir)]
        img_list.sort()
        return render(request, "pdfmanager/pdfsplitshow.html", {'images': img_list, 'ts': ts})


def pdf_split_download(request):
    if request.method == 'POST':
        inp = request.POST
        images = inp.getlist('check')
        pages = [int(i.split(".")[0].split("/")[-1].split("_")[-1]) for i in images]
        pages.sort()
        ts = inp.getlist('timestamp')[0]
        inp_file = f'./media/temp/pdf_split/{ts}/pdf/' + os.listdir(f'./media/temp/pdf_split/{ts}/pdf')[0]
        op_dir = f'media/temp/pdf_split/{ts}/pdf/output'
        os.system(f"mkdir -p {op_dir}")
        fileurl = '/' + pdf_split_zip(inp_file, pages, op_dir)
        return render(request, "pdfmanager/pdfsplit_download.html", {'fileurl': fileurl})


def pdf_rotate(request):
    return render(request, "pdfmanager/pdfrotate.html")


def pdf_rotate_show(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'pdf_rotate_img_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/pdf_rotate/{ts}/pdf/'+ op_file_prefix + '.pdf', my_file)         # Arguments-> filename, file object
        res = pdf_to_image_low(fs.url(file),  f'/media/temp/pdf_rotate/{ts}/pdf' + op_file_prefix + '/', ts, 'pdf_rotate')

        ts = res[0]
        img_dir = res[1]
        img_rel = os.path.relpath(img_dir, '.')
        img_rel = '/' + img_rel + '/'
        # Read images and pass it to template for selection.
        img_list = [img_rel + p for p in os.listdir(img_dir)]
        img_list.sort()
        return render(request, "pdfmanager/pdfrotateshow.html", {'images': img_list, 'ts': ts})


def pdf_rotate_download(request):
    if request.method == 'POST':
        inp = request.POST
        angle = int(inp.getlist('rotate-angle')[0])
        pages = inp.getlist('check')
        ts = inp.getlist('timestamp')[0]
        all_img = [f'./media/temp/pdf_rotate/{ts}/images' + i for i in os.listdir(f'./media/temp/pdf_rotate/{ts}/images')]
        inp_file = f'./media/temp/pdf_rotate/{ts}/pdf/' + os.listdir(f'./media/temp/pdf_rotate/{ts}/pdf')[0]
        op_file = f'./media/temp/pdf_rotate/{ts}/pdf/output.pdf'
        with open(inp_file, 'rb') as f:
            pdf_rotate_selected(f, pages, op_file, angle)
        path = Path(os.path.abspath(op_file))
        fs = FileSystemStorage()
        path = '/' + os.path.relpath(path, './media')
        fileurl = fs.url(path)
        return render(request, "pdfmanager/pdfrotate_download.html", {'fileurl': fileurl})


def pdf_extract(request):
    return render(request, "pdfmanager/pdfextract.html")


def pdf_extract_show(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'pdf_extract_img_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/pdf_extract/{ts}/pdf/' + op_file_prefix + '.pdf',
                       my_file)  # Arguments-> filename, file object
        res = pdf_to_image_low(fs.url(file), f'/media/temp/pdf_extract/{ts}/pdf' + op_file_prefix + '/', ts, 'pdf_extract')

        ts = res[0]
        img_dir = res[1]
        img_rel = os.path.relpath(img_dir, '.')
        img_rel = '/' + img_rel + '/'
        # Read images and pass it to template for selection.
        img_list = [img_rel + p for p in os.listdir(img_dir)]
        img_list.sort()
        return render(request, "pdfmanager/pdfextractshow.html", {'images': img_list, 'ts': ts})


def pdf_extract_download(request):
    if request.method == 'POST':
        inp = request.POST
        pages = inp.getlist('check')
        ts = inp.getlist('timestamp')[0]
        all_img = [f'./media/temp/pdf_extract/{ts}/images' + i for i in os.listdir(f'./media/temp/pdf_extract/{ts}/images')]
        inp_file = f'./media/temp/pdf_extract/{ts}/pdf/' + os.listdir(f'./media/temp/pdf_extract/{ts}/pdf')[0]
        op_file = f'./media/temp/pdf_extract/{ts}/pdf/output.pdf'
        with open(inp_file, 'rb') as f:
            pdfextract(f, pages, op_file)
        path = Path(os.path.abspath(op_file))
        fs = FileSystemStorage()
        path = '/' + os.path.relpath(path, './media')
        fileurl = fs.url(path)
        return render(request, "pdfmanager/pdfextract_download.html", {'fileurl': fileurl})


def pdf_encrypt(request):
    ts = str(int(round(datetime.now().timestamp())))

    if request.method == 'POST':
        file_name = request.FILES['inputFile'].name
        inp = request.POST
        passwd = inp['inputGroupPasswd']
        my_file = list(request.FILES.values())[0]
        op_dir = f'./media/temp/pdf_encrypt/{ts}/'
        os.system(f'mkdir -p {op_dir}')
        output_pdf = file_name.split(".")[0] + '_encrypted.pdf'
        file_path = op_dir + output_pdf
        if pdf_add_password(my_file, passwd, file_path):
            path = Path(file_path)
            fs = FileSystemStorage()
            path = '/' + os.path.relpath(path, './media')
            fileurl = fs.url(path)
            return render(request, "pdfmanager/pdfencrypt_download.html", {'fileurl': fileurl})
    return render(request, "pdfmanager/pdfencrypt.html")


def pdf_decrypt(request):
    ts = str(int(round(datetime.now().timestamp())))
    if request.method == 'POST':
        file_name = request.FILES['inputFile'].name
        inp = request.POST
        passwd = inp['inputGroupPasswd']
        my_file = list(request.FILES.values())[0]
        op_dir = f'./media/temp/pdf_decrypt/{ts}/'
        os.system(f'mkdir -p {op_dir}')
        output_pdf = file_name.split(".")[0] + '_decrypted.pdf'
        file_path = op_dir + output_pdf
        if pdf_remove_password(my_file, passwd, file_path):
            path = Path(file_path)
            fs = FileSystemStorage()
            path = '/' + os.path.relpath(path, './media')
            fileurl = fs.url(path)
            return render(request, "pdfmanager/pdfdecrypt_download.html", {'fileurl': fileurl})
    return render(request, "pdfmanager/pdfdecrypt.html")

def pdf_watermark(request):
    return render(request, "pdfmanager/pdfwatermark.html")


def pdf_info(request):
    return render(request, "pdfmanager/pdfinfo.html")


def convert_from_pdf(request):
    return render(request, "pdfmanager/convertfrompdf.html")


def pdf_to_jpg(request):
    return render(request, "pdfmanager/pdftojpg.html")


def pdf_to_jpg_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'pdf_to_jpg_img_' + ts
    quality = 'High'
    print(request.FILES)
    print(request.POST)
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/convert_from_pdf/{ts}/pdf/' + op_file_prefix + '.pdf', my_file)  # Arguments-> filename, file object
        img_dir = base_dir + f'/media/temp/convert_from_pdf/{ts}/jpg/'
        os.system(f"mkdir -p {img_dir}")
        res = pdf_to_image(fs.url(file), img_dir + op_file_prefix, quality, 'jpg')
        fileurl = '/' + os.path.relpath(img_dir, '.') + '/' + res.split('/')[-1]
        return render(request, "pdfmanager/pdftojpg_download.html", {'fileurl': fileurl})


def pdf_to_png(request):
    return render(request, "pdfmanager/pdftopng.html")


def pdf_to_png_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'pdf_to_png_img_' + ts
    quality = 'High'
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/convert_from_pdf/{ts}/pdf/' + op_file_prefix + '.pdf', my_file)  # Arguments-> filename, file object
        img_dir = base_dir + f'/media/temp/convert_from_pdf/{ts}/png/'
        os.system(f"mkdir -p {img_dir}")
        res = pdf_to_image(fs.url(file), img_dir + op_file_prefix, quality, 'png')
        fileurl = '/' + os.path.relpath(img_dir, '.') + '/' + res.split('/')[-1]
        return render(request, "pdfmanager/pdftopng_download.html", {'fileurl': fileurl})


def pdf_to_word(request):
    return render(request, "pdfmanager/pdftoword.html")


def pdf_to_word_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'pdf_to_word_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/convert_from_pdf/{ts}/pdf/' + op_file_prefix + '.pdf', my_file)
        #res = pdf_to_image_low(fs.url(file), f'/media/temp/pdf_split/{ts}/pdf' + op_file_prefix + '/', ts, 'pdf_split')
        op_dir = f'media/temp/convert_from_pdf/{ts}/word'
        os.system(f"mkdir -p {op_dir}")
        op_file = op_dir + '/' + op_file_prefix + '.docx'
        convert_pdf_to_word('./' + fs.url(file), op_dir + '/' + op_file_prefix + '.docx')
        fileurl = '/' + op_file
        return render(request, "pdfmanager/pdftoword_download.html", {'fileurl': fileurl})


def convert_to_pdf(request):
    return render(request, "pdfmanager/converttopdf.html")


def jpg_to_pdf(request):
    return render(request, "pdfmanager/jpgtopdf.html")


def jpg_to_pdf_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'jpg_to_pdf_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/convert_to_pdf/{ts}/jpg/' + op_file_prefix + '.jpg', my_file)  # Arguments-> filename, file object
        print(file)
        pdf_dir = base_dir + f'/media/temp/convert_to_pdf/{ts}/pdf/'
        os.system(f"mkdir -p {pdf_dir}")
        res = image_to_pdf(fs.url(file), pdf_dir + op_file_prefix + '.pdf')
        fileurl = '/' + os.path.relpath(pdf_dir, '.') + '/' + res.split('/')[-1]
        return render(request, "pdfmanager/jpgtopdf_download.html", {'fileurl': fileurl})


def png_to_pdf(request):
    return render(request, "pdfmanager/pngtopdf.html")


def png_to_pdf_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'png_to_pdf_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        fs = FileSystemStorage()
        file = fs.save(f'temp/convert_to_pdf/{ts}/png/' + op_file_prefix + '.png', my_file)  # Arguments-> filename, file object
        print(file)
        pdf_dir = base_dir + f'/media/temp/convert_to_pdf/{ts}/pdf/'
        os.system(f"mkdir -p {pdf_dir}")
        res = image_to_pdf(fs.url(file), pdf_dir + op_file_prefix + '.pdf')
        fileurl = '/' + os.path.relpath(pdf_dir, '.') + '/' + res.split('/')[-1]
        return render(request, "pdfmanager/pngtopdf_download.html", {'fileurl': fileurl})


def word_to_pdf(request):
    return render(request, "pdfmanager/wordtopdf.html")


def word_to_pdf_download(request):
    ts = str(int(round(datetime.now().timestamp())))
    op_file_prefix = 'word_to_pdf_' + ts
    if request.method == 'POST':
        my_file = list(request.FILES.values())[0]
        print(my_file.name.split(".")[1])
        fs = FileSystemStorage()
        file = fs.save(f'temp/convert_to_pdf/{ts}/doc/' + op_file_prefix + '.' + my_file.name.split(".")[1], my_file)
        op_dir = f'media/temp/convert_to_pdf/{ts}/word'
        os.system(f"mkdir -p {op_dir}")
        op_file = op_dir + '/' + op_file_prefix + '.pdf'
        #convert_word_to_pdf('./' + fs.url(file), op_file)
        fileurl = '/' + op_file
        return render(request, "pdfmanager/wordtopdf_download.html", {'fileurl': fileurl})

# def pdf_view(request):
#     try:
#         return FileResponse(open('/Users/rohitmac/MyMAC/Projects/repo/pdfproject/pdf_project/output/pdfmerge/pdf_merge_1653327541.pdf', 'rb'), content_type='application/pdf')
#     except FileNotFoundError:
#         raise Http404()