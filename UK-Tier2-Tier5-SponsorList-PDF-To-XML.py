__author__ = 'somdipdey'

import urllib.request
from lxml import etree
import os
from io import open
import sys


def download_pdf_file(url):
    pdfdata = urllib.request.urlopen(url).read()
    f = open(r'original.pdf', 'wb')
    f.write(pdfdata)

    
''' Repair a PDF’s corrupted XREF table and stream lengths, if possible '''
def fix_pdf_file_format():
    cmd = 'pdftk original.pdf output fixedFormat.pdf'
    cmd += " >/dev/null 2>&1"
    os.system(cmd)

    
def pdftoxml(pdfdata):
    import tempfile

    """converts pdf file to xml file"""
    pdffout = tempfile.NamedTemporaryFile(suffix='.pdf')
    pdffout.write(pdfdata)
    pdffout.flush()

    xmlin = tempfile.NamedTemporaryFile(mode='r', suffix='.xml')
    tmpxml = xmlin.name  # "temph.xml"
    cmd = 'pdftohtml -xml -zoom 1.5 -enc UTF-8 -noframes "%s" "%s"' % (pdffout.name, os.path.splitext(tmpxml)[0])
    cmd += " >/dev/null 2>&1"  # can't turn off output, so throw away even stderr yeuch
    os.system(cmd)

    pdffout.close()
    # xmlfin = open(tmpxml)
    xmldata = xmlin.read()
    xmlin.close()
    return xmldata


def main(url):
    download_pdf_file(url)
    print(">>PDF from url downloaded")
    fix_pdf_file_format()
    print(">>Fixed the XREF table of PDF (if corrupted) before converting to XML")

    pdfdata = open(r'fixedFormat.pdf', 'rb').read()
    print(">>pdfdata read")
    xmldata = pdftoxml(pdfdata)
    #pypdfx(r'original.pdf')
    print(">>PDF to XML Conversion complete")

''' 
    For main(url), provide the current url of latest PDF sponsor list as the parameter
'''
if __name__ == '__main__': main(r'https://www.gov.uk/government/uploads/system/uploads/attachment_data/file/671998/2018-01-05_Tier_2_5_Register_of_Sponsors.pdf')
