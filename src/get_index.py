from curl_cffi import requests
from pathlib import Path
from time import sleep
from config import headers,download_year_range,base_index_name,index_path

base_url = "https://www.sec.gov/Archives/edgar/full-index/%s/QTR%s/master.idx"



def get_all_url_and_name():
    """
        Generate all files and URLs to be downloaded base on template
    """
    all_urls = []
    all_names = []
    for year in download_year_range:
        for quarter in range(1, 5):
            all_urls.append(base_url % (year, quarter))
            all_names.append(base_index_name % (year, quarter))
    return all_urls, all_names


def download_index(urls,names):
    """
        Download index file
    """
    for url,name in zip(urls,names):
        print("download %s..." % name)
        res = requests.get(url,headers=headers, impersonate="chrome")
        if res.status_code != 200:
            print("error! response code is %s" % res.status_code)
        with index_path.joinpath(name).open("wb") as f:
            f.write(res.content)
        sleep(1)

if __name__ == '__main__':
    urls,names = get_all_url_and_name()
    download_index(urls,names)
