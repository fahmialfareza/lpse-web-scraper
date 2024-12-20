from requests import post
from json import dump


def download_tender_data():
    # Define the URL
    url = "https://lpse.lkpp.go.id/eproc4/dt/lelang?draw=1&start=0&length=20000&authenticityToken=e4b9b0c81d9993c737c58c06c745556d7031b3fe"

    # Send the POST request
    response = post(
        url,
        headers={
            "Cookie": "SPSE_SESSION=85340a9fd784646c4b4045c5c80eef87c5ea1434-___AT=e4b9b0c81d9993c737c58c06c745556d7031b3fe&___TS=1734594364801&___ID=711b4963-a2b3-40c9-9cad-fa679517eadb; _cfuvid=mbrnaT3KwWhctwT4CIu.sgnMbSRhwqee8Ta8GrA1w.g-1734438947358-0.0.1.1-604800000; cf_clearance=DvKP1cg8uP24w3yrAMEKBB2v5thEPS.yQpU0CaVMrZU-1734560978-1.2.1.1-Ckjc74t1G9WrjukddSETNE197xNN9Zqf01EHwhCGUscVXfHh6.TIij2BJluAFo7aS49ic7VE0p2FeOj9252iaelsTlcuQK1U9E3LxE3BnUKS.FUvq6lqlYqYCFxQnW.A_L4KcSXcHeFTyaS79GtNc9BD9MsKQNSyUx_WPOLQL0HHnUWNfgMaF5f37NjJnUZvqai4gzVdAOsbAkR3bQpS4dYQG9.XkjewEhiQbNk6uyrdxN6bxdZ4phKuvMlmwK3rbquldVhYjV94U8U7YkauTgzACiX9_A8JiTpXnhJYA1PRiUIYek6QIn5NmeLp_kMj2PnslCI.nGihMJ6Z7pUoWPlU7PGCYEMzu.ffQOiwIAkaiUSO306tCnj3sMSdHsXh",
            "Referer": "https://lpse.lkpp.go.id/eproc4/lelang",
            "Origin": "https://lpse.lkpp.go.id",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        },
    )

    # Check the response status
    if response.status_code == 200:
        # Parse JSON response
        json_data = response.json()

        # Save to a file
        with open(
            "data/downloader/lpse_tender_data.json", "w", encoding="utf-8"
        ) as file:
            dump(json_data, file, ensure_ascii=False, indent=4)
        print("Data saved to data/downloader/lpse_tender_data.json")
    else:
        print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
