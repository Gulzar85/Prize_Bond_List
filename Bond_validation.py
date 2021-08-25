import scrapy
import pandas as pd
from urllib.request import urlopen
from datetime import date
import re


def read_excel():
    df = pd.read_excel('Rs750_Bonds.xlsx')
    return df['Bonds'].values.tolist()


class BondValidationSpider(scrapy.Spider):
    name = 'Bond_validation'
    allowed_domains = ['savings.gov.pk']
    start_urls = ['http://savings.gov.pk/rs-750-draws/']

    def parse(self, response):
        for link in response.css('#middle a::attr(href)').getall():
            yield response.follow(link, callback=self.parse_bonds)

    def parse_bonds(self, response):
        # declare list to store prize bonds
        prize_list = list()
        # open link to read
        link = urlopen(response.url)
        # read text file
        file = link.read()
        # Decode text file
        file_decode = file.decode('utf-8')
        # Split lines
        file_split = " ".join(file_decode.split())
        # Split each bond # and convert it into list
        bond_list = file_split.split(' ')
        for bond in bond_list:
            try:
                bond = int(bond)
                prize_list.append(bond)
            except:
                continue

        # Read Bonds from excel file and verify
        for bond_no in read_excel():
            if bond_no in prize_list:
                yield {
                    'Bond': re.search("(?:Rs.\.?)\s*(\d+(?:[.,]\d+)*)", response.url).group(0),
                    'Bond #': bond_no,
                    'DRAW Date': date(int(response.url.split('/')[-1].split('.')[0].split('-')[2][0:4]),
                                      int(response.url.split('/')[-1].split('.')[0].split('-')[1]),
                                      int(response.url.split('/')[-1].split('.')[0].split('-')[0])).strftime("%d-%m-%Y"),
                    'URL': response.url,
                }
