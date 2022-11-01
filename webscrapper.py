from selenium.webdriver.common.by import By
from datetime import datetime
import module

url = tuple(['https://www.365scores.com/pt-br/football/england/manchester-united/team/105#results','https://www.365scores.com/pt-br/football/spain/real-madrid/team/131#results',
            'https://www.365scores.com/pt-br/football/england/liverpool/team/108#results', 'https://www.365scores.com/pt-br/football/germany/bayern-munich/team/331#results', 
            'https://www.365scores.com/pt-br/football/france/psg/team/480#results', 'https://www.365scores.com/pt-br/football/italy/juventus/team/226#results',
            'https://www.365scores.com/pt-br/football/england/manchester-city/team/110#results', 'https://www.365scores.com/pt-br/football/spain/fc-barcelona/team/132#results', 
            'https://www.365scores.com/pt-br/football/spain/atletico-madrid/team/134#results'])
Time = tuple(["Man Utd", "Real Madrid", "Liverpool", "Bayern de Munique", "PSG", "Juventus", "Man City", "FC Barcelona", "Atl. Madrid"])

Atributos = tuple(["Data", "Partida", "Nome", "Nota", "Area", "Posição", "Min", "Gols", "Assist.", "Pênalti recebido", 
                "Total de chutes", "Chutes no gol", "Chutes para fora", "Trave", "Chutes interceptados", "Chances perdidas", 
                "Impedimentos", "Passes decisivos", "Quase gol", "Passes completados", "Passes longos completados", 
                "Cruzamentos completos", "Dribles completos", "Toques", "Faltas recebidas", "Pênalti cometido", "Faltas cometidas", 
                "Posse de bola perdida", "Driblado", "Perigo afastado", "Interceptações", "Bolas recuperadas", 
                "Vitória em duelos por baixo", "Vitória em duelos por cima", "Defesas", "Gols sofridos", "Pênalti defendido",
                "Reposição de soco", "Erros que terminaram em chute adversário", "Defesa pelo alto"])

f_temp = open("a.txt", "w")

for i in range(len(Time)):
    # Criando variáveis e configurações iniciais
    driver, actions = module.criaDriver()
    driver.get(url[i])
    driver.find_element(By.XPATH, "//button[@id = 'didomi-notice-agree-button']").click()
    j=1
    while(True):
        # Acessando um jogo específico
        dataLimite = datetime(2022, 8, 2)
        jogo, dataJogo = module.acessaJogo(driver, actions, j, dataLimite)
        if(jogo == 1):
            resultado = module.acessaEscalação(driver, actions, Time[i])
            module.acessaJogadores(driver, actions, f_temp, Atributos, [dataJogo, resultado])
            module.entreJogos(driver, actions)
            j += 1
        elif(jogo == 2):
            j += 1
        else:
            break
    
    driver.close()
f_temp.close()

module.adiciona()