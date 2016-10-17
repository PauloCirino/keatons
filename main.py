from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

import selenium.common.exceptions
import csv

link = 'http://www.keatons.com/search-property-display'


class PropertyScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(10)
        self.driver.set_window_size(1280, 900)

    def scrape_properties(self):
        self.driver.get(link)
        properties = []

        select_list = self.driver.find_element_by_xpath("//div[@class='list-button']/a[1]")
        select_list.click()
        sleep(5)

        more_items_button = self.driver.find_element_by_xpath("//div[@class='properties']/p/a[4]")
        more_items_button.click()
        sleep(5)

        while True:
            s = BeautifulSoup(self.driver.page_source, "html.parser")

            for a in s.find_all('div', class_='property-holder'):
                property = dict()

                property['price'] = a.find('h4', class_='price').find_all('span')[1].contents[0]
                property['bedrooms'] = a.find('div', class_='icons').find('div', class_='bedrooms').find('p').contents[0].strip()
                property['reception'] = a.find('div', class_='icons').find('div', class_='reception-rooms').find('p').contents[0].strip()
                property['bathrooms'] = a.find('div', class_='icons').find('div', class_='bathrooms').find('p').contents[0].strip()
                property['garden'] = a.find('div', class_='icons').find('div', class_='garden').find('p').contents[0].strip()
                property['car'] = a.find('div', class_='icons').find('div', class_='car').find('p').contents[0].strip()
                property['station'] = a.find('div', class_='icons').find('div', class_='station').find('p').contents[0].strip()
                property['rail'] = a.find('div', class_='icons').find('div', class_='rail').find('p').contents[0].strip()
                property['epc'] = a.find('div', class_='icons').find('div', class_='epc').find('p').contents[0].strip()

                if len(a.find('span', class_='road-name').contents) > 0:
                    property['street'] = a.find('span', class_='road-name').contents[0]
                else:
                    property['street'] = "Not Available"

                properties.append(property)

            next_button_soup = s.find_all('a', class_='next')

            if len(next_button_soup) != 0:
                try:
                    next_button = self.driver.find_element_by_class_name('next')
                    next_button.click()
                    sleep(5)
                except selenium.common.exceptions.NoSuchElementException:
                    break
            else:
                break

        return properties

    def scrape(self):
        properties = self.scrape_properties()

        with open("keatons.csv", 'w') as csvfile:
            field_names = ['street', 'price', 'bedrooms', 'reception', 'bathrooms', 'garden', 'car', 'station', 'rail', 'epc']
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()

            for data in properties:
                writer.writerow(data)

        self.driver.quit()


if __name__ == '__main__':
    scraper = PropertyScraper()
    scraper.scrape()