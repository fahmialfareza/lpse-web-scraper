from requests import post
from json import dump

# Define the URL
url = "https://lpse.lkpp.go.id/eproc4/dt/lelang?draw=1&start=0&length=20000&authenticityToken=982f56df3601b36dfbdf4e896bd9055652172738"


# Send the POST request
response = post(url)

# Check the response status
if response.status_code == 200:
    # Parse JSON response
    json_data = response.json()

    # Save to a file
    with open("data/lpse_tender_data.json", "w", encoding="utf-8") as file:
        dump(json_data, file, ensure_ascii=False, indent=4)
    print("Data saved to data/lpse_tender_data.json")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
