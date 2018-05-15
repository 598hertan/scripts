#!/usr/bin/python35

"""
Author: James Hertan
Date:   09/25/2017

DESCRIPTION:
Generic methods for scraping websites.

"""

import bs4, requests, os
from os import listdir, makedirs
import json
from os.path import join, isfile

#--------WEB SCRAPING-----------
def get_soup(url, local_file=''):
    """input a url, output its soup by saving the HTML as a text file in cwd"""

    if local_file == '':
        temp_file = save_HTML(url)          #COMMENT THIS OUT to use the cached temp file
    else:
        temp_file = local_file     #Comment this to generate a new temp file

    html = create_text_file(temp_file)
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup
def save_HTML(url, temp_filename=''):
    # retrieve HTML as text from a URL, return the filename of the txt file created
    r = requests.get(url)
    r.raise_for_status()

    path = os.getcwd()
    target_directory_name = join(path, 'temp')

    if temp_filename == '':
        temp_filename = str(url.split('.')[1]) + '.txt'
        temp_filename = join(target_directory_name, temp_filename)

    success_message = "Temp file '{}' created!".format(temp_filename)

    try:
        with open(temp_filename, 'wb') as fn:
            for chunk in r.iter_content(100000):
                fn.write(chunk)
    except FileNotFoundError as e:
        makedirs(target_directory_name)
        save_HTML(url)
    else:
        print(success_message)
    return temp_filename
def create_text_file(file):
    """input file, outputs reading of file"""
    with open(file, 'r', encoding='utf-8') as fn:
        return fn.read()
def get_text_from_selection(soup_selection_body):
        """input a soup selection, return its text as a string"""
        body_text = []
        for i in soup_selection_body:
            body_text.append(i.getText())
        return ', '.join(body_text)

#TODO Write get_links(soup_selection_a)
#--------END WEB SCRAPING-----------

#--------API Scripts-----------
###  Access
def get_key(filename):
    '''Retrieve the API key from a key file'''
    with open(filename, 'r') as fn:
        key = fn.readline()
        return (key)

###  Read
def convert_file_to_json(txt_file):
    '''Pass a filename, converts the file's text to a JSON object. Returns the JSON object, 0 if something went wrong.'''
    try:
        with open(txt_file, 'r') as fn:
            data = json.loads(fn.read())
            return data
    except FileNotFoundError as e:
        print("File does not exist.")
        return 0

###  Write
def save_data(data, filename='data.txt'):
    '''Save data to a txt file. Data is converted to a string. Output is a new file.'''
    with open(filename, 'w') as fn:
        fn.write(json.dumps(data))

###  Update
#TODO Write save_scrape_to_JSON()

###  Delete
#--------END API Scripts-----------



#--------PDF Scripts-----------
def save_pdf_from_url(pdf_url, target_directory_name=''):
    """input the url of the pdf file to download, file saves to a 'PDF' folder in cwd unless a path is identified"""
    filename = get_PDF_fn(pdf_url)

    if '.pdf' not in filename:
        filename = 'temp.pdf'

    path = os.getcwd()

    if target_directory_name == '':
        target_directory_name = join(path, 'PDF')

    try:
        loose_files = [file for file in listdir(target_directory_name) if isfile(join(target_directory_name, file))]

        if filename in loose_files:
            print("'{}' already exists on your hard-drive at '{}'.\nEnd program.".format(filename, target_directory_name))
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
            save_pdf_from_url(pdf_url, target_directory_name)
    else:
        pass
def get_PDF_fn(url):
    '''helper function for save_pdf(), provide the magpiPDF url to determine the pdf name'''
    name = url.split('/')[4]
    return name
#--------END PDF Scripts-----------


#--------Printing Scripts-----------
def pretty_print(self, label, value, adjust=15):
    '''Helper function for print_data() to print nicely'''
    print(label.ljust(adjust), value)
#--------END Printing-----------




def main():

    # url = 'http://www.kissmywhisk.com'
    url = 'https://www.raspberrypi.org/magpi/'
    soup = get_soup(url)
    print(type(soup))


    # url = 'http://econpy.pythonanywhere.com/ex/001.html'
    # soup = get_soup(url)
    # urls = (soup.select('a'))
    # print(len(soup.select('a')))
    #
    # for link in urls:
    #     print(link.get('href'))

if __name__ == "__main__": main()
