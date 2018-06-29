# coding=utf-8
from bs4 import BeautifulSoup
import os, sys, urllib2, time, random

path = os.getcwd()
root_path = os.path.join(path, u'wwwroot')
if not os.path.isdir(root_path):
    os.mkdir(root_path)
downloaded_list = []

def download_loop(base_url, base_path):
    print base_url
    print base_path
    
    content = urllib2.urlopen(base_url)
    soup = BeautifulSoup(content)
    link = soup.find_all('a')
    for download in link:
        flink = download.get('href')
        if isinstance(flink, basestring) == False:
            continue

        if flink.find(".html", len(flink) - 5) != -1:
            print '+' + flink
            if flink.startswith("http"):
                continue

            down_url = combine_url(base_url, flink)
            disk_dir = make_recursion_dir(down_url, base_path)
            disk_file = combine_disk_path(disk_dir, flink)
            if down_url in downloaded_list:
                continue
            
            try:
                content2 = urllib2.urlopen(down_url).read()
                with open(disk_file, 'wb') as code:
                    code.write(content2)
                    soup2 = BeautifulSoup(content2)
                    downloaded_list.append(down_url)
                    download_resource(soup2, base_url, base_path, ".css")
                    download_resource(soup2, base_url, base_path, ".js")
                    download_resource(soup2, base_url, base_path, ".png")
                    download_resource(soup2, base_url, base_path, ".jpg")
                    download_resource(soup2, base_url, base_path, ".gif")
            except urllib2.HTTPError,e:
                print e.reason

def make_recursion_dir(url, base_path):
    start_index = 0
    if url.find("http://") != -1:
        start_index=7
    if url.find("https://") != -1:
        start_index=8
    first_position = url.find("/", start_index)
    if first_position == -1:
        return base_path
    if first_position == len(url)-1:
        return base_path
    second_position = url.find("/", first_position+1)
    if second_position == -1:
        return base_path;
    if first_position == second_position:
        return base_path
    folder = url[first_position: second_position]
    file_path = os.path.join(base_path, folder.replace("/", ""))
    if not os.path.isdir(file_path):
        os.mkdir(file_path)
    return make_recursion_dir(url[second_position:], file_path)

def combine_disk_path(disk_dir, flink):
    last_position = flink.rfind("?")
    if last_position == -1:
        last_position = len(flink)+1
    if flink.find("/") == -1:
        file_name = flink[0:last_position]
    else:
        last_split = flink.rfind("/")
        file_name=flink[last_split+1:last_position]
    return os.path.join(disk_dir, file_name)

def combine_url(base_url, flink):
    if flink.find("../") == 0:
        last_split = base_url[0:len(base_url)-1].rfind("/")
        return combine_url(base_url[0:last_split+1],flink[3:])
    else:
        return base_url+flink

def download_resource(soup, base_url, base_path, suffix):
    if suffix == ".css":
        tag = "link"
        attr = "href"
    elif suffix == ".js":
        tag = "script"
        attr = "src"
    elif suffix == ".png":
        tag = "img"
        attr = "src"
    elif suffix == ".jpg":
        tag = "img"
        attr = "src"
    elif suffix == ".gif":
        tag = "img"
        attr = "src"
    link = soup.find_all(tag)
    for resource in link:
        flink = resource.get(attr)
        if isinstance(flink, basestring) == False:
            continue

        if flink.find(suffix, len(flink) - len(suffix)) != -1:
            print '+' + flink
            if flink.startswith("http"):
                continue
            
            down_url = combine_url(base_url, flink)
            disk_dir = make_recursion_dir(down_url, base_path)
            disk_file = combine_disk_path(disk_dir, flink)
            if os.path.exists(disk_file):
                continue
            if down_url in downloaded_list:
                continue
            try:
                content2 = urllib2.urlopen(down_url).read()
                with open(disk_file, 'wb') as code:
                    code.write(content2)
                    downloaded_list.append(down_url)
                    if suffix == ".css":
                        download_res_in_css(down_url, base_path, content2)
            except urllib2.URLError,e:
                print e.reason

def download_res_in_css(css_url, base_path, content):
    split_array = content.split("url(")
    if len(split_array) == 0:
        return
    split_array = split_array[1:]
    for piece in split_array:
        piece = "url(" + piece
        try:
            download_res_in_css_split(css_url, base_path, piece)
        except urllib2.URLError,e:
            print e.reason
        except IOError,e:
            print "IOError"
        except WindowsError,e:
            print "WindowsError"

def download_res_in_css_split(css_url, base_path, content):
    first_position = content.find("url(")
    if first_position == -1:
        return
    second_position = content.find(")",first_position)
    if second_position == -1:
        return
    sub_str = content[first_position+4:second_position]
    res_url = sub_str.replace("\\'","").replace("\\\"","").replace("'","").replace("\"","")
    print '+' + res_url

    if res_url.startswith("http"):
        return
    if res_url.startswith("data"):
        return
    base_url = css_url[0:css_url.rfind("/")+1]
    down_url = combine_url(base_url,res_url)
    disk_dir = make_recursion_dir(down_url, base_path)
    disk_file = combine_disk_path(disk_dir, res_url)
    if os.path.exists(disk_file):
        return
    content2 = urllib2.urlopen(down_url).read()
    with open(disk_file, 'wb') as code:
        code.write(content2)

##    print u'download completed'

download_loop('http://www.runoob.com/python/', root_path)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
raw_input("Press <Enter> To Quit!")