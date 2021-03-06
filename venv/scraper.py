# web scraper for getting information on veteran certified businesses in San Antonio
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
def first_page ():
    # getting url setup
    my_url = "https://vetbiz.va.gov/advancedsearch/searchresults/?id=61468e1e-12bb-eb11-89ee-0003ff00655b&page=1&source=VIPAdvancedSearch&records=250"
    client = uReq(my_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")

    # generic placement of items on chrome inspect
    containers = page_soup.findAll("tr",{"class":"col-sm-12 col-lg-12"})

    # creating the csv file
    #filename = "Veteran Businesses Information.csv"
    #f = open(filename, 'w')

    # write headers on excel file
    #headers = "Business Name"
    #f.write(headers)

    # for loop to add content into the csv file in rows
    for container in containers:
        detail_link = container.a["href"]
        detail_link = 'https://vetbiz.va.gov' + detail_link
        second_page(detail_link)

def second_page(detail_link):
    my_url = detail_link
    client = uReq(my_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")

    # generic placement of items on chrome inspect
    containers = page_soup.findAll("tr", {"class": "col-sm-12 col-lg-12"})

    # creating the csv file
    filename = "Veteran Businesses Information.csv"
    f = open(filename, 'w')

    # write headers on excel file
    headers = "Business Name"
    f.write(headers)

    # for loop to add content into the csv file in rows
    for container in containers:

        # read div for ncis code
            # drop 'ncis code:'
            # split text into list
            # send list to => business_type(listOfCodes)
            # listOfCode -> then put into .csv

        detail_link = container.a["href"]
        print(detail_link)

def business_type(listOfCodes):
    filename = "categories.csv"
    #open
    #read
    #put into dict (numbers and strings)


    #listOfCodes
    # loop through list of codes
    # if code == key
        # replace code with value (string) from dict

    return listOfCodes