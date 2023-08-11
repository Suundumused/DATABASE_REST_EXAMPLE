from flask import *

import sys
import os

sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Data"))
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
        
        self.storage = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../storage") #define a pasta local onde os arquivos serão manipulados.
        
        @app.errorhandler(415)
        def unsupported_media_type(error):
            return jsonify({"error": "Unsupported Media Type."}), 415
        
        @app.errorhandler(500)
        def bad_request(error):
            return jsonify({"error": "Critical Unknown Error."}), 500
        
        @app.route('/ls', methods=['GET']) #lista de arquivos.
        def ls():
            if request.method == 'GET':
                try:
                    return jsonify(Databases = os.listdir(self.storage)), 200 #lista de arquivos.
                
                except Exception as e:
                    return jsonify(Error = '{}'.format(e)), 500 #retorna o erro
                
            else:
                return jsonify(message = 'Wrong method'), 401 #método incorreto retorna erro como json.
                
        @app.route('/touch', methods=['POST']) #cria/sobrescreve arquivo com conteúdo.
        def touch():
            if request.method == 'POST':
                data = request.get_json()
            
                FileName = data.get('database' )#carrega variável do json requisição do cliente.
                Content = data.get('content')
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify(message = 'Access Violation.'), 403
                
                 #cria/sobrescreve arquivo com conteúdo.
                
                return Connector.ReadWrite.make_file(self.storage+"/"+FileName, Content) #retorna o novo conteúdo do arquivo.
                
            else:
                return jsonify(message = 'Wrong method'), 401
            
        @app.route('/nano', methods=['PUT']) #editar linha arquivo específico
        def nano():
            if request.method == 'PUT':
                data = request.get_json()
            
                FileName = data.get('database') #carrega variável do json requisição.
                Index = data.get('index')
                Content = data.get('content')
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify(message = 'Access Violation.'), 403
                
                return Connector.ReadWrite.edit_db(self.storage+"/"+FileName, Index, Content)
                
            else:
                return jsonify(message = 'Wrong method'), 401
        
        @app.route('/cat', methods=['GET']) #ler arquivo específico
        def cat():
            if request.method == 'GET':
                data = request.get_json()
                
                FileName = data.get('database') #carrega variável do json requisição.
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify(message = 'Access Violation.'), 403
            
                return Connector.ReadWrite.read_file(self.storage+"/"+FileName) #retorna o novo conteúdo do arquivo.
            
            else:
                return jsonify(message = 'Wrong method'), 401
            
        @app.route('/rm', methods=['DELETE']) #remove arquivo.
        def rm():
            if request.method == 'DELETE':
                data = request.get_json()
    
                FileName = data.get('database')#carrega variável do json requisição do cliente.
                
                if Protection.antiescape(FileName) == True: #proteje o servidor, exemplo de nome do arquivo: "../../../../../Windows/System32/appraiser.dll"
                    return jsonify(message = 'Access Violation.'), 403
                
                #deleta o arquivo.
                
                return Connector.ReadWrite.rm_file(self.storage+"/"+FileName, self.storage) #retorna a lista de arquivos.
                
            else:
                return jsonify(message = 'Wrong method'), 401