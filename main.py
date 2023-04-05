# ----------------------INSTALAÇÕES -------------------------------------------------
'''
Para instalar as bibliotecas necessárias use o arquivo requirements.txt (disponibilizado
junto com o projeto) coloque-o na mesma pasta do main.py e digite no terminal do pycharm:
pip install -r requirements.txt

(OBS: O arquivo conta também com as bibliotecas extras do ambiente virtual, mas não serão instaladas
caso já existente)

O caminho do main.py (mesma do requerimento) deve ser:
k:\ProjetosPython\Projetos\Desafio\DanielAmorim
é no main.py do pycharm que este código deve ser colado (limpar o main.py antes).
'''

# ----------------------CONSIDERAÇÕES------------------------------------------------
'''
 Para evitar block e cair na tela de login usei navegador anônimo e useragent.
 Cada nova leitura de dado na página aguarda um tempo ramdomico para evitar bloqueio.
 Na nova versão do webdriver não precisa baixar o cromedriver, automaticamente será
 instalado de acordo com a versão do seu navegador, única exigência é usar com 
 selenium 4 que já será instalado com o requeriments.

 O web scraping roda sem interferência humana, porém se ocorrer algum erro seja por conexão com
 internet ou queda de energia uma tela será apresentada na próxima utilização perguntando
 se quer continuar de onde parou ou reiniciar toda a busca, entenda:

 - REINICIAR: Limpa os dados temporários salvos e exclui o CSV, para criar um novo arquivo de buscas.
 - CONTINUAR: Refaz o filtro na página da busca e continua a busca de onde parou.

 O programa tenta simular a manipulação humana no site para evitar bloqueio, por este motivo as etapas
 são realizadas lentamente na medida do possível. 

 O Linkedin, mesmo com os cuidados, bloqueia facilmente a página dos contratantes, o que pode
 gerar a falta dos dados como (Número de funcionários, seguidores e local sede).
'''
# ----------------------BIBLIOTECAS -------------------------------------------------

# Selenium e Wd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


servico = Service(ChromeDriverManager().install())

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Espera do webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# User agent para tentar minimizar bloqueios usando agent randomico
from fake_useragent import UserAgent
user_agent = UserAgent().random

# Configurar as opções do Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(f'user-agent={user_agent}')
# Para sair da janela anônima comente abaixo
chrome_options.add_argument("--incognito")

# Criar uma instância do driver do Chrome com as opções configuradas
navegador = webdriver.Chrome(service=servico, options=chrome_options)

# mais algumas bibliotecas
import pandas as pd
import time
from datetime import datetime
import random
import os
import tkinter as tk
import sys


# -------------- DEFININDO AS VARIÁVEIS -----------------------------------------------------

wait_time = 5  # Tempo de espera do webdriverwait
wait = WebDriverWait(navegador, wait_time)

pais_busca = "brasil"
vaga_busca = "marketing+e+publicidade"
link_da_busca = "https://www.linkedin.com/jobs/search?position=1&pageNum=0"

# local e nome dos arquivos
arq_scraping = "Scraping - Daniel de Souza Amorim.csv"
arq_print = "Filtros do linkedin - Daniel de Souza Amorim.png"

# time randomico entre 1, 5
tempo_random = random.uniform(1, 3)

# ------------------DEFININDO CLASSES E FUNÇÕES -------------------

# CLASSE PAI: CLASSE CONSTRUTORA
class Acao_elementos:

    def __init__(self, elemento, cmd_do_key):
        self.elemento = elemento
        self.cmd = cmd_do_key
        if cmd_do_key == "click":
            time.sleep(tempo_random)
            self.elemento.click()
        else:
            time.sleep(tempo_random)
            self.elemento.send_keys(self.cmd)

# CLASSE FILHA: USADO SOMENTE PARA EXEMPLIFICAR USO DE CLASSE COM HERANÇA
class Execute(Acao_elementos):
    def __init__(self, elemento , cmd_list):
        for cmd in cmd_list:
            super().__init__(elemento, cmd)

