# web scraper for getting information on veteran certified businesses in San Antonio
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import pandas as pd

# filename = "Veteran Businesses Information.csv"
# f = open(filename, 'w')
# headers = "Business Name, DUNS, Email, Website, Last Verified, Expiration Date, Year Established, Address1, " \
#           "Address2, City, State, Phone, Fax, NAICS Codes, Disabled Veteran Owned, Women Owned, Minority Owned\n"
# f.write(headers)

def first_page():
    # getting url setup
    my_url = "https://vetbiz.va.gov/advancedsearch/searchresults/?id=61468e1e-12bb-eb11-89ee-0003ff00655b&page=1&source=VIPAdvancedSearch&records=250"
    client = uReq(my_url)
    page_html = client.read()
    client.close()
    page_soup = soup(page_html, "html.parser")

    # generic placement of items on chrome inspect
    containers = page_soup.findAll("div",{"class":"col-sm-12 col-lg-12"})
    company_types = pd.read_csv("business_categories.csv")
    company_dict = dict(zip(company_types.Code, company_types["Industry Title"]))

    # csv headers
    filename = "Veteran Businesses Information.csv"
    f = open(filename, 'w')
    headers = "Business Name, DUNS, Email, Website, Last Verified, Expiration Date, Year Established, Address1, " \
              "Address2, City, State, Phone, Fax, NAICS Codes, Disabled Veteran Owned, Women Owned, Minority Owned\n"
    f.write(headers)

    # for loop to find profile details link for each business
    for container in containers:
        detail_link = container.a["href"]
        detail_link = 'https://vetbiz.va.gov' + detail_link
        second_page(detail_link, company_dict, f)
    f.close()


def second_page(detail_link, company_dict, f):
    # filename = "Veteran Businesses Information.csv"
    # f = open(filename, 'w')
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
        web = headerH2[4].findAll("a")[1]["href"]  # some are empty bc they have no website

        # business information portion LEFT COLUMN DATES
        businessDiv = container.find("div", {"id":"businessinfo-column"}) # general placement of div
        dates = businessDiv.contents[5] # general locations for div contents for verification dates
        allDates = dates.contents # list of correct div information over verification
        lastVer = allDates[3].contents
        expiration = allDates[5].contents
        established = allDates[7].contents

        # business information RIGHT COLUMN LOCATION/FAX
        basicInfo = businessDiv.contents[7] # general location for address, fax, phone, city, state information
        basicList = basicInfo.contents # list of above information ^^^
        add1 = basicList[1].contents
        add2 = basicList[3].contents
        city = basicList[5].contents
        state = basicList[7].contents
        phone = basicList[9].contents
        fax = basicList[11].contents

        # removing commas from name and addresses
        name = str(name).replace(',','')
        add1 = str(add1).replace(',','')
        add2 = str(add2).replace(',','')

        # business type section
        codeDiv = container.find("div", {"id":"businesstype-column"}) # general location of div for business type
        codeLoc = codeDiv.contents[5] # general location for NAICS codes
        codes = codeLoc.contents # list of code column
        tempt = str(codes[5].contents)
        NAICS = tempt.split(' ')
        NAICS = NAICS[2:]
        NAICS = [i.strip(',]\'_a_Except') for i in NAICS]
        tuple = set(NAICS)

        types = set()

        for t in tuple:
            cat = business_type(t, company_dict)
            types.add(cat)

        types = str(types).replace(',','')

        # business type RIGHT COLUMN disabled/women/minority
        status = codeDiv.contents[7] # general location of information
        statusList = status.contents # list of the above information
        disabled = str(statusList[1].contents)
        disabled = disabled.split(':')
        disabled = disabled[1:]
        disabled = [i.strip('\\n ') for i in disabled]
        disabled = str(disabled)[2:5].strip('\\')
        women = str(statusList[3].contents)
        women = women.split(':')
        women = women[1:]
        women = [i.strip('\\n ') for i in women]
        women = str(women)[2:5].strip('\\')
        minority = str(statusList[5].contents)
        minority = minority.split(':')
        minority = minority[1:]
        minority = [i.strip('\\n ') for i in minority]
        minority = str(minority)[2:5].strip('\\')

        # convert into booleans
        disabled_B = False
        women_B = False
        minority_B = False

        if disabled == 'Yes':
            disabled_B = True
        if women == 'Yes':
            women_B = True
        if minority == 'Yes':
            minority_B = True


        # add info to csv, true/false all caps
        f.write(str(name)+","+str(DUNS)+","+str(email)+","+str(web)+","+str(lastVer)+","+str(expiration)+","+str(established)+","+str(add1)+","+str(add2)+","+str(city)+","+str(state)+","+str(phone)+","+str(fax)+","+types+","+str(disabled_B)+","+str(women_B)+","+str(minority_B)+"\n")


def business_type(t, company_dict):

    t = t[0]+t[1]
    t = int(t)

    for k in company_dict:
        if k == t:
            return company_dict[k]

first_page()