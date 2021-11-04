# Overview

The purpose of this repo is to download 10-K(annual report) files in EDGAR. The download process can be divided into two steps:

1. Download the index file for the specified year from <https://www.sec.gov/Archives/edgar/full-index/>. e.g., you can download the index file of the first quarter of 2015 from  <https://www.sec.gov/Archives/edgar/full-index/2015/QTR1/master.idx>.

2. Parse the index file. Each index file contains five variables, follow the format below:

    >CIK|Company Name|Form Type|Date Filed|Filename

    We can filter by `Form Type`, keep all rows whose `Form type` is `10-K`, then get the download link by concatenate their `Filename` and base URL <http://www.sec.gov/Archives/>, and finally use the `requests` package to access the URL and save content to file.  

## example

Assume that the contents of the index file we want to download are as follows:

>CIK|Company Name|Form Type|Date Filed|Filename
>
>1000209|MEDALLION FINANCIAL CORP|10-K|2015-03-11|edgar/data/1000209/0001193125-15-087622.txt

We can see that the `Form Type` of this line is `10-K`, which match our conditions, and the content of the `Filename` part in this line is `edgar/data/1000209/0001193125-15-087622.txt`, then extract it and concatenate it with the `http://www.sec.gov/Archives/`， we can get the download URL corresponding to this file: <http://www.sec.gov/Archives/edgar/data/1000209/0001193125-15-087622.txt>, finally access URL to download this file.

## File description

- **config.py**: Configuration file

- **get_index.py**: Download the index file according to the configuration and save it to the index folder under the data directory

- **download.py**: Download 10-k file based on the index file content and save it to the 10k folder under the data directory

**Note**: The data directory is in the project root directory used to store the downloaded data; when it does not exist, the program will automatically create it.

## Requirements

- python(3.6+)
- requests
- tqdm

## Usage

1. Open `config.py` and change the value of the 'download_year_range' variable, assuming you want to download data of 2015

    ```python
    download_year_range = range(2015, 2016)
    ```

2. Install the required libraries.

    ```bash
    pip install -r requirements.txt
    ```

3. Execute `get_index.py` to get EDGAR Index Files.

    ```bash
    python src/get_index.py
    ```

4. Execute `download.py` to download 10K.

    ```bash
    python src/download.py
    ```
