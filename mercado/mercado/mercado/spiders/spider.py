import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from mercado.items import MercadoItem

class MercadoSpider(CrawlSpider):
    name = "mercado"
    item_count = 0
    allowed_domain = ["www.mercadolibre.com.mx"]
    start_urls = ["https://listado.mercadolibre.com.mx/impresoras#D[A:impresoras]"]

    rules = {
        Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="andes-pagination__button andes-pagination__button--next shops__pagination-button"]/a'))),
        Rule(LinkExtractor(allow = (), restrict_xpaths = ('//h2[@class="ui-search-item__title shops__item-title"]')), 
            callback = 'parse_item', follow = False),
    }

    def parse_item(self, response):
        ml_item = MercadoItem()

        #info de producto
        ml_item["titulo"] = response.xpath('normalize-space(/html/body/main/div[2]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div[2]/h1/text())').extract()
        ml_item["precio"] = response.xpath('normalize-space(//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[2]/div[1]/span/span[3]/text())').extract()
        ml_item["condicion"] = response.xpath('normalize-space(/html/body/main/div[2]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span/text())').extract()
        ml_item["envio"] = response.xpath('normalize-space(//*[contains(@class, "ui-pdp-media__title--on-hover"")]/text())').extract()
        ml_item["opiniones"] = response.xpath('normalize-space(//p[@class="ui-review-capability__rating__average ui-review-capability__rating__average--desktop"]/text())').extract()
        ml_item["ventas_productos"] = response.xpath('normalize-space(/html/body/main/div[2]/div[3]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div[1]/span/text())').extract()
        
        # info de la tienda o vendedor
        ml_item["vendedor-url"] = response.xpath('normalize-space(//*[starts-with(@class, "ui-pdp-media__action")]/@href)').extract()
        ml_item["tipo_vendedor"] = response.xpath('normalize-space(/html/body/main/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/div/p[1]/text())').extract()
        ml_item["ventas_vendedor"] = response.xpath('normalize-space(/html/body/main/div[2]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[1]/strong/text())').extract()
        self.item_count += 1
        if self.item_count > 20:
            raise CloseSpider('item_exceed')
        yield ml_item

        