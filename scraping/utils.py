import requests
from bs4 import BeautifulSoup


def fetch_soup(url: str) -> BeautifulSoup:
    """Download the HTML source-code of a specified URL and return it as a BeautifulSoup.

    Args:
        url (str): the URL to request.

    Returns:
        BeautifulSoup: the content of the requested URL structured as a BeautifulSoup
        object.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except:
        # TO-DO: adicionar logging de erro quando não for possível alcançar o
        # conteúdo da página
        raise

    return BeautifulSoup(response.content, "html.parser")
