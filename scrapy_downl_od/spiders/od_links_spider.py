import scrapy


class LinksSpider(scrapy.Spider):
    """Scrapy spider for open directories. Will gather all download links recursively"""

    name = "od_links"

    black_list = (
        "?C=N;O=D",
        "?C=M;O=A",
        "?C=S;O=A",
        "?C=D;O=A",
    )

    saved_links = set()

    def __index__(self, **kw):
        super(LinksSpider, self).__init__(**kw)
        self.base_url = kw.get("base_url")

    def should_save(self, link):
        """Whether or not a link should be saved"""
        return link not in self.saved_links and not link.rsplit("?", maxsplit=1)[0].endswith("/")

    def should_crawl(self, link):
        """Whether or not the link should be followed"""
        if link.endswith(tuple(self.black_list)):
            return False

        if not link.startswith(self.base_url):
            return False

        return link.rsplit("?", maxsplit=1)[0].endswith("/")

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)

    def parse(self, response):

        links = response.xpath('//a/@href').extract()
        for link in links:
            full_link = response.urljoin(link)

            if self.should_save(full_link):
                self.saved_links.add(full_link)
                yield {
                    "link": full_link
                }

            if self.should_crawl(full_link):
                yield response.follow(full_link, callback=self.parse)

