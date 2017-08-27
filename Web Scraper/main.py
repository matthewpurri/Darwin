import time  # Runtime
import sys  # Folder and error managment
import os  # File managment
import urllib.request, urllib.error  # Webscraping tools
import helper as hlp  # To use functions from helper.py file

species_names = hlp.readTextFile("search_keywords.txt")
extra_keywords = hlp.readTextFile("extra_keywords.txt")

def main():
    for species in species_names:
        print("Species: {}".format(species))
        search_species = species.replace(' ','%20')
        for keyword in extra_keywords:
            if(hlp.checkFolder(species, keyword)):  # If folder already created do not rerun
                if(keyword != ''):
                    search_keyward = ' ' + keyword
                    search_keyword = search_keyward.replace(' ','%20')
                    url = 'https://www.google.com/search?q=' + search_species + search_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
                else:
                    url = 'https://www.google.com/search?q=' + search_species + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'

                raw_html = hlp.download_page(url)
                items = hlp._images_get_all_items(raw_html)

                # Download files
                hlp.downloadImages(items, species, keyword)

if __name__ == '__main__':
    main()
