import csv, time, requests
from selenium import webdriver
from bs4 import BeautifulSoup

start_url = 'https://exoplanets.nasa.gov/discovery/exoplanet-catalog/'

browser=webdriver.Chrome('chromedriver.exe')
browser.get(start_url)
time.sleep(10)

headers = [
    'Name',
    'Lightyears from Earth',
    'Mass',
    'Stellar Magnitude',
    'Discovery Date',
    'Hyperlink',
    'Planet Type', 
    'Planet Radius', 
    'Orbital Radius',
    'Orbital Period',
    'Eccentricity'
]

planet_data = []

def scrape():
    for i in range(0, 201):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        for ul_tag in soup.find_all('ul', attrs={'class','exoplanet'}):
            li_tags = ul_tag.find_all('li')
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if(index == 0):
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append('')
            hyperlink_li_tag = li_tags[0]
            temp_list.append('https://exoplanets.nasa.gov'+hyperlink_li_tag.find_all('a', href=True)[0]['href'])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/div[1]/div[2]/div[1]/div/nav/span[2]/a').click()

def scrape_more(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp = []
        for tr in soup.find_all('tr', attrs={'class': 'fact_row'}):
            td = tr.find_all('td')
            temp = []
            for i in td:
                try:
                    temp.append(i.find_all('div', attrs={'class': 'value'})[0].contents[0])
                except:
                    temp.append('')
            planet_data.append(temp)
    except:
        time.sleep(1)

print('scraping')

scrape()


for index, data in enumerate(planet_data):
    scrape_more(data[5])
    print(f'{index+1} page done')


final_planet_data = []

for index, data in enumerate(planet_data):
    final_planet_data.append(data+final_planet_data[index])

print('writing to csv...')

with open('planets.csv', 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)

print('done!')
                    
