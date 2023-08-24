import requests
import json

import os
import sys
import io
import threading

import ctypes
import contextlib
import keyboard

class program:
    def read_json_file(file): #abrir arquivo json contendo a requisição.
        
        config_name = 'reqs'
           
        if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
            # Executando como executable (PyInstaller)
            path = os.path.dirname(sys.executable)
        else:
            # Executando como  script .py
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
            
        filename = os.path.join(path, config_name+ "\\" + file)           
        
        try:
            if not os.path.exists(filename):
                os.system('cls')
                print("No such file or directory: " + filename) #erro se o arquivo nao existir.
            
            else: #ATUALIZADO PARA MOSTRAR DADOS COM QUEBRA DE LINHA.
                with contextlib.ExitStack() as stack:
                    file = stack.enter_context(io.open(filename, mode='r', encoding='utf-8', errors='ignore'))
                    data = json.load(file) #chave methods e IP são usados apenas no contexto deste app cliente para se referir ao IP/Porta, o servidor não usa esse valores.
                    
                    if data['method'] == "GET": #MÉTODOS SÃO SELECIONADOS A PARTIR DO ARQUIVO JSON NA PASTA REQUESTS.
                        response = requests.get(data['IP'], json=data)

                        os.system('cls')
                                                
                        for x in (response.json())['Values']:
                            print(x)
                            
                        print("\nScroll up to see the entire DataFrame.")
                    
                    elif data['method'] == "PUT":
                        response = requests.put(data['IP'], json=data)
                        
                        os.system('cls')
    
                        for x in (response.json())['Values']:
                            print(x)
                            
                        print("\nScroll up to see the entire DataFrame.")
                    
                    elif data['method'] == "POST":
                        response = requests.post(data['IP'], json=data)
                        
                        os.system('cls')
                        
                        for x in (response.json())['Values']:
                            print(x)
                            
                        print("\nScroll up to see the entire DataFrame.")
                    
                    elif data['method'] == "DELETE":
                        response = requests.delete(data['IP'], json=data)
                        
                        os.system('cls')
                        
                        for x in (response.json())['Values']:
                            print(x)
                            
                        print("\nScroll up to see the entire DataFrame.")
                    
                    else: #ERRO SE NENHUM DOS 4 MÉTODOS FOREM USADOS.
                        os.system('cls')
                        print("\nUnknown method.")
            
        except Exception as e:
            #os.system('cls')
            print(e)
            
        
        finally:
            App = program() #REINICIA TODO O APP QUANDO TUDO TERMINAR.
    
            Listener = threading.Thread(target=Interact)
            Listener.start()
            
    
    def __init__(self):
        print("\n=================== | API_Client_V1 | ===================\n") #TELA DE BOAS VINDAS.
        print("Choose an option: \n")
        print("1 - Run through the request json file: 'Type filename'.")
        print("2 - Exit\n")
            
class Interact:
    def read_key(): #CAPTURA O QUE O USUÁRIO DIGITA NO TECLADO.
        event = keyboard.read_event()
        return event.name
    
    def __init__(self): #INICIA LOOP: AGUARDANDO INTERAÇÃO DO USUÁRIO.
        while True:
            self.key = Interact.read_key()
                    
            try:
                if self.key == "esc":
                    os.system('cls')
                    
                    break
        
                elif self.key == '1': #OPÇÃO QUE INICIA INTERAÇÃO COM O SERVIDOR HTTP.
                    program.read_json_file(input("Type the filename including the extension: "))
                    
                    break
                
                elif self.key == '2':
                    os.system('cls')
                    
                    break

            except KeyboardInterrupt:
                break
        
if __name__ == "__main__":
    myappid = 'Suundumused.API_Client.API_Client.1' #Anexa id do desenvolvedor no processo.
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    App = program()
    
    Listener = threading.Thread(target=Interact) #instancia processo de captura de chaves.
    Listener.start()
