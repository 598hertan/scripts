__author__ = 'JHertan'
#November, 5, 2015

from bs4 import BeautifulSoup   #http://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree
import urllib.request           #for opening a web page and saving it as html file
import os                       #for deleting my temp html files
from csv import writer          #for writing a csv file with output data

class ExtractHtml():
    """
    Extract the HTML code from a URL and save it as an html file
    Input: URL of webpage html to save
    Optional Input: Use 'target_filename' to identify a preferred name of the html file that will be generated
    Output: html file of the page's source html code
    """
    def __init__(self, source, target_filename='extracted_html.html'):
        self.html = target_filename
        # print("Enter the web page name:\n>>> ")
        # url=input()

        url = str(source)
        html = urllib.request.urlopen(url)
        data = html.read()

        with open(self.html, "wb+") as file:   #generate an html_file
            file.write(data)

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, target):
        self._html = target

    @html.deleter
    def html(self):
        os.remove(self._html)

class Extract_HTML_Links():
    """
    Finds all links ('a') based on a given "source" URL

    Input: source URL for searching
    Optional Input: criteria as a string.   Ex: '/news' to extract links with '/news' within the url string
    Output: object as an iterable list of URLs
    """
    def __init__(self, source, criteria=None):
        has_criteria = False
        if criteria != None:
            has_criteria = True
            self.filter = criteria
        self.url = source
        self.other_pages = list()
        page = ExtractHtml(self.url)
        soup = BeautifulSoup(open(page.html, 'r'), 'html.parser')

        #link_limit = 5                             #create a limit variable (int) to limit the amount of links saved

        if has_criteria:
            for link in soup.find_all('a'):   #Use link limit like this:    soup.find_all('a', limit=link_limit)
                if str(self.filter) in str(link) and link.get('href') not in self.other_pages:
                    self.other_pages.append(link.get('href'))
                else:
                    continue
        else:
            for link in soup.find_all('a'):
                self.other_pages.append(link.get('href'))
            self.other_pages.insert(0, source)
        os.remove(page.html)


    def __iter__(self):                     #makes the ExtractLinks object an iterator
        for link in self.other_pages:
            yield link

    def __str__(self):
        intro = "From '{}', here are the 'a' hrefs identified:\n".format(self.url)
        return intro + '\n'.join(self.other_pages)

def main():
    csv_output = 'transactions.csv'                                                   #saves the output data here
    url_list = Extract_HTML_Links('http://econpy.pythonanywhere.com/ex/001.html', criteria='ex/002')         #finds all links for the given URL  #can use link_name_criteria to filter the list of links generated based on the string entered
    print(url_list)
    print('\n')

    print("Processing", end="")
    for url in url_list:
        print(".", end="")
        page = ExtractHtml(url, 'econ.html')                      #Object instantiated with all 'a' hrefs from the HTML code within each url identified in url_list

        soup = BeautifulSoup(open(page.html, 'r'), 'html.parser')           #makes a temporary soup file for reading through the html of information

        #*******************************************************************
        #Hard-coded below is code to generate data based on what you want
        #Example for 'http://econpy.pythonanywhere.com/ex/001.html' will generate buyer and price data
        #************START Hard-coded Logic*********************************
        buyers = (soup.find_all(attrs={"title": "buyer-name"}))
        prices = (soup.find_all(attrs={"class": "item-price"}))
        buyer_list, prices_list = list(), list()
        transaction_data = []
        for buyer in buyers:                                                #cleans up the data
            buyer_list.append(str(buyer).split('>', 1)[1].split('<')[0])
        for price in prices:   #print(soup.select(".item-price"))           #cleans up the data
            prices_list.append(str(price).split('>', 1)[1].split('<')[0])
        for tran in zip(buyer_list, prices_list):                           #generates data based on the html file and the search criteria
            transaction_data.append(", ".join(tran))
        #************END Hard-coded Logic*********************************

        output = writer(open(csv_output,'a+', newline='\n'), delimiter=',')

        for transaction in transaction_data:                #appends the data to the csv_output
            name, price = transaction.split(',')
            output.writerow([name, price])

        del page.html                           #calls the deleter decorator to remove the temporary file


    print('\n')
    print("File '{}' created successfully".format(csv_output))

if __name__ == "__main__":
    main()
