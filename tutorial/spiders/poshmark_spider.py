import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Brand Names Listing Page
# https://poshmark.com/brand/Nike-Men-Shoes?availability=all
# https://poshmark.com/brand/Nike?availability=all

# detail Page
# https://poshmark.com/listing/IKEA-Euro-Pillow-Covers-Set-of-2-Splash-of-color-Fun-646ec3b1932a8aeff17333f9

# Listing Page based on Category
# https://poshmark.com/category/Home-Bath-Hand_Towels
# https://poshmark.com/category/Women-Jewelry-Earrings

# Parties pAge
# https://poshmark.com/parties


class PoshmarkSpider(CrawlSpider):
    name = "poshmark"
    allowed_domains = ["poshmark.com"]
    start_urls = ["https://poshmark.com/"]

    rules = (
        Rule(LinkExtractor(allow="category")),
        Rule(LinkExtractor(allow="brand")),
        Rule(LinkExtractor(allow="listing"), callback="parse_item")
    )

    def parse_item(self, response):
        """ Parsing All Items """
        # Item Images
        image_list = []
        images = response.css("div.slideshow__container ul li")
        for image in images:
            image_list.append(image.css("img.ovf--h.d--b").attrib["src"])

        # Item Id
        id = response.css("a.listing__brand")

        # Item Title
        title = response.css("div.listing__title h1::text").get()       

        # Item Brand
        brand = response.css("a.listing__brand::text").get()

        # Item discount_price
        discount_price = response.css("p.h1::text").get()

        # Item price
        price = response.css("p.h1>span::text").get()

        # Item size
        size = response.css("button.size-selector__size-option::text").get()

        # Item Description
        description = response.css("div.listing__description::text").get()

        yield {
            "id": id.attrib["data-et-prop-listing_id"] if id else None,
            "images": image_list,
            "title": title.strip(),
            "brand": brand.strip() if brand else None,
            "discount_price": discount_price.strip() if discount_price else None,
            "price": price.strip() if price else None,
            "size": size.strip() if size else None,
            "description": description.strip() if size else None
        }
