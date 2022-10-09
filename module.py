from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from time import sleep
import selenium.common.exceptions as exc


def criaDriver():
    opt = Options()
    opt.headless = False
    driver = webdriver.Chrome(executable_path = './chromedriver', options = opt)
    return driver, ActionChains(driver)

def tentaAcessarJogo(driver, action, jogo, lastDate):
    """Coleta a data do jogo, verifica se o jogo ocorreu após a data desejada e então acessa o jogo"""
    action.send_keys(Keys.ESCAPE).perform()
    data = driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/a/div[2]").get_attribute('innerHTML')
    data = datetime.strptime(data, "%d/%m/%Y")
    if(data > lastDate):
        action.send_keys(Keys.ESCAPE).perform()
        driver.find_element(By.XPATH, f"/html/body/div[3]/div/main/div[4]/div/div/div[1]/div/div[2]/div[{jogo}]/div/div/div/div/div[2]/a").click()
        sleep(1)
        return 1, data
    return 0, data

def acessaJogo(driver, action, jogo, lastDate):
    try:
        Jogo, dataJogo = tentaAcessarJogo(driver, action, jogo, lastDate)
    except exc.NoSuchElementException or exc.ElementClickInterceptedException:
        sleep(1)
        action.send_keys(Keys.ESCAPE).perform()
        Jogo, dataJogo = tentaAcessarJogo(driver, action, jogo, lastDate) 
    return Jogo,dataJogo

def acessaEscalação(driver,action, Time):
    """Acessa a escalação detalhada e adentra o time em questão"""
    resultado = driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[3]/div/div[1]").text.split("\n")
    driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[3]/div/div[2]/div[8]/div/div[2]/a").click()
    sleep(1)
    Home = driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[1]/div/div[1]")
    if(Home.text == Time):
        Home.click()
        sleep(0.5)
    else:
        driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[1]/div/div[2]").click()
        sleep(0.5)
    return resultado[0] + " " + resultado[2] + "x" + resultado[4] + " " + resultado[6]

def acessaJogadores(driver, action, file, atributos, dadosJogo):
    driver.find_element(By.XPATH, "/html/body/div[3]/div/main/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div[2]").click()
    for _ in range(1,18):
        try:
            driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div[1]/div[2]/div[1]/span/div").get_attribute('innerHTML')
            coletaDados(driver, file, atributos, dadosJogo)
            action.send_keys(Keys.RIGHT).perform()
        except exc.NoSuchElementException:
            break        
    
def entreJogos(driver, action):
    driver.back()
    driver.back()
    sleep(0.5)
    action.send_keys(Keys.ESCAPE).perform()

def coletaInicial(driver):
    stats = {}
    stats["Nome"] = driver.find_element(By.XPATH, f"/html/body/div[4]/div/div[2]/div/div[1]/div[2]/div[1]/div").text
    nota = driver.find_element(By.XPATH, f"/html/body/div[4]/div/div[2]/div/div[1]/div[2]/div[1]/span/div").text
    if("-" != nota):
        stats["Nota"] = nota
    stats["Posição"] = driver.find_element(By.XPATH, f"/html/body/div[4]/div/div[2]/div/div[1]/div[2]/div[2]").text
    return stats

def escreveDados(file, dados, atributos, dadosJogo):
    file.write(dadosJogo[0].strftime("%d/%m/%Y") + ";" + dadosJogo[1])
    for i in atributos[2:]:
        try:
            file.write(';' + dados[i])
        except KeyError:
            file.write(';')
    file.write("\n") 

def coletaDados(driver, file, atributos, dadosJogo):
    stats = coletaInicial(driver)
    primeiroBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div[2]/div[1]").text.split("\n")
    segundoBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div[2]/div[2]").text.split("\n")
    terceiroBloco = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div[2]/div[3]").text.split("\n")
    
    stats[primeiroBloco[2]] = primeiroBloco[1][:-1]
    stats[primeiroBloco[4]] = primeiroBloco[3][0]
    stats[primeiroBloco[6]] = primeiroBloco[5]
    stats['Area'] =  segundoBloco[0]
    for i in range(1, len(segundoBloco), 2):
        stats[segundoBloco[i]] = segundoBloco[i+1]
    for i in range(1, len(terceiroBloco), 2):
        if(terceiroBloco[i] != "Assistências"):
            stats[terceiroBloco[i]] = terceiroBloco[i+1]
        else:
            stats["Assist."] = terceiroBloco[i+1]
    escreveDados(file, stats, atributos, dadosJogo)