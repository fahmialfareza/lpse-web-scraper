from requests import post
from json import dump
from os.path import dirname, join, abspath
from config.config import (
    LPSE_URL,
    LPSE_AUTHENTICITY_TOKEN,
    LPSE_COOKIE,
    LPSE_USER_AGENT,
    LPSE_LELANG_DATA_LENGTH,
)


def download_tender_data():
    """Download the tender data from the LPSE website and save it to a JSON file.

    This function sends a POST request to the LPSE website to download the tender data. The data is then saved to a JSON file in the 'data' directory.

    Returns:
        None
    Raises:
        None
    """

    # Define the URL
    url = f"{LPSE_URL}/lkpp/dt/lelang?draw=1&start=0&length={LPSE_LELANG_DATA_LENGTH}&authenticityToken={LPSE_AUTHENTICITY_TOKEN}"

    # Send the POST request
    response = post(
        url,
        headers={
            "Cookie": f"{LPSE_COOKIE}",
            "Referer": f"{LPSE_URL}/lkpp/lelang",
            "Origin": f"{LPSE_URL}",
            "User-Agent": f"{LPSE_USER_AGENT}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        },
    )

    # Check the response status
    if response.status_code == 200:
        # Get the path to the 'data' directory
        base_dir = dirname(dirname(abspath(__file__)))
        data_dir = join(base_dir, "..", "data", "downloader")
        file_path = join(data_dir, "lpse_tender_data.json")

        # Parse JSON response
        json_data = response.json()

        # Save to a file
        with open(file_path, "w", encoding="utf-8") as file:
            dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"Data saved to {file_path}")

        return file_path
    else:
        raise Exception(
            f"Failed to fetch data. HTTP Status Code: {response.status_code}"
        )
