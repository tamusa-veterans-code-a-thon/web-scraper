# web scraper for getting information on veteran certified businesses in San Antonio
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

# if csv file doesnt exist create one

def first_page():
    # getting url setup
    my_url = "https://vetbiz.va.gov/advancedsearch/searchresults/?id=61468e1e-12bb-eb11-89ee-0003ff00655b&page=1&source=VIPAdvancedSearch&records=250"
    client = uReq(my_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")

    # generic placement of items on chrome inspect
    containers = page_soup.findAll("div",{"class":"col-sm-12 col-lg-12"})

    # creating the csv file
    #filename = "Veteran Businesses Information.csv"
    #f = open(filename, 'w')

    # write headers on excel file
    #headers = "Business Name"
    #f.write(headers)

    # for loop to find profile details link for each business
    for container in containers:
        detail_link = container.a["href"]
        detail_link = 'https://vetbiz.va.gov' + detail_link
        second_page(detail_link)

def second_page(detail_link):
    # url information setup
    my_url = detail_link
    client = uReq(my_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")

    # generic placement of items on chrome inspect
    containers = page_soup.findAll("div", {"class": "table-responsive"})

    # for loop to add content into the csv file in rows
    for container in containers:
        headerH2 = container.h2.contents # list
        name = headerH2[0]
        DUNS = headerH2[2].contents # DUNS: 080750233
        email = headerH2[4].a["href"] # mailto:david@1CS.Business it works in emails this way
        # web = headerH2[4].div.div.a.a  # problems getting into the correct 'a' as there are 2 of them in the same tag
        # print(web)


        # read div for ncis code
            # drop 'ncis code:'
            # split text into list
            # send list to => business_type(listOfCodes)
            # listOfCode -> then put into .csv


# def business_type(listOfCodes):
    #filename = "categories.csv"
    #open
    #read
    #put into dict (numbers and strings)


    #listOfCodes
    # loop through list of codes
    # if code == key
        # replace code with value (string) from dict

    #return listOfCodes
first_page()