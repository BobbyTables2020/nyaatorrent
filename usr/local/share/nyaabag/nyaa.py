import requests
import utils
import torrent
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class Nyaa:

    def __init__(self):
        self.SITE = utils.TorrentSite.NYAASI
        self.URL = "https://nyaa.si"
        self.session = requests.Session()
        retry = Retry(connect=99, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def last_uploads(self, number_of_results):
        r = self.session.get(self.URL)

        # If anything up with nyaa servers let the user know.
        r.raise_for_status()

        json_data = utils.parse_nyaa(
            request_text=r.text,
            limit=number_of_results + 1,
            site=self.SITE
        )
        return torrent.json_to_class(json_data)

    def search(self, keyword, **kwargs):
        url = self.URL

        user = kwargs.get('user', None)
        category = kwargs.get('category', 0)
        subcategory = kwargs.get('subcategory', 0)
        filters = kwargs.get('filters', 0)
        page = kwargs.get('page', 0)

        if user:
            user_uri = f"user/{user}"
        else:
            user_uri = ""

        if page > 0:
            r = self.session.get("{}/{}?f={}&c={}_{}&q={}&p={}".format(
                url, user_uri, filters, category, subcategory, keyword,
                page))
        else:
            r = self.session.get("{}/{}?f={}&c={}_{}&q={}".format(
                url, user_uri, filters, category, subcategory, keyword))

        r.raise_for_status()

        json_data = utils.parse_nyaa(
            request_text=r.text,
            limit=None,
            site=self.SITE
        )

        return torrent.json_to_class(json_data)

    def get(self, view_id):
        r = self.session.get(f'{self.URL}/view/{view_id}')
        r.raise_for_status()

        json_data = utils.parse_single(request_text=r.text, site=self.SITE)

        return torrent.json_to_class(json_data)

    def get_user(self, username):
        r = self.session.get(f'{self.URL}/user/{username}')
        r.raise_for_status()

        json_data = utils.parse_nyaa(
            request_text=r.text,
            limit=None,
            site=self.SITE
        )
        return torrent.json_to_class(json_data)
