# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".


"""5dimes mma odds"""
# coding=utf-8
#
# Scrapes bestfightodds.com and makes data available on IRC via search

import scraperwiki
import os
from lxml import html
from requests import get

page = get('http://bestfightodds.com')
    
cutoff_point = page.text.find('Future Events')
tree = html.fromstring(page.text[:cutoff_point])

btree = tree.xpath('////div[@class="table-scroller"]/table/tbody/tr[@class="even"]')
rtree = tree.xpath('////div[@class="table-scroller"]/table/tbody/tr[@class="odd"]')

for index, i in enumerate(btree):
    name = i[0][0][0].text
    if not i[1][0][0][0].text:
        odds = None
    else:
        odds = i[1][0][0][0].text
    index = 1000 + index
    scraperwiki.sqlite.save(unique_keys=["index"], data={"index":index, "name":name, "odds":odds}, table_name="data")

for index, i in enumerate(rtree):
    name = i[0][0][0].text
    if not i[1][0][0][0].text:
        odds = None
    else:
        odds = i[1][0][0][0].text
    index = 2000 + index
    scraperwiki.sqlite.save(unique_keys=["index"], data={"index":index, "name":name, "odds":odds}, table_name="data")

os.rename("scraperwiki.sqlite", "data.sqlite")
