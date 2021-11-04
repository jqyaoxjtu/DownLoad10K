import re
from pathlib import Path

from curl_cffi import requests
from config import download_year_range, headers,base_index_name,index_path,files_path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor,as_completed

sess = requests.Session() # Construct connections pool

quit = False

def read_index():
    """
        Reading index file content, filter by `Form Type` to get the 10k file list
    """
    file2url = dict()
    for year in download_year_range:
        for quarter in range(1, 5):
            this_index_file = base_index_name % (year, quarter)

            with index_path.joinpath(this_index_file).open("rb") as f: # Reading index file content
                content = f.read()
            content = content.decode("gbk")

            split_contents = re.split("---+", content)
            info_lines = split_contents[-1]

            lines = info_lines.splitlines()
            lines = filter(None, lines)

            for line in lines:
                _, _, form_type, _, url_name = line.split("|")
                if re.match("10-?K", form_type, re.I) is not None: # Filter 10-k file
                    url_part = url_name.replace("edgar/data/", "")
                    file_name = url_part.replace("/", "_")
                    file2url[file_name] = url_name
    return file2url


def download_file(file_name, url):
    """
        Access url to get file content and save to file_name
    """
    if not quit:
        base_url = "http://www.sec.gov/Archives/%s"
        res = sess.get(base_url % (url), headers=headers, impersonate="chrome")
        if res.status_code != 200:
            print("error! the response code is %s" % res.status_code)
            return
        with files_path.joinpath(file_name).open("wb") as f: # Save content to file
            f.write(res.content)


def download_10k(all_index):
    all_downloaded_files = set([str(f.name) for f in files_path.glob("*.txt")])
    all_file = set(all_index.keys())
    print("total: %s" % len(all_file))
    print("need to download: %s" % len(all_file - all_downloaded_files))
    
    pool = ThreadPoolExecutor(max_workers=5) # Use five threads to download concurrently
    tasks = []
    for key in all_file - all_downloaded_files:
        this_url = all_index[key]
        tasks.append(pool.submit(download_file,key,this_url)) # Submit task to the Thread Pool
    try:
        for res in tqdm(as_completed(tasks)):
            res.result()
    except KeyboardInterrupt: # Handling exit signals
        print("hit ctrl c, shutdown!")

        global quit
        quit = True
        pool.shutdown(wait=True)
    else:
        pool.shutdown()


if __name__ == '__main__':
    all_index = read_index()
    download_10k(all_index)
