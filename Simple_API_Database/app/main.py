from flask import *

from waitress import serve

import os
import sys

import ctypes
import argparse

config_name = 'templates'
           
if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
    # Executando como executable (PyInstaller)
    path = os.path.dirname(sys.executable)
else:
    # Executando como  script .py
    path = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.insert(1, os.path.join(path, config_name))
import Routes #Carrega script com as rotas.

class program:
    def __init__(self, app, routes):
        
        self.parser = argparse.ArgumentParser(  #descrição do app
        description='My API Server',
        epilog="Started!")
    
        self.parser.add_argument("-ip","--host", help="Set/Get Local IPV4, default = '0.0.0.0'", type=str, default="0.0.0.0")#criar argumento alterar ip
        self.parser.add_argument("-p","--port", help="Set Port Forwarding, default = 8080", type=int, default=8080) #alterar porta
    
        self.args = self.parser.parse_args()
    
        if self.args.host == "0.0.0.0":
            print("Server running Forwarded at: " + str(self.args.port))
    
        else:
            print("Server running at: " + str(self.args.host) + ":" + str(self.args.port))
    
        try:
            #app.run(debug=True, threaded=True, port=args.port) #testes apenas.
            serve(app, host=self.args.host, port=self.args.port) #inicia o servidor em modo distribuição.
        
        except Exception as e:
            print(e)
            
            exit()
    
if __name__ == "__main__":
        
    config_name = 'templates'
           
    if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
        # Executando como executable (PyInstaller)
        path = os.path.dirname(sys.executable)
    else:
        # Executando como  script .py
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
            
    template_folder1 = os.path.join(path, config_name)
        
    app = Flask(__name__, template_folder=template_folder1) #AJUSTA A PASTA TEMPLATES
    
    app.config['JSON_SORT_KEYS'] = False #desativar ordem alfabética
    
    myappid = 'Suundumused.SimpleAPI.SimpleAPI.1' #Anexa id do desenvolvedor no processo.
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    routes = Routes.Routes(app) #carrega as rotas.
    program = program(app, routes) #incia o servidor.