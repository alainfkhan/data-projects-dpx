"""URL managers"""

from pathlib import Path
from typing import Protocol
from urllib.parse import urlparse

import kaggle

from icecream import ic
from requests.exceptions import HTTPError
from rich import print


# Interface
class URLHandler(Protocol):
    def can_handle(self, url: str) -> bool: ...
    def download(self, url: str, *, raw_path: Path, external_path: Path) -> Path: ...


class KaggleHandler:
    def can_handle(self, url: str) -> bool:
        return "kaggle.com" in url

    def download(self, url: str, *, raw_path: Path, external_path: Path) -> Path:
        parsed_url = urlparse(url)

        # TODO: clean include url query
        handle = parsed_url.path.removeprefix("/datasets/").removesuffix("/data")

        kaggle.api.authenticate()

        try:
            kaggle.api.dataset_download_files(
                dataset=handle,
                path=raw_path,
                unzip=True,
            )
        except HTTPError as e:
            print(e)
            print("Kaggle dataset not found. Verify the kaggle URL is correct.")
        else:
            kaggle.api.dataset_metadata(
                dataset=handle,
                path=external_path,
            )

        return raw_path


class DirectDownloadHandler:
    # https://srhdpeuwpubsa.blob.core.windows.net/whdh/COVID/WHO-COVID-19-global-table-data.csv
    def can_handle(self, url: str) -> bool:
        return url.endswith(".csv") or "download" in url

    def download(self, url: str, *, raw_path: Path, external_path: Path) -> Path:
        return raw_path


class URLDispatcher:
    handlers: list[URLHandler] = [
        KaggleHandler(),
        DirectDownloadHandler(),
    ]

    def __init__(self) -> None:
        pass

    def download(self, url: str, *, raw_path: Path, external_path: Path) -> Path:
        # check if url is valid url
        # parsed_url = urlparse(url)

        for handler in self.handlers:
            if handler.can_handle(url):
                return handler.download(
                    url,
                    raw_path=raw_path,
                    external_path=external_path,
                )

        raise ValueError(f"No handler found for URL: {url}")
