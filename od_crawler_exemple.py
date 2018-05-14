from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Example usage. Links will be written into data.json

process = CrawlerProcess(get_project_settings())

process.crawl("od_links", base_url="http://the-eye.eu/public/ripreddit/")
process.start()
