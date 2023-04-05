import scrapy
import json
import xml.etree.ElementTree as ET

class MySpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        # Read the sitemap from the local file
        # import idioms_sitemap_1.xml (in the same directory as this file) as sitemap_xml
        with open("sitemaps/idioms_sitemap_1.xml", "r") as f:
            sitemap_xml = f.read()

        # Parse the sitemap XML
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        root = ET.fromstring(sitemap_xml)
        for url in root.findall(".//ns:loc", namespace):
            yield scrapy.Request(url.text, self.parse)

    def parse(self, response):
        # Extract the data using XPath
        idiom = response.xpath("""//*[@id="Definition"]/section[1]/h2""").get()
        description = response.xpath("""//*[@id="Definition"]/section[1]/div[1]""").get()

        # Save the data to a JSON file
        data = {'idiom': idiom, 'description': description}
        with open("output.json", "a") as f:
            json.dump(data, f)
            f.write("\n")

