from re import sub
from json import load
from scrapy import Selector, Spider, Request
from time import sleep


# Create the Spider class
class LPSESpiderTender(Spider):
    name = "lpsespidertender"
    id = 0
    data = dict()
    # Custom headers
    headers = {
        "referer": "https://lpse.lkpp.go.id/eproc4/lelang?kategoriId=&tahun=&instansiId=&rekanan=&kontrak_status=&kontrak_tipe=",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Cookie": "SPSE_SESSION=6cc9c9e6a5d17422816227504113c72e308aa541-___AT=820e4823d184b209a0e5840679dd7e769064ff1e&___TS=1734450500724&___ID=0172250d-92ca-4b0a-9de1-2efeb0d37c83; _cfuvid=J1AQW8E9Q817XZI4MF2zrkMOVaIvDOjArETseiAm00o-1734448688196-0.0.1.1-604800000",
    }

    # start_requests method
    def start_requests(self):
        # Open and read the JSON file
        with open("data/lpse_tender_data.json", "r") as file:
            tenders = load(file)
        self.data = {
            int(tender[0].strip()): {
                "Kode": int(tender[0].strip()),
                "Nama Paket": f"{tender[1].strip()} - {tender[8].strip()} - {tender[6].strip()} - {tender[5].strip()} - {tender[7].strip()} - Nilai kontrak {tender[10].strip()}",
                "K/L/PD/Instansi Lainnya": tender[2],
                "Tahapan": tender[3].strip(),
                "HPS": tender[4].strip(),
            }
            for tender in tenders["data"]
        }
        ids = [tender[0] for tender in tenders["data"]]

        pengumuman_lelang_urls = [
            f"https://lpse.lkpp.go.id/eproc4/lelang/{id}/pengumumanlelang" for id in ids
        ]
        peserta_urls = [
            f"https://lpse.lkpp.go.id/eproc4/lelang/{id}/peserta" for id in ids
        ]
        pemenang_urls = [
            f"https://lpse.lkpp.go.id/eproc4/evaluasi/{id}/pemenang" for id in ids
        ]
        pemenang_berkontrak_urls = [
            f"https://lpse.lkpp.go.id/eproc4/evaluasi/{id}/pemenangberkontrak"
            for id in ids
        ]

        # Pengumuman
        for url in iter(pengumuman_lelang_urls):
            self.id = int(url.split("/")[5])
            yield Request(url=url, headers=self.headers, callback=self.parse_pengumuman)
            sleep(1)

            # TODO: Comments
            # if len(self.data) >= 2:
            #     break

        # Peserta
        for url in iter(peserta_urls):
            self.id = int(url.split("/")[5])
            yield Request(url=url, headers=self.headers, callback=self.parse_peserta)
            sleep(1)

            # TODO: Comments
            # if len(self.data) >= 2:
            #     break

        # Pemenang
        for url in iter(pemenang_urls):
            self.id = int(url.split("/")[5])
            yield Request(url=url, headers=self.headers, callback=self.parse_pemenang)
            sleep(1)

            # TODO: Comments
            # if len(self.data) >= 2:
            #     break

        # Pemenang Berkontrak
        for url in iter(pemenang_berkontrak_urls):
            self.id = int(url.split("/")[5])
            yield Request(
                url=url, headers=self.headers, callback=self.parse_pemenang_berkontrak
            )
            sleep(1)

            # TODO: Comments
            # if len(self.data) >= 2:
            #     break

    def parse_pengumuman(self, response):
        # Extract all tables
        tables = response.xpath('//table[contains(@class,"table-bordered")]/tr')
        titles = tables.xpath("./th/text()").extract()
        contents = tables.xpath("./td").extract()
        pengumuman = dict()
        for title, content in zip(titles, contents):
            # Use a selector to clean content
            contentSelector = Selector(text=content)
            raw_content = contentSelector.css("::text").extract()
            clean_content = [
                sub(r"\s+", " ", text).strip()
                for text in raw_content  # Remove \n and excessive spaces
            ]
            pengumuman[title] = "".join(
                [item for item in clean_content if item]
            )  # Remove empty strings
        if pengumuman:
            self.data[self.id]["Pengumuman"] = pengumuman

    def parse_peserta(self, response):
        # Extract all tables
        tables = response.xpath('//table[contains(@class,"table")]')
        titles = tables.xpath("./thead/tr/th//text()").extract()
        contents = tables.xpath("./tbody/tr/td").extract()
        title_length = len(titles)
        content_length = len(contents)
        peserta_list = list()
        peserta = dict()
        for i in range(content_length):
            if i % title_length == 0:
                if len(peserta) != 0:
                    peserta_list.append(peserta)
                peserta = dict()
            content = Selector(text=contents[i])
            peserta[titles[i % title_length]] = "".join(
                [x for x in content.css("::text").extract()]
            ).strip()
        if len(peserta_list) > 0:
            self.data[self.id]["Peserta"] = peserta_list

    def parse_pemenang(self, response):
        # Extract all tables
        contents = response.xpath('//div[@class="content"]/table/tr').extract()
        content_length = len(contents)
        pemenang = dict()
        for i in range(content_length):
            content = Selector(text=contents[i])
            if i == 6:
                table = content.xpath("//table/tr")
                key = table.css("th").extract()
                value = table.css("td").extract()
                key_value = zip(key, value)
                for k, v in iter(key_value):
                    k_selector = Selector(text=k)
                    v_selector = Selector(text=v)
                    pemenang["".join(k_selector.css("::text").extract()).strip()] = (
                        "".join(v_selector.css("::text").extract()).strip()
                    )
            else:
                key = "".join(content.css("th::text").extract()).strip()
                value = "".join(content.css("td::text").extract()).strip()
                pemenang[key] = value
        if pemenang:
            self.data[self.id]["Pemenang"] = pemenang

    def parse_pemenang_berkontrak(self, response):
        # Extract all tables
        contents = response.xpath('//div[@class="content"]/table/tr').extract()
        content_length = len(contents)
        pemenang_berkontrak = dict()
        for i in range(content_length):
            content = Selector(text=contents[i])
            if i == 6:
                table = content.xpath("//table/tr")
                key = table.css("th").extract()
                value = table.css("td").extract()
                key_value = zip(key, value)
                for k, v in iter(key_value):
                    k_selector = Selector(text=k)
                    v_selector = Selector(text=v)
                    pemenang_berkontrak[
                        "".join(k_selector.css("::text").extract()).strip()
                    ] = "".join(v_selector.css("::text").extract()).strip()
            else:
                key = "".join(content.css("th::text").extract()).strip()
                value = "".join(content.css("td::text").extract()).strip()
                pemenang_berkontrak[key] = value
        if pemenang_berkontrak:
            self.data[self.id]["Pemenang Berkontrak"] = pemenang_berkontrak
