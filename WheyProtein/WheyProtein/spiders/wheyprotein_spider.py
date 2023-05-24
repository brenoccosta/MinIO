import scrapy
from datetime import datetime

class AgendaSpider(scrapy.Spider):
    name = "wheyprotein"
    start_urls = [
        # Max Titatnium Top Whey 3W 900g
        # "https://www.mercadolivre.com.br/suplemento-em-po-max-titanium-top-whey-3w-proteinas-top-whey-3w-sabor-baunilha-em-pote-de-900g/p/MLB6091177?pdp_filters=item_id:MLB2963216994#is_advertising=true&searchVariation=MLB6091177&position=1&search_layout=stack&type=pad&tracking_id=6b73fd7e-6d8f-47db-aad6-b154495173a4&is_advertising=true&ad_domain=VQCATCORE_LST&ad_position=1&ad_click_id=OWY1MDA1ZDYtMDk3Ny00MmNlLTk3NWYtN2E2OThjMjI1MGFj"
        # , "https://www.netshoes.com.br/whey-protein-top-whey-3w-mais-performance-900-g-max-titanium-baunilha-A05-0901-963"
         "https://www.maxtitanium.com.br/top-whey-3w-mais-performance-900g/p?idsku=106"
        # Dux Whey Protein Concentrado 900g
        # , "https://www.mercadolivre.com.br/suplemento-em-po-dux-nutrition-whey-protein-concentrado-proteinas-whey-protein-concentrado-sabor-baunilha-em-pote-de-900g/p/MLB15067109?pdp_filters=category:MLB264201#searchVariation=MLB15067109&position=4&search_layout=stack&type=product&tracking_id=35eb6593-f89f-41a8-bbe7-9d3f8e3546e7"
        # , "https://www.netshoes.com.br/whey-protein-concentrado-dux-nutrition-900g-cookies-AUF-1268-037"
        , "https://www.duxnutrition.com/wheyproteinconcentrado-pote900g/p?skuId=2967"
        # Integral Médica Whey 3W Super 907g
        # , "https://produto.mercadolivre.com.br/MLB-2652411790-super-whey-protein-3w-pote-907g-integralmedica-_JM?searchVariation=174551860029#searchVariation=174551860029&position=23&search_layout=stack&type=item&tracking_id=b6a1e379-69e7-46c2-ab69-339855cdec2e"
        # , "https://www.netshoes.com.br/whey-3w-super-907g-integralmedica-baunilha-MNH-1170-963"
        , "https://www.integralmedica.com.br/superwhey-3w/p"
        # Probiótica 3 Whey Protein 900g
        # , "https://produto.mercadolivre.com.br/MLB-2783564400-whey-3w-whey-protein-900g-probiotica-_JM?searchVariation=175166709480#searchVariation=175166709480&position=28&search_layout=stack&type=item&tracking_id=3f83bc49-5fb9-4b35-90ff-34797a4a5bf7"
        # , "https://www.netshoes.com.br/whey-protein-3w-900-g-probiotica-baunilha-168-0064-963"
        , "https://www.probiotica.com.br/3-whey-protein-pote-900g/p?skuId=57"
    ]

    def parse(self, response):
        # WheyProteinFile = open(f"WheyProtein.txt", "a")
        site = response.url

        print(f"\n\n\n\n\n\nAqui: {response.url}\n")
        if "mercadolivre" in site:
            marca = response.xpath('//*[@id="ui-pdp-main-container"]/div[1]/div/div[4]/div/div/div[1]/table/tbody/tr[1]/td/span')
            peso = response.xpath('//*[@id="ui-pdp-main-container"]/div[1]/div/div[4]/div/div/div[1]/table/tbody/tr[10]/td/span')
            produto = response.xpath('//*[@id="ui-pdp-main-container"]/div[1]/div/div[4]/div/div/div[1]/table/tbody/tr[3]/td/span')
            valor = response.xpath('//*[@id="ui-pdp-main-container"]/div[1]/div/div[1]/div[2]/div[3]/div[1]/span/span[3]')
            print(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "netshoes" in site:
            marca = response.xpath('//*[@id="features"]/ul/li[12]/a/text()')
            peso = response.xpath('//*[@id="features"]/ul/li[7]/text()')
            produto = response.xpath('//*[@id="features"]/ul/li[1]/text()')
            valor = response.xpath('//*[@id="buy-box"]/div[3]/p/span/span/text()')
            print(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')
        
        elif "maxtitanium" in site:
            marca = 'Max Titanium'
            peso = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/section/div/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[5]/div/div/div/div/div[2]/text()')
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[3]/section/div/div/div/div[8]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/div/p[1]/b/text()')
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[1]/div[9]/section/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/span/span/span/text()')
            print(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "duxnutrition" in site:
            marca = 'Dux Nutrition'
            peso = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/h1/span/text()')
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/h1/span/text()')
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[4]/div/div/div/section/div/div/div/div[2]/div/div/div[2]/div/div[4]/div/div/div/div/div[1]/div/div[2]/span/span/text()')
            print(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "integralmedica" in site:
            marca = 'Integral Medica'
            peso = response.xpath('/html/body/main/div[1]/div/div/div[2]/div/div[1]/div/ul[1]/li[2]/span/label[1]/text()')
            produto = response.xpath('/html/body/main/div[1]/div/div/div[1]/section[2]/div[3]/div/text()')
            valor = response.xpath('/html/body/main/div[1]/div/div/div[2]/div/div[2]/div[1]/div/p[1]/em[2]/strong/text()')
            print(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        elif "probiotica" in site:
            marca = 'Probiotica'
            peso = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/section/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[5]/div/div/div/div/div[1]/span/text()')
            produto = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/section/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div/div[1]/h1/span[1]/text()[1]/text()')
            valor = response.xpath('/html/body/div[2]/div/div[1]/div/div/div/div[3]/div/div[2]/div[2]/section/div/div/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/span/span/span/text()')
            print(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n\n\n\n\n\n')

        # WheyProteinFile.write(f'{datetime.today()};{marca};{peso};{produto};{valor};{site}\n')
        # WheyProteinFile.close()

