from pathlib import Path

# downlaod date range
download_year_range = range(2015, 2016)

# request header
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

# index filename format template
base_index_name = "%sQTR%smaster.idx"

this_file_path = Path(__file__).parent
data_path = this_file_path.joinpath("../data")
index_path = data_path.joinpath("index")
files_path = data_path.joinpath("10k")
data_path.mkdir(exist_ok=True)
index_path.mkdir(exist_ok=True)
files_path.mkdir(exist_ok=True)