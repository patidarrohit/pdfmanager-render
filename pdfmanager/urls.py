from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('pdfmerge/', views.pdf_merge, name='pdfmerge'),
    path('pdfmergedownload/', views.pdf_merge_download, name='pdfmergedownload'),

    path('pdfsplit/', views.pdf_split, name='pdfsplit'),
    path('pdfsplitshow/', views.pdf_split_show, name='pdfsplitshow'),
    path('pdfsplitdownload/', views.pdf_split_download, name='pdfsplitdownload'),

    path('pdfrotate/', views.pdf_rotate, name='pdfrotate'),
    path('pdfrotateshow/', views.pdf_rotate_show, name='pdfrotateshow'),
    path('pdfrotatedownload/', views.pdf_rotate_download, name='pdfrotatedownload'),

    path('pdfextract/', views.pdf_extract, name='pdfextract'),
    path('pdfextractshow/', views.pdf_extract_show, name='pdfextractshow'),
    path('pdfextractdownload/', views.pdf_extract_download, name='pdfextractdownload'),

    path('pdfwatermark/', views.pdf_watermark, name='pdfwatermark'),
    path('pdfinfo/', views.pdf_info, name='pdfinfo'),

    path('pdfencrypt/', views.pdf_encrypt, name='pdfencrypt'),
    path('pdfdecrypt/', views.pdf_decrypt, name='pdfdecrypt'),

    path('convertfrompdf/', views.convert_from_pdf, name='convertfrompdf'),
    path('pdftojpg/', views.pdf_to_jpg, name='pdftojpg'),
    path('pdftojpgdownload/', views.pdf_to_jpg_download, name='pdftojpgdownload'),
    path('pdftopng/', views.pdf_to_png, name='pdftopng'),
    path('pdftopngdownload/', views.pdf_to_png_download, name='pdftopngdownload'),
    path('pdftoword/', views.pdf_to_word, name='pdftoword'),
    path('pdftoworddownload/', views.pdf_to_word_download, name='pdftoworddownload'),

    path('converttopdf/', views.convert_to_pdf, name='converttopdf'),
    path('jpgtopdf/', views.jpg_to_pdf, name='jpgtopdf'),
    path('jpgtopdfdownload/', views.jpg_to_pdf_download, name='jpgtopdfdownload'),
    path('pngtopdf/', views.png_to_pdf, name='pngtopdf'),
    path('pngtopdfdownload/', views.png_to_pdf_download, name='pngtopdfdownload'),
    path('wordtopdf/', views.word_to_pdf, name='wordtopdf'),
    path('wordtopdfdownload/', views.word_to_pdf_download, name='wordtopdfdownload'),

]