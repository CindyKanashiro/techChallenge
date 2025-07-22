import re
import sqlite3
from typing import Literal
from urllib.parse import urljoin

import pandas as pd
import requests
from scraping.utils import fetch_soup


def download_catalogue_data():
    """Download the book catalogue data and save it as a SQLite table."""

    df = fetch_catalogue_data()
    save_catalogue_data_as_sqlite_table(df)


def fetch_catalogue_data() -> pd.DataFrame:
    """Fetch all book data from the catalogue pages.

    Args:
        catalogue_url (str): the base URL of the catalogue pages.

    Returns:
        pd.DataFrame: a DataFrame containing details of all books in the
        catalogue.
    """

    catalogue_url = "http://books.toscrape.com/catalogue/"

    df = pd.DataFrame(
        columns=["title", "price", "rating", "stock", "category", "cover"]
    )

    book_urls = fetch_book_urls(catalogue_url)

    for book_url in book_urls:
        book_details = fetch_book_details(book_url)
        df = pd.concat([df, pd.DataFrame([book_details])], ignore_index=True)
    return df


def fetch_book_urls(catalogue_url: str) -> list[str]:
    """Fetch all book URLs from all of the catalogue pages.

    Args:
        catalogue_url (str): the base URL of the catalogue pages.

    Returns:
        list[str]: a list of URLs of all books in the catalogue.
    """

    book_urls = []

    number_of_pages = int(
        fetch_soup(urljoin(catalogue_url, "page-1.html"))
        .select_one("ul.pager li.current")
        .get_text(strip=True)
        .removeprefix("Page 1 of ")
    )

    for page_number in range(1, number_of_pages + 1):
        page_url = urljoin(catalogue_url, f"page-{page_number}.html")
        soup = fetch_soup(page_url)

        page_book_urls = [
            urljoin(catalogue_url, a["href"])
            for a in soup.select("article.product_pod h3 a")
        ]
        book_urls.extend(page_book_urls)

    return book_urls


def fetch_book_details(book_url: str) -> dict:
    """Fetch the details of a book from its page.

    Args:
        book_url (str): the URL of the book's page.

    Returns:
        dict: a dictionary containing the book's title, price, rating, stock,
        category, and cover image.
    """
    soup = fetch_soup(book_url)

    title = soup.select_one("div.product_main h1").get_text(strip=True)

    price = float(
        soup.find("th", string="Price (incl. tax)")
        .find_next_sibling("td")
        .get_text(strip=True)
        .removeprefix("£")  # remove o símbolo da moeda
    )

    rating_classes = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = rating_classes[soup.select_one("p.star-rating")["class"][-1]]

    stock = (
        soup.find("th", string="Availability")
        .find_next_sibling("td")
        .get_text(strip=True)
    )
    stock = re.search(r"\d+", stock)  # busca valor numérico interio na string
    stock = (
        int(stock.group()) if stock else 0
    )  # se não existir valor numérico, assume 0

    category = soup.select_one("ul.breadcrumb").find_all("li")[2].get_text(strip=True)

    cover_url = urljoin(book_url, soup.select_one("div.item.active img")["src"])
    cover = requests.get(cover_url).content  # array de bytes

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "stock": stock,
        "category": category,
        "cover": cover,
    }


def save_catalogue_data_as_sqlite_table(
    df: pd.DataFrame,
    db_path: str = "books.db",
    if_exists: Literal["fail", "replace", "append"] = "replace",
) -> None:
    """Save the DataFrame containing book details as a table in a SQLite database.

    Args:
        df (pd.DataFrame): DataFrame containing book details.
        db_path (str, optional): path to the sqlite database file. Defaults to
        "books.db".
        if_exists (Literal["fail", "replace", "append"], optional): behavior
        when the table already exists. Defaults to "replace".
    """

    with sqlite3.connect(db_path) as conn:
        df.to_sql(
            "books",
            conn,
            if_exists=if_exists,
            index=False,
        )
