import os
import urllib.request, urllib.error
import time
import sys

def readTextFile(filename):
    """
    Input:
    - filename: The name of the file to be read (not binary file)
    Output:
    - A list containing the lines from the txt file
    Purpose:
    - Return a list of species names to be searched
    """
    try:
        with open(filename,'r') as f:
            data = f.read().splitlines()  # splitlines removes the '\n'
        return data
    except:
        print("Keyword file was not found.")
        sys.exit()

def checkFolder(s, k):
    """
    Input:
    - s: Name of species
    - k: Extra keyword
    Return:
    - True: New folder created
    - False: Folder already exits
    Purpose:
    - Check to see if folder exists
    """
    folder_path = 'C:/Users/Matthew/Documents/Projects/Darwin/Web Scraper/Dataset/'
    if(k == ''):
        k = 'none'
    if(not os.path.exists(folder_path+s)):
        print("Creating new folder: {}".format(folder_path+s))
        os.makedirs(folder_path+s)
        print("Creating new folder: {}".format(folder_path+s+'/'+k))
        os.makedirs(folder_path+s+'/'+k)
        return True
    else:
        if(not os.path.exists(folder_path+s+'/'+k)):
            print("Creating new folder: {}".format(folder_path+s+'/'+k))
            os.makedirs(folder_path+s+'/'+k)
            return True
        else:
            return False

def download_page(url):
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))

#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            # print("No links")
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content

def downloadImages(items, species, keyword):
    if(keyword == ''):
        keyword = 'none'
    folder_path = 'C:/Users/Matthew/Documents/Projects/Darwin/Web Scraper/Dataset/' + species + '/' + keyword
    for i, img in enumerate(items):
        filename = folder_path+'/img_'+str(i)+'.jpg'
        try:
            req = urllib.request.Request(img, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            try:
                response = urllib.request.urlopen(req, None, 15)  # additional data=None, timeout due to connection=15 seconds
                output_file = open(filename,'wb')
                data = response.read()
                output_file.write(data)
                response.close();

                print("Downloaded: {}".format(filename))

            except httplib.IncompleteRead as e:
                e.partial
                print("Incomplete read on image: {}".format(filename))




        except IOError:   #If there is any IOError
            print("IOError on image: {}".format(filename))

        except urllib.error.HTTPError:  #If there is any HTTPError
            print("HTTPError on image: {}".format(filename))

        except urllib.error.URLError as e:
            print("URLError on image: {}".format(filename))