# FUNÇÃO FILTRA VAGAS NA TELA PRNCIPAL
def filtrar_vaga(contador):
    try:
        # PREENCHE PAIS
        elemento = navegador.find_element(By.ID, 'job-search-bar-location')
        cmd_list = [Keys.ESCAPE, pais_busca, Keys.ARROW_DOWN, Keys.ENTER]
        Execute(elemento, cmd_list)
        # PREENCHE NOME DA VAGA
        elemento = navegador.find_element(By.ID, "job-search-bar-keywords")
        cmd_list = [Keys.ESCAPE, vaga_busca, Keys.ENTER]
        Execute(elemento, cmd_list)
        # SELECIONA TEMPO INTEGRAL
        navegador.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[4]/div/div/button').click()
        elemento = navegador.find_element(By.ID, 'f_JT-0')
        cmd_list = ["click", Keys.ENTER]
        Execute(elemento, cmd_list)
        # SELECIONA ESTÁGIO
        navegador.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[5]/div/div/button').click()
        elemento = navegador.find_element(By.ID, 'f_E-0')
        cmd_list = ["click", Keys.ENTER]
        Execute(elemento, cmd_list)
        # PRINT SCREEN DO FILTRO
        navegador.save_screenshot(arq_print)
        time.sleep(1)
        return
    except:
        if contador < 3:
            navegador.get(link_da_busca)
            contador += 1
            print(f"Tentativa {contador} falhou, tentando novamente...")
            filtrar_vaga(contador)
            return
        else:
            print("Site bloqueou o scraping, tente mais tarde!")
            navegador.close()
            sys.exit(1)

# FUNÇÃO DA JANELA OPÇÃO REINICIAR
def resposta_reiniciar():
    # Remover o arquivo
    try:
        print(f"Arquivos de backup foram removidos, recomeçando a busca...")
        os.remove(arquivo_temp)
        os.remove('temp_data.txt')
        # Try por causa deste arquivo que não é sempre criado
        os.remove(arq_scraping)
        time.sleep(1)
        janela.destroy()
        return
    except:
        time.sleep(1)
        janela.destroy()
        return


# FUNÇÃO DA JANELA OPÇÃO CONTINUAR
def resposta_sim():
    print("Continuando de onde parou... aguarde")
    janela.destroy()
    return


# VERIFICA SE EXISTE TEMP, SE SIM ABRE A JANELA DE OPÇÕES
arquivo_temp = "temp_progress.txt"

# JANELA DE OPÇÕES DO TKINTER
if os.path.exists(arquivo_temp):
    janela = tk.Tk()
    janela.title("Escolha uma opção")
    janela.geometry("320x155")

    # LABEL
    label = tk.Label(janela, text="Continuar a busca de onde parou?\n \n"
                                  "ATENÇÃO: Se reiniciar, excluirá o arquivo CSV da busca\n"
                                  "e recomeçará todo o processo.")
    label.pack(pady=10)
    # FRAME
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)
    # BOTÕES
    botao_sim = tk.Button(frame_botoes, text="Continue", width=10, command=resposta_sim)
    botao_sim.pack(side="right", padx=10)
    botao_nao = tk.Button(frame_botoes, text="Ok, reinicie!", width=10, command=resposta_reiniciar)
    botao_nao.pack(side="left", padx=10)
    # TAMANHO DA JANELA
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    # CENTRO D TELA
    x = (screen_width - janela.winfo_reqwidth()) / 2
    y = (screen_height - janela.winfo_reqheight()) / 2
    # CENTRALIZANDO A JANELA
    janela.geometry("+%d+%d" % (x, y))
    janela.mainloop()


# SCROLL NA PÁGINA
def scroll_ate_ttl_vagas(qnt_de_vagas, element_de_vagas):
    '''
    Função executa scroll na página atá que a quantidade de elementos
    correspondam a mesma quantidade de vagas disponíveis.
    '''
    while float(qnt_de_vagas) >= int(len(element_de_vagas)):
        # executar um script JavaScript para fazer o scroll na página
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(tempo_random)  # aguardar a página carregar
        # página estava bloqueando scroll persistente pra baixo, resolvi com um pequeno scroll pra cima
        navegador.execute_script("window.scrollBy(0, -60)")

        element_de_vagas = navegador.find_elements(By.CLASS_NAME, "job-search-card")
        qnt_de_vagas = navegador.find_element(By.CLASS_NAME, "results-context-header__job-count").text

        # Botao ver mais
        mais = navegador.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button")
        if mais.text == "Ver mais vagas":
            # se botão "Ver mais vagas" presente, clica para continua o scroll
            mais.click()
            time.sleep(1)

        # aviso fim
        aviso_fim = navegador.find_element(By.CLASS_NAME, "inline-notification__text")
        if aviso_fim.text == "Você viu todas as vagas para esta pesquisa":
            break

    return element_de_vagas


# PEQUENO SCROLL FAKE PARA SIMULAR USUÁRIO NA PÁGINA E EVITAR BLOCK
def scroll_fake():
    navegador.execute_script("window.scrollBy(0, 400)")
    return

# SALVANDO ARQUIVO CSV
def salvar_csv(resultados):
    lista_da_busca = pd.DataFrame(resultados, columns=["Url vaga Linkedin", "Nome da vaga", "Empresa contratante",
                                                       "URl empresa contratante",
                                                       "Tipo contratação", "Nível experiência",
                                                       "Número de candidaturas", "Data postagem vaga",
                                                       "Horário scraping", "Quantidade funcionários",
                                                       "Quantidade seguidores", "Local sede", "Url candidatura"])
    lista_da_busca.to_csv(arq_scraping, encoding='ANSI', sep=';', index=False)
    return

