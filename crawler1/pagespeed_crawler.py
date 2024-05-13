"""
@manoel olegario 

05-02-2024
"""

from playwright.sync_api import sync_playwright
from time import sleep
from datetime import datetime
from schedule import run_pending, every
import psycopg2
import pygetwindow as gw
import settings

site_de_pesquisa = "https://www.site.com.br/" # aqui escolhemos o site que queremos analisar

def send_data(situacao, desempenho, acessibilidade, praticas_recomendadas, seo, empresa, situacao_mobile, desempenho_mobile, acessibilidade_mobile, praticas_recomendadas_mobile, seo_mobile, empresa_mobile):
    print('Acessando banco de dados...')
    # Dados de conexão com o banco de dados PostgreSQL
    user = settings.database['redshift']['USER']
    password = settings.database['redshift']['PASSWORD']
    host = settings.database['redshift']['HOST']
    port = settings.database['redshift']['PORT']
    database = settings.database['redshift']['NAME']
    schema = "bi"

    # Criar a conexão com o banco de dados
    conn_str = f"host={host} port={port} dbname={database} user={user} password={password}"
    conn = psycopg2.connect(conn_str)

    # Abrir um cursor para executar os comandos SQL
    cursor = conn.cursor()

    # Definir o código SQL para criar a tabela (somente se não existir)
    sql_script1 = f"""
    CREATE TABLE IF NOT EXISTS {schema}.desempenho_site2 (
        data_teste TIMESTAMP, 
        situacao VARCHAR(25),
        desempenho VARCHAR(5),
        acessibilidade VARCHAR(5),
        praticas_recomendadas VARCHAR(5),
        seo VARCHAR(5),
        empresa VARCHAR(50),
        situacao_mobile VARCHAR(25),
        desempenho_mobile VARCHAR(5),
        acessibilidade_mobile VARCHAR(5),
        praticas_recomendadas_mobile VARCHAR(5),
        seo_mobile VARCHAR(5),
        empresa_mobile VARCHAR(50)
    );
    """

    # Executar o script SQL
    cursor.execute(sql_script1)

    # Obter a data e hora atuais
    data_hora_atual = datetime.now()

    # Definir o código SQL para inserir os dados
    sql_script2 = f"""
    INSERT INTO {schema}.desempenho_site2 (data_teste, situacao, desempenho, acessibilidade, praticas_recomendadas, seo, empresa, situacao_mobile, desempenho_mobile, acessibilidade_mobile, praticas_recomendadas_mobile, seo_mobile, empresa_mobile)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    # Executar o script SQL para inserir os dados
    cursor.execute(sql_script2, (data_hora_atual, situacao, desempenho, acessibilidade, praticas_recomendadas, seo, empresa, situacao_mobile, desempenho_mobile, acessibilidade_mobile, praticas_recomendadas_mobile, seo_mobile, empresa_mobile))

    # Confirmar 
    # Confirmar as alterações no banco de dados
    conn.commit()

    # Fechar a conexão e o cursor
    cursor.close()

    print('Concluído!')



def func():
    with sync_playwright() as playwright: 
        try:
            print("Executando...")
            navegador = playwright.chromium.launch(headless=False) # criando o navegador - instância da lib (playwright)
            page = navegador.new_page() # criando a página no navegador
            try:
                window = gw.getWindowsWithTitle('Chromium')[0]  # isso pressupõe que a janela do OBS contém 'OBS' no título
                window.minimize()
            except IndexError:
                print("Janela não encontrada.")
            sleep(3) # aguradando para inserir o link da página
            page.goto('https://pagespeed.web.dev/') # link da página é inserido
            print("Link da página ok")
            sleep(3) # aguardando o carregamento da página
            input_busca = page.locator('#i4') # procurando o input para inserir o link
            input_busca.click(timeout=60000) # quando o input é entrado há uma simulação de click sobre ele
            input_busca.fill(site_de_pesquisa) # após o click é feita a inserção do link da embarca
            print("Link da Empresa ok")
            sleep(5) # aguardando o carregamento da página
            button_analisar = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/form/div[2]/button/span') # buscando o botão Analisar na página
            button_analisar.click(timeout=60000) # clicando no botão Analisar
            print("Botão Analisar ok")
            sleep(10) # aguardando o carregamento das informações

            sleep(10) # aguardando o carregamento das informações
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);") # rolando a página
            sleep(25) # aguardando 
            ##################### pegando os dados computador #############################
            situacao_mobile = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/span[1]').inner_text()
            desempenho_mobile = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[1]/div[2]').inner_text()
            acessibilidade_mobile = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[2]/div[2]').inner_text()
            praticas_recomendadas_mobile = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[3]/div[2]').inner_text()
            seo_mobile = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[2]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[4]/div[2]').inner_text()
            
            # pc
            page.evaluate('window.scrollTo(0, 0)') # voltando ao topo da página
            sleep(2)
            button_computador = page.locator('//*[@id="desktop_tab"]/span[2]') # Buscando o botão Computador
            button_computador.click(timeout=60000) # clicando no botão Computador
            print("Botão Computador ok")
            sleep(10) # aguardando o carregamento das informações
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);") # rolando a página
            sleep(25) # aguardando 
            ##################### pegando os dados mobile #############################
            situacao = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[3]/span/div/div[1]/div[2]/div[1]/div/div/div[1]/div/div/span[1]').inner_text()
            desempenho = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[3]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[1]/div[2]').inner_text()
            acessibilidade = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[3]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[2]/div[2]').inner_text()
            praticas_recomendadas = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[3]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[3]/div[2]').inner_text()
            seo = page.locator('//*[@id="yDmH0d"]/c-wiz/div[2]/div/div[2]/div[3]/div/div/div[3]/span/div/div[2]/div[2]/div/div/article/div/div[2]/div/div/div/div[2]/a[4]/div[2]').inner_text()

            send_data(situacao, desempenho, acessibilidade, praticas_recomendadas, seo,  "embarca.ai", situacao_mobile, desempenho_mobile, acessibilidade_mobile, praticas_recomendadas_mobile, seo_mobile, "embarca.ai")
            sleep(15)
        except Exception as erro:
            navegador.close()
            print(f"Erro: {erro}")


def main():
    func()
    print("Concluído...")
    
# schedule
every(30).minutes.do(main)

while True: # loop de controle da schedule
    run_pending() # run_pending realiza as tarefas do every a cada segundo
    sleep(1)

