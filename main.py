import requests
from bs4 import BeautifulSoup as HQArena
from tqdm import tqdm
import os

def find_all_html_pages(main_page_url):
    response = requests.get(main_page_url, allow_redirects=True)
    data = HQArena(response.text, 'lxml')
    all_pages = data.find_all('a', itemprop="url")
    return all_pages

def download_image(url, url_prefix, count):
    response = requests.get(url, allow_redirects=True)
    data = HQArena(response.text, 'lxml')
    image_url = data.find('a', id="resolution")
    file_postfix = data.find('meta', itemprop="keywords")['content'].replace(" ", "-").replace(",", "")[:20]

    if image_url is not None:
        i_url = image_url['href']
        try:
            response = requests.get(url_prefix + i_url, stream=True)
            total_size_in_bytes = int(response.headers.get('content-length', 0))  # Fixed the missing closing parenthesis
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

            with open(f'{count}-{file_postfix}.jpg', 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")
        except:
            print("It might be the connection broken :|")

if __name__ == "__main__":
    all_pages = find_all_html_pages("https://4kwallpapers.com/random-wallpapers/")
    count = 0
    os.chdir(os.path.expanduser('~/Pictures'))
    for page in all_pages:
        url = page['href']
        download_image(url, "https://4kwallpapers.com", count)
        count += 1
