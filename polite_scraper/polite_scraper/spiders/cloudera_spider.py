import scrapy


class ClouderaJobs(scrapy.Spider):
    name = "cloudera"

    def start_requests(self):
        urls = [
            "https://jobs.jobvite.com/cloudera/search?l=Hungary+%3E+Budapest&c=&q="
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in response.xpath("//td[contains(@class,'jv-job-list-name')]/a/@href").extract(): # and this extract the links
            yield response.follow(href,self.parse_job)

    def parse_job(self,response):
        yield {
            'jobtitle' : response.xpath("//h2/text()").extract_first().strip(),
            'description' : response.xpath('//div[contains(@class, "jv-job-detail-description")]').extract()[0]
        }
