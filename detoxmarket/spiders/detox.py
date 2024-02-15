import scrapy, re

from detoxmarket.items import DetoxmarketItem
from datetime import datetime

class DetoxSpider(scrapy.Spider):
    name = 'detox'    

    BASE_URL = 'https://www.thedetoxmarket.com'

    urlPattern = r'^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?$'

    def start_requests(self):        
        self.logger.info('Start request Detox Market')

        targetUrl = self.BASE_URL + '/pages/brand-list'

        yield scrapy.Request(url=targetUrl, callback=self.parseAllBrand)

    def parseAllBrand(self, response):
        self.logger.info('Parse all brand')

        brandList = response.css('div.content > div.brand-letter-holder > div.row > div.four-fifths > div.row > div.column > a::attr(href)').getall()

        for brandUrl in brandList:        
            if (bool(re.match(self.urlPattern, brandUrl))):
                targetUrl = brandUrl
            else:
                targetUrl = self.BASE_URL + brandUrl

            #self.logger.info(targetUrl)
            yield scrapy.Request(url=targetUrl, callback=self.parseProductList)

    def parseProductList(self, response):
        self.logger.info('Parse product list')
        
        productList = response.css('div.product-list-container > div.product-list > div.product-block > div.product-block__inner > div.image > div.inner > a::attr(href)').getall()

        for productUrl in productList:            
            if (bool(re.match(self.urlPattern, productUrl))):
                targetUrl = productUrl
            else:
                targetUrl = self.BASE_URL + productUrl

            #self.logger.info(targetUrl)

            yield scrapy.Request(url=targetUrl, callback=self.parseProduct)

    def parseProduct(self, response):
        self.logger.info('Parse product')

        productName = response.css('div.product-details > div.product-title-wrapper > h1 > div.product-title::text').get()
        productName = productName.replace('\n', '').strip()

        productTag = response.css('div.product-details > div.product-special-tags-wrapper > span.special-tag::text').get()
        if productTag:
            productTag = productTag.replace('\n', '').strip()
        
        price = response.css('div.product-details > div.product-price > span::text').get()
        if price:
            price = price.replace('\n', '').strip()

        #descList = response.css('div.product-details > div.product-detail-accordion > div.cc-accordion > div.cc-accordion-item__panel > div.cc-accordion-item__content > p::text').extract()
        descList = response.css('div.product-details > div.product-detail-accordion > div.cc-accordion')
        
        description = descList.xpath('//details[@open=""]/div/div/p/text()').get()
        if description:
            description = description.replace('\n', '').strip()

        ingredients = descList.xpath('//details[@class="cc-accordion-item"][1]/div/div/text()').get()
        if ingredients:
            ingredients = ingredients.replace('\n', '').strip()

        howToUse = descList.xpath('//details[@class="cc-accordion-item"][2]/div/div/text()').get()
        if howToUse:
            howToUse = howToUse.replace('\n', '').strip()

        others = descList.xpath('//details[@class="cc-accordion-item"][3]/div/div/text()').get()
        if others:
            others = others.replace('\n', '').strip()

        now = datetime.now()        
        dtString = now.strftime("%d/%m/%Y %H:%M:%S")        

        #self.logger.info(descList)

        product = DetoxmarketItem()
        product['name'] = productName
        product['tag'] = productTag        
        product['feature'] = response.css('div.product-details > div.product-title-wrapper > h1 > div.brand-and-type > span.brand > a::attr(text)').get()
        product['price'] = price
        product['description'] = description        
        product['ingredients'] = ingredients
        product['howToUse'] = howToUse
        product['otherDetail'] = others
        product['scrapedDate'] = dtString
        product['imageSrc'] = response.css('div.product-container > div.product-gallery > div.main > div.product-slideshow > div.product-media > a.main-img-link::attr(href)').get()
        product['imageList'] = response.css('div.product-container > div.product-gallery > div.thumbnails > a.thumbnail::attr(href)').getall()        

        yield product