import scrapy
import csv

class MergedJobs(scrapy.Spider):
    name = "merged"

    locations = {
        "chemaxon" : { "url" : "https://www.chemaxon.com/jobs/",
                       "jobLinkSelect" : "//div[contains(@class, 'masonry-item')]/a/@href",
                       "jobtitle" : "//h1/text()",
                       "description" : "//div[contains(@class,'entry')]"},
        "cloudera" : { "url" : "https://jobs.jobvite.com/cloudera/search?l=Hungary+%3E+Budapest&c=&q=",
                       "jobLinkSelect" : "//td[contains(@class,'jv-job-list-name')]/a/@href",
                       "jobtitle" : "//h2/text()",
                       "description" : "//div[contains(@class, 'jv-job-detail-description')]"},
        "nng"      : { "url" : "https://www.nng.com/jobs/",
                       "jobLinkSelect" : "//td[contains(@class,'jv-job-list-name')]/a/@href",
                       "jobtitle" : "//h2[contains(@class, 'jv-header')]/text()",
                       "description" : "//div[contains(@class, 'jv-job-detail-description')]"}
    }
    def start_requests(self):
        for target in self.locations.keys():
            yield scrapy.Request(url=self.locations[target]["url"], callback=self.parse, meta = {"target" : target })

    
    def parse(self, response):
        target = response.meta["target"]
        jobLinkSelect = self.locations[target]["jobLinkSelect"]
        for href in response.xpath(jobLinkSelect).extract(): # and this extract the links
            yield response.follow(href,self.parse_job,meta = {"target" : target })

    def parse_job(self,response):
        target = response.meta["target"]
        yield {
            'company' : target,
            'jobtitle' : response.xpath(self.locations[target]["jobtitle"]).extract_first().strip(),
            'description' : response.xpath(self.locations[target]["description"]).extract()[0]
        }

