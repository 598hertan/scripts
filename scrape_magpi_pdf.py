#!/usr/bin/python35

"""
Author: James Hertan
Date:   09/23/2017

DESCRIPTION:
Download MagPi magazine file.
Assumes that from the soup, the file is located at soup.select('div > .col-xs-12 a')[5]

"""
import bs4, requests, os
from os import listdir, makedirs
from os.path import join, isfile

def get_soup(url):
    """input a url, save the HTML as a text file in cwd, output its soup"""

    # temp_file = get_html(url)          #COMMENT THIS OUT to use the cached temp file
    temp_file = save_HTML(url)          #COMMENT THIS OUT to use the cached temp file
    # temp_file = 'raspberrypi.txt'     #UNCOMMENT THIS to use the cached temp file

    html = get_text_from_file(temp_file)
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup
def save_HTML(url, temp_filename=''):
    # retrieve HTML as text from a URL, return the txt file created
    r = requests.get(url)
    r.raise_for_status()

    if temp_filename == '':
        temp_filename = str(url.split('.')[1]) + '.txt'

    success_message = "Temp file '{}' created!".format(temp_filename)

    with open(temp_filename, 'wb') as fn:
        for chunk in r.iter_content(100000):
            fn.write(chunk)

    print(success_message)
    return temp_filename
def get_text_from_file(file):
    """input file, outputs reading of file"""
    with open(file, 'r', encoding='utf-8') as fn:
        return fn.read()

def get_pdf_url(soup):
    '''get the PDF url for the magpi mag'''

    link_tag = (soup.select('div > .col-xs-12 a')[5])
    pdf_url = (link_tag.get('href'))

    return pdf_url

def save_pdf(pdf_url, target_directory_name=''):
    filename = get_PDF_fn(pdf_url)

    if '.pdf' not in filename:
        print("This program failed to identify where the PDF file is. Please inspect the html element and update the code.\nEnd program.")
        quit()

    path = os.getcwd()

    if target_directory_name == '':
        target_directory_name = join(path, 'magpi')

    try:
        loose_files = [file for file in listdir(target_directory_name) if isfile(join(target_directory_name, file))]

        if filename in loose_files:
            print("{} already exists on your hard-drive at '{}\{}'\nEnd program.".format(filename, path, target_directory_name))
        else:
            print("The PDF file '{}' is downloading to {}. This may take a minute or so...".format(filename, target_directory_name))
            response = requests.get(pdf_url)
            pdf_file = open(os.path.join(target_directory_name, os.path.basename(filename)), 'wb')

            # write to disk
            for chunk in response.iter_content(100000):
                pdf_file.write(chunk)
            pdf_file.close()

            print("\nPDF file '{}' has been saved!".format(filename))
    except (FileNotFoundError) as e:
            print("The target directory doesn't exist.\n{}\nCreating directory '{}'.".format(e, target_directory_name))
            makedirs(target_directory_name)
            save_pdf(pdf_url, target_directory_name)
    else:
        pass
def get_PDF_fn(url):
    '''helper function for save_pdf(), provide the magpiPDF url to determine the pdf name'''
    name = url.split('/')[4]
    return name


def main():
    url = 'https://www.raspberrypi.org/magpi/'
    soup = get_soup(url)
    pdf_url = get_pdf_url(soup)
    save_pdf(pdf_url, 'magpi')

if __name__ == "__main__": main()
