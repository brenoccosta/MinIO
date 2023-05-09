# MinIO and Web Crawler Project
Este projeto foi desenvolvido no 1S/2023 para a matéria de Redes e Comunicação do curso de Ciência de Dados e Inteligência Artificial da PUC Campinas.

### Introdução
Este projeto visa desenvolver os estágios de captação, processamento e análise de dados.

A primeira etapa consiste no desenvolvimento de um *web crawler* desenvolvido com a biblioteca [scrapy](https://docs.scrapy.org/en/latest/) conforme este [tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html). Como fonte de dados utilizou-se o site do [Planalto](https://www.gov.br/planalto/pt-br) e captou-se dados da agenda presidencial.

Os dados captados são formatados em .csv e armazenados num servidor local de MinIO. Posteriormente, tais dados são normalizados e passados para uma base local de MySQL.

## Coleta de dados
### Inicializando o Scrapy
O projeto "Planalto" de *scrapy* extraiu as variáveis *datetime,  dia, mês, ano, dia da semana, hora, local e evento,* e foi inicializado pelo comando:

	scrapy startproject Planalto

No diretório onde se é executado, cria-se uma pasta homônima para o projeto. Outra, que contém o *crawler* e que também possui o mesmo nome, é criada dentro da do projeto, portanto originando algo como: `Planalto/Planalto/`. Quando se executa o *crawler*, seu *parser* guarda por padrão qualquer arquivo originado na pasta do projeto, portanto, em `Planalto/`, mesmo que ele em si esteja armazenado em `Planalto/Planalto/spiders/`.

O arquivo *agenda_spider.py* é o *crawler* desenvolvido para este projeto e sua consistência é bastante simples. A biblioteca *scrapy* funciona em cima de classes, e a deste projeto possui apenas como atributos seu nome, pelo qual será futuramente chamado, e as URLs que serão raspadas, neste caso, uma só; e como método, apenas o *parser*. Veja:

``` python
class AgendaSpider(scrapy.Spider):
	name = "agenda"
	start_urls = [
		'https://www.gov.br/planalto/pt-br'
	]

	def parse(self, response):
		# code
```

O método *parse* serve-se do HTML do site, passado pelo parâmetro *response*. Uma vez que um só site está sendo raspado, esse método será chamado uma única vez, e por estarmos coletando diversos dados, os laços de repetição foram construídos dentro do mesmo.

### Selecionando os dados
Sua construção foi simples. Acessando o site do [Planalto](https://www.gov.br/planalto/pt-br), vê-se logo a sessão "Agenda do Presidente da República", por padrão selecionada para o dia de hoje.

Assim, coletou-se os dados do mês e do ano do *datepicker*, enquanto o dia numérico e o dia da semana, da galeria de datas, utilizando para ambos os casos *xpath*, que localiza unicamente um elemento na página.

``` python
def parser(self, response):
	hoje = response.xpath('xpath')
	dia = hoje.css('css::text').get()
	diadasemana = hoje.css('css::text').get()
	ano = response.xpath('xpath/text()').get()
	mes = response.xpath('xpath/text()').get()
```

Para os compromissos presidenciais, que envolvem os dados de hora, local e evento, utilizou-se seleção por *css*, uma vez que todos os dados da **galeria** de compromissos devem ser coletados. O fato da mesma ser dinâmica reforça a necessidade do uso de um seletor não fixo, pois há dias sem compromissos por exemplo.

``` python
def parser(self, response):
	# code

	for div in response.css('css'):
		evento = div.css('css::text').get()
		local = div.css('css::text').get()
		hora = div.css('div.class::text').get()
```

### Coletando os dados
Para finalizar o *crawler* resta apenas indicar onde registrar as informações colhidas. Nesta solução o método *parser* abre um arquivo local em modo de *append* (escrita ao final) na pasta do projeto (`Planalto/`), registra os dados dentro do laço, e fecha-o, completando o método.

``` python
def parser(self, response):
	AgendaFile = open("AgendaPresidencial.txt", "a")
	
	# code

	for div in response.css('css'):
		# code
		
		AgendaFile.write(f'{dados};\n')

	AgendaFile.close()
```

E assim podemos abrir um terminal, também na pasta do projeto `Planalto/`, e rodar a seguinte linha de comando:

	scrapy crawl agenda

A biblioteca *scrapy* identifica, dentre todos os *crawlers* possíveis do projeto em questão, aquele que possui o nome idêntico ao passado. Vale lembrar que o primeiro atributo da nossa classe era: 

``` python 
name = "agenda" 
```

Permitindo a identificação do crawler desejado. Após a execução, deve-se verificar a presença do arquivo originado em `Planalto/AgendaPresidencial.txt`.

#### Periodicidade
Uma vez que o ambiente de execução está sendo uma máquina virtual Linux, fez-se uso do recurso do CRON.

## Armazenamento de dados
### MinIO
A raspagem de dados elaborada acima foi designada para operar continuamente, e num possível cenário de acúmulo de muitos dados, optou-se por servir-se do MinIO no gerenciamento de tais dados.

Por isso neste repositório há uma pasta nomeada `minio`, que nada mais é que o servidor local utilizado neste projeto **(observação: o ambiente de execução foi uma máquina virtual Ubuntu).**

>	Nota: [tutorial completo](https://min.io/docs/minio/linux/index.html).

Após a instalação, executa-se no terminal o seguinte comando, dentro deste repositório:

	minio server minio/ --console-address :9090

O primeiro termo chama o MinIO, indica que operar-se-á um servidor, a pasta na qual estará alocado e o endereço do mesmo, no caso, na máquina local. Por padrão retorna que o usuário e a senha são "minioadmin", que não foram alterados para este projeto. Basta abrir `localhost:9090` em seu navegador e já será possível acessar o servidor.


### Enviando dados para o servidor
Após criar-se um *bucket* chamado "planalto" para este projeto, que contém somente o arquivo AgendaPresidencial.txt, foi necessário encontrar uma maneira de, numa única execução, guardar os dados raspados no servidor ao invés de localmente na pasta do projeto `Planalto/`.

Primeiro houve tentativas de incluir dentro do *crawler* o acesso ao servidor, porém resultou em uma complexidade desnecessária para seu propósito, concluindo-se que a segunda opção era a mais adequada.

Uma vez que se deve executar na pasta `Planalto/` o comando `scrapy crawl agenda` pelo terminal e que se guarda o arquivo gerado no mesmo diretório, criou-se o arquivo AgendaCrawler.py nesse local, responsável por conectar-se ao MinIO e por chamar o *crawler*.

#### AgendaCrawler.py
O *script* python em questão é bastante simples e segue seis etapas nesta ordem:

1. Conexão com o cliente de MinIO
2. Declaração das variáveis (arquivo, bucket e *path*)
3. Download do arquivo
4. Execução do crawler por chamada de subprocesso
5. Upload do arquivo
6. Exclusão do arquivo local

Acompanhe abaixo o código de cada etapa:

``` python
def main():
    # Connecting with localhost
    client = Minio(
        "127.0.0.1:9000",
        access_key="minioadmin",
        secret_key="minioadmin",
        secure=False
    )
    print("Client connected")

    # Declaring main variables
    BucketName = "planalto"
    ObjectName = "AgendaPresidencial"
    FilePath = "AgendaPresidencialTESTE.txt"
    print("Variables declared")

    # Downloading file
    client.fget_object(BucketName, ObjectName, FilePath)
    print("File downloaded")

    # Appending to file
    subprocess.run("scrapy crawl agenda", shell=True)
    print("Crawler activated")

    # Uploading file
    client.fput_object(BucketName, ObjectName, FilePath)
    print("File uploaded")

    # Removing local file
    Path(FilePath).unlink()
    print("File deleted")
```

## Estruturando os dados com SQLite3