# LISTAS
tupla_resultados = []
lista_vaga_ja_lida = []

# ABRE ARQUIVO OU CRIA O TEMP_DATA
with open('temp_data.txt', 'a+') as d:
    # Move o cursor para o início do arquivo
    d.seek(0)
    for linha in d:
        tupla_resultados.append(eval(linha))

salvar_csv(tupla_resultados)

# ABRE ARQUIVO OU CRIA O TEMP_PROGRESS
with open('temp_progress.txt', 'a+') as p:
    # Move o cursor para o início do arquivo
    p.seek(0)
    for linha in p:
        lista_vaga_ja_lida.append(linha.replace("\n", ""))

print('Quantidade de vagas já analisadas:', len(lista_vaga_ja_lida))


indice_ult = int(len(lista_vaga_ja_lida))

if indice_ult == 0:
    # ABRE O NAVEGADOR NO LINK DA BUSCA
    navegador.get(link_da_busca)
    time.sleep(2)


    # CHAMA FUNÇÃO FILTRAR VAGAS
    contador = 0
    filtrar_vaga(contador)
    # PEGA URL DO FILTRO
    url_do_filtro = navegador.current_url
    # Salva progresso de leitura
    with open('temp_progress.txt', 'a') as f:
        f.write(f'{url_do_filtro}' + '\n')
else:
    url = lista_vaga_ja_lida[0]
    navegador.get(url)

# PEGA ELEMENTOS QUE CONTÉM AS VAGAS (auxilia no scroll até o fim da página)
element_de_vagas = navegador.find_elements(By.CLASS_NAME, "job-search-card")
qnt_de_vagas = navegador.find_element(By.CLASS_NAME, "results-context-header__job-count").text
time.sleep(1)

# SCROLL NA PÁGINA
try:
    element_de_vagas = scroll_ate_ttl_vagas(qnt_de_vagas, element_de_vagas)
except:
    print("Site bloqueou o scraping, tente mais tarde!")
    navegador.close()
    sys.exit(1)

print(f"Encontramos {len(element_de_vagas)} em {vaga_busca}, iniciando...")

# VERIFICA ULTIMO ÍNDICE DA VAGA LIDA E CONTINUA OU INICIA
indice_ult = int(len(lista_vaga_ja_lida))

