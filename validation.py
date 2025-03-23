# url_shortener/validation.py
import re

def is_valid_url(url):
    regex = r"^(?:http|ftp)s?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,6}(\.[a-zA-Z]{2})?(/[\w-]*)*$"
    return re.match(regex, url) is not None
