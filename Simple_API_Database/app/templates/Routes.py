from flask import *

import sys
import os

config_name = 'Data'
           
if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
    # Executando como executable (PyInstaller)
    path = os.path.dirname(sys.executable)
else:
    # Executando como  script .py
    path = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.insert(1, os.path.join(path, config_name))
import Connector #Carrega script que faz a leitura/escrita de arquivos.

class Protection:
    def antiescape(Paths): #Proteja as pastas anteriores a pasta alvo para que não seja acessada por meio de parâmetros de escape.
        Filter = [r"cd", r"../", r"./", r".\\", r"..\\", r"~", r"..", r"cd..",
                  r"cd /", r"cd/", r"cd ..", r"cd.", r"cd .", r". .", r"cd \\", r"cd\\" , r"%", r"¨"]

        Found = False

        try:
            for word in Filter:
                if Paths.find(word) != -1:
                    Found = True

            if Paths.find("..\\") != -1 or Paths.find(".\\") != -1 or Found == True:
                return True

            else:
                return False

        except Exception as e:
            return True

class Routes:
    def __init__(self, app):
        
        config_name = 'storage'
           
        if getattr(sys, 'frozen', False):  #-----ATUALIZADO-----
            # Executando como executable (PyInstaller)
            path = os.path.dirname(sys.executable)
        else:
            # Executando como  script .py
            path = os.path.dirname(os.path.abspath(sys.argv[0]))
        
        self.storage = os.path.join(path, config_name) #define a pasta local onde os arquivos serão manipulados.
        
        @app.errorhandler(415)
        def unsupported_media_type(error):
            return jsonify({'Values': ["Unsupported Media Type."]}), 415
        
        @app.errorhandler(500)
        def bad_request(error):
            return jsonify({'Values': ["Critical Unknown Error."]}), 500
        
        @app.route('/ls', methods=['GET']) #lista de arquivos.
        def ls():
            if request.method == 'GET':
                try:
                                    #lista de arquivos.
                    return jsonify({'Values': os.listdir(self.storage)}), 200
                
                except Exception as e:
                    error_message = repr(e)
                    
                    return jsonify({'Values': ["{}".format(error_message)]}), 500                
            else:
                return jsonify({'Values': ["Wrong method"]}), 401
            
        @app.route('/touch', methods=['POST']) #cria/sobrescreve arquivo com conteúdo.
        def touch():
            if request.method == 'POST':
                data = request.get_json()
            
                FileName = data.get('database' )#carrega variável do json requisição do cliente.
                Content = data.get('content')
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify({'Values': ["Access Violation."]}), 403
                
                 #cria/sobrescreve arquivo com conteúdo.
                
                return Connector.ReadWrite.make_file(self.storage+"/"+FileName, Content) #retorna o novo conteúdo do arquivo.
                
            else:
                return jsonify({'Values': ["Wrong method"]}), 401
            
        @app.route('/nano', methods=['PUT', 'DELETE']) #editar linha arquivo específico
        def nano():
            if request.method == 'PUT':
                data = request.get_json()
            
                FileName = data.get('database') #carrega variável do json requisição.
                RemoveValue = False
                Column = data.get('column')
                Line = data.get('line')
                Content = data.get('content')
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify({'Values': ["Access Violation."]}), 403
                
                return Connector.ReadWrite.edit_db(self.storage+"/"+FileName, Column, Line, Content, RemoveValue)
                
            elif request.method == 'DELETE':                
                data = request.get_json()
            
                FileName = data.get('database') #carrega variável do json requisição.
                RemoveValue = True
                Column = data.get('column')
                Line = data.get('line')
                Content = data.get('content')
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify({'Values': ["Access Violation."]}), 403
                
                return Connector.ReadWrite.edit_db(self.storage+"/"+FileName, Column, Line, Content, RemoveValue)
            
            else:
                return jsonify({'Values': ["Wrong method"]}), 401
        
        @app.route('/cat', methods=['GET']) #ler arquivo específico
        def cat():
            if request.method == 'GET':
                data = request.get_json()
                
                FileName = data.get('database') #carrega variável do json requisição.
                Range = data.get('Range')
                column = data.get("column")
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify({'Values': ["Access Violation."]}), 403
            
                return Connector.ReadWrite.read_file(self.storage+"/"+FileName, Range, column) #retorna o novo conteúdo do arquivo.
            
            else:
                return jsonify({'Values': ["Wrong method"]}), 401
            
        @app.route('/rm', methods=['DELETE']) #remove arquivo.
        def rm():
            if request.method == 'DELETE':
                data = request.get_json()
    
                FileName = data.get('database')#carrega variável do json requisição do cliente.
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify({'Values': ["Access Violation."]}), 403
                
                #deleta o arquivo.
                
                return Connector.ReadWrite.rm_file(self.storage+"/"+FileName, self.storage) #retorna a lista de arquivos.
                
            else:
                return jsonify({'Values': ["Wrong method"]}), 401