# INICIA CAPTURA DE DADOS
for elem in element_de_vagas[indice_ult:]:

    indice_ult += 1
    print("--------------------------------------------------")

    # Salva progresso de leitura
    with open('temp_progress.txt', 'a') as f:
        f.write(f'{indice_ult}' + '\n')

    time.sleep(1)
    try:
        # clica em um elemento da lista para exibir o painel de informações
        scroll_fake()
        elem.click()
        time.sleep(tempo_random)

        # Usando o webdriverwait para ver se link abre (se não abrir pula busca)
        condicao = EC.visibility_of_element_located((By.CLASS_NAME, "num-applicants__caption"))
        retorno = wait.until(condicao)
        candidatos = retorno.text
        print("QNT candidatos: ", candidatos)

        titulo_vaga = elem.find_element(By.CLASS_NAME, 'sr-only').text
        print("Titulo vaga:", titulo_vaga)

        contratante = elem.find_element(By.CLASS_NAME, "hidden-nested-link").text
        print("Contratante: ", contratante)

        data_anuncio = elem.find_element(By.TAG_NAME, "time").get_attribute("datetime")
        print("Data anuncio: ", data_anuncio)

        link_contr = elem.find_element(By.CLASS_NAME, "hidden-nested-link").get_attribute("href")
        print("Link contratante: ", link_contr)

        link_vaga = elem.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")
        print("Link vaga: ", link_vaga)

        # Pega elementos do painel de vagas principal
        painel_dados = navegador.find_elements(By.CLASS_NAME, 'details-pane__content')
        time.sleep(2)

        for el in painel_dados:

            box_elem = navegador.find_element(By.CLASS_NAME, "description__job-criteria-list")

            lista_tags = box_elem.find_elements(By.TAG_NAME, "span")

            n_exp = str(lista_tags[0].text)
            print("Nivel experiencia: ", n_exp)
            t_contrato = str(lista_tags[1].text)
            print("Tipo contrato: ", t_contrato)

            time.sleep(2)
            # Clica no botão para inscrição na vaga
            btn_vaga = el.find_element(By.CLASS_NAME, "sign-up-modal__outlet").click()
            time.sleep(2)

            # identifica e fecha popup (ao fechar, automáticamente abre a janela de candidatura)
            pop1 = navegador.find_element(By.XPATH, '//*[@id="sign-up-modal"]/div/section')
            pop1.send_keys(Keys.ESCAPE)
            time.sleep(2)

            # switch para a janela de candidatura
            navegador.switch_to.window(navegador.window_handles[1])
            url_candidatura = navegador.current_url
            print("Link candidatura:", url_candidatura)
            # fecha janela de candidatura
            time.sleep(2)
            navegador.close()

            # switch para janela principal
            navegador.switch_to.window(navegador.window_handles[0])
            time.sleep(2)

            # Para pegar o link da empresa se referenciando com o children para pegar o link no parent
            filho = el.find_element(By.TAG_NAME, "img")
            pai = filho.find_element(By.XPATH, "..")
            link_empresa = pai.get_attribute("href")

            # TRY se fez necessário aqui pois se linkedin bloquear/pedir login nesta etapa
            # ignoro somente estes dados (salva N/I não informado) mas grava no CSV os dados anteriores
            try:
                '''
                O linkedin bloqueia muito esta página que vai abrir a partir deste bloco ou alguns links
                quebrados, então esse try ignora caso aconteça não perco os dados anteriores e os dados desta página
                eu salvo como não informado.
                '''
                # Abrir janela com link da empresa (qnt func e qnt seguidores)
                navegador.execute_script(f"window.open('{link_empresa}', 'new_window')")
                time.sleep(4)

                # Switch para a janela da empresa
                navegador.switch_to.window(navegador.window_handles[1])
                time.sleep(2)

                # Fecha o popup
                pop2 = navegador.find_element(By.TAG_NAME, "button")
                pop2.send_keys(Keys.ESCAPE)
                time.sleep(1)

                # Scroll fake e tempor random pra simular manipulação humana
                # essa página da empresa é onde mais ocorrem os bloqueios
                scroll_fake()
                time.sleep(tempo_random)

                # Buscar elementos na página da empresa
                tela_empresa = navegador.find_elements(By.CLASS_NAME, 'core-rail')
                for el in tela_empresa:
                    tela = el.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[3]')
                    func = tela.text
                    func = func.replace("\n", "").strip()
                    funcionarios = func.replace("Tamanho da empresa", "")
                    print("QNT Funcionários: ", funcionarios)

                    segs = navegador.find_element(By.CLASS_NAME, "top-card-layout__first-subline")

                    lista_result = segs.text.split(" ")
                    seguidor = lista_result[-2]
                    print("QNT Seguidores: ", seguidor)

                    lista_cidade = lista_result[:-2]
                    local = " ".join(lista_cidade)
                    print("Local: ", local)
                time.sleep(5)
                # Fecha janela da empresa
                navegador.close()
                # Retorna para janela principal
                navegador.switch_to.window(navegador.window_handles[0])
                pass
            except Exception as error:
                navegador.close()
                # Retorna para janela principal
                navegador.switch_to.window(navegador.window_handles[0])
                # seta variáveis como nao informado (caso página contratante bloqueada)
                funcionarios = "N/I"
                seguidor = "N/I"
                local = "N/I"
                print("*** Alguns dados não disponíveis o site bloqueou link!")
                continue

        time_sys = datetime.now()
        hora_scraping = f'{time_sys.hour}:{time_sys.minute}h - {time_sys.day}/{time_sys.month}/{time_sys.year}'
        print("Hora scraping: ", hora_scraping)

        tupla_resultados.append((link_vaga, titulo_vaga, contratante, link_empresa, t_contrato, n_exp, candidatos,
                                 data_anuncio, hora_scraping, funcionarios, seguidor, local, url_candidatura))

        # Salva dados da vaga no arquivo temporário
        with open('temp_data.txt', 'a') as g:
            g.write(
                f'{(link_vaga, titulo_vaga, contratante, link_empresa, t_contrato, n_exp, candidatos, data_anuncio, hora_scraping, funcionarios, seguidor, local, url_candidatura)}' + '\n')
        pass

        # Chama função para salvar o CSV
        salvar_csv(tupla_resultados)

    except Exception as error:
        # se o link do elemento não abrir ignora esse elemento e continua no próximo
        print("Link não respondeu, inexistente ou bloqueado, indo pro próximo...")
        continue

    time.sleep(tempo_random)

print("-----------------------------------")
print("Scraping chegou ao FIM!")
print("Todas as vagas já foram adicionadas ao arquivo CSV.")
print("Para uma nova consulta click em reiniciar na janela apresentada.\n"
      "ATENÇÃO: Ao reiniciar, o CSV será excluido, caso queira salvar-lo\n"
      "copie o arquivo CSV para outro local antes de iniciar uma nova busca.")
