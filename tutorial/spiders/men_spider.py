# from pathlib import Path
import scrapy


class MenSpider(scrapy.Spider):
    name = "men"

    def start_requests(self):
        urls = [
            "https://poshmark.com/brand/Nike-Men-Shoes",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        shoes_data = {}
        # page = response.url.split("/")[-1]
        # filename = f"{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved File {filename}")
        shoes = response.css(".item__details")
        for shoe in shoes:
            # Get Shoe Id
            id_link = shoe.css("div>a")
            shoe_id = id_link.attrib["data-et-prop-listing_id"]

            # Get Shoe Name
            shoe_name = shoe.css("div>a::text").get()

            # Get Shoe Price
            shoe_price = shoe.css("div.m--t--1>span::text").get()

            shoe_data = {
                "id": shoe_id,
                "name": shoe_name,
                "price": shoe_price
            }
            shoes_data[shoe_id] = shoe_data

        # List of All Data
        print(shoes_data)
        print(len(shoes_data))
