import os
import argparse
import requests
from pathlib import Path
from requests import HTTPError
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
import logging
import time
from urllib.parse import urljoin


logger = logging.getLogger('Logger')


def get_soup(url, id_book):
    response = requests.get(f'{url}/b{id_book}/')
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def check_for_redirect(response):
            if response.history:
                raise HTTPError


def download_txt(url, id_book, filename, folder='books/'):
    url = f"{url}/txt.php"
    payload_txt = {'id': id_book}
    response = requests.get(url, params=payload_txt)
    response.raise_for_status()
    check_for_redirect(response)

    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath_without_format = os.path.join(folder, sanitize_filename(filename))
    filepath = f'{filepath_without_format}.txt'
    with open(filepath, 'w') as file:
        file.write(response.text)

    return filepath


def download_image(url, image, filename, folder='images/'):
    url = urljoin(url, image)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(folder, sanitize_filename(filename))
    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_comments(comments, filename, folder='comments/'):
    Path(folder).mkdir(parents=True, exist_ok=True)
    filepath_without_format = os.path.join(folder, sanitize_filename(filename))
    filepath = f'{filepath_without_format}.txt'
    with open(filepath, 'w') as file:
        file.writelines(f"{comment}\n" for comment in comments)

    return filepath


def parse_book_page(soup):
    not_sanitized_tittle, not_sanitized_author = soup.find('h1').text.split('::')
    tittle = sanitize_filename(not_sanitized_tittle.strip())
    author = sanitize_filename(not_sanitized_author.strip())

    comments_tag = soup.find_all(class_='texts')
    comments = [comment.find(class_='black').text for comment in comments_tag]

    genre_tag = soup.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in genre_tag]

    image_tag = soup.find(class_='bookimage').find('img')['src']
    image = image_tag.split('/')[-1]
    parse_book = tittle, author, comments, genres, image, image_tag

    return parse_book


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Скачивание заданных страниц'
    )
    parser.add_argument('start_id', help='Страница с', type=int)
    parser.add_argument('end_id', help='Страница по', type=int)
    args = parser.parse_args()

    return args.start_id, args.end_id


def main():
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)

    url = 'https://tululu.org'
    start_id, end_id = get_arguments()

    for id_book in range(start_id, end_id + 1):
        try:
            soup = get_soup(url, id_book)
            tittle, author, comments, genres, image, image_tag = parse_book_page(soup)
            download_txt(url, id_book, f'{id_book}. {tittle}')
            download_image(url, image_tag, image)
            download_comments(comments, f'{id_book}. {tittle} - комментарии')
        except HTTPError:
            logger.warning(f'Страница {url}/b{id_book} не существует')
            continue
        except ConnectionError:
            logger.warning('Потеряно соединение с интернетом')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
