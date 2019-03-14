import requests
import urllib.request
import bs4
import re
import os
import sys


def download_code(url,time=10):
    print("Downloading site code.")
    try:
        source_code = requests.get(url,timeout=10).text
        BS_parse = bs4.BeautifulSoup(source_code, "html.parser")
        print("SUCCESS!")
        return BS_parse

    except requests.exceptions.ConnectionError:
        print("Connection error.\nCan not download code for: {}".format(url))
    except requests.exceptions.MissingSchema as er:
        print(er)
    except requests.exceptions.InvalidSchema as er:
        print(er)

def delete_style_and_script(source_code):
    print("Removing style and JS.")
    for script in source_code(["script", "style"]):
        script.extract()
    print("SUCCESS!")
    return source_code


def get_text(source_code):
    print("Extracting text.")
    a=source_code.get_text()
    print("SUCCESS!")
    return a


def get_img_link(source_code,source_url):
    all_img = source_code.findAll("img")
    print('Collecting all images.')
    img_url_list = []
    for img in all_img:

        img_url = img.get("src")
        if not img_url: continue

        if re.match("^//", img_url):
            img_url = "http:" + img_url
        if re.match("^/", img_url):
            img_url = source_url + img_url
        img_url_list.append(img_url)
    print("SUCCESS!")
    return list(set(img_url_list))


def save_img(urls_list,source_url,path=False):
    print("Saving images.")
    size_of_img=len(urls_list)
    file_names={}
    counter=0

    if not path:
        path=re.search('^.*?[a-z](/|$)', source_url).group(0).split("//")[1].strip("/")

    if not os.path.exists(path):
        os.makedirs(path)

    for url in urls_list:
        img_name = re.search('^.*?/', url[::-1]).group(0)[::-1].strip("/")
        # print(img_name)

        if img_name not in file_names:
            file_names[img_name]=0
        else:
            file_names[img_name]+=1
            img_name_splited=img_name.split(".")
            img_name=img_name_splited[0]+"_"+str(file_names[img_name])+"."+".".join(img_name_splited[1:])

        counter += 1

        try:
            urllib.request.urlretrieve(url, path+"/"+img_name)
            sys.stdout.write("\rDOWNLOAD OF IMG FILES: {}%".format(counter * 100 / size_of_img))
            sys.stdout.flush()
        except urllib.error.HTTPError:
            print("\nCould not download {}\n{}!".format(img_name,url))
    else:
        print("\nSUCCESS!")


def save_text(text,source_url,path=False):
    print("Saving text from the page.")
    site_name=re.search('^.*?[a-z](/|$)', source_url).group(0).split("//")[1].strip("/")

    if not path:
        path=site_name

    if not os.path.exists(path):
        os.makedirs(path)

    final_save_file = path+"/"+site_name+"_text"

    with open(final_save_file,"w") as file:
        file.write(text)
    print("SUCCESS!")


def test():
    test_url=["https://en.wikipedia.org/wiki/Main_Page","http://da.mn/","https://www.yahoo.com/","https://www.google.com","https://www.youtube.com/"]

    ok=0
    for url in test_url:
        print("\nTest for: "+url)
        test=do_everything(url)
        if test: ok+=1

    print("\nCorrect for {}% of test data.".format(ok*100/len(test_url)))


def do_everything(url):
    full_code = download_code(url)
    if full_code:
        extracted_code = delete_style_and_script(full_code)
        text = get_text(extracted_code)
        img_list = get_img_link(extracted_code, url)
        save_img(img_list, url)
        save_text(text, url)
        return True
    return False


def __main__():
    url="http://da.mn/"
    test()

if __name__ == '__main__':
    __main__()
