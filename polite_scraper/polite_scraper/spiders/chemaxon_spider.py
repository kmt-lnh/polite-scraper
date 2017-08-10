import scrapy


class ChemaxonJobs(scrapy.Spider):
    name = "chemaxon"

    def start_requests(self):
        urls = [
            "https://www.chemaxon.com/jobs/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        for href in response.xpath("//div[contains(@class, 'masonry-item')]/a/@href").extract(): # and this extract the links
            yield response.follow(href,self.parse_job)

    def parse_job(self,response):
        yield {
            'jobtitle' : response.xpath("//h1/text()").extract_first().strip(),
            'description' : response.xpath('//div[contains(@class,"entry")]').extract()[0]
        }

