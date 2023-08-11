import os
import sys
import io
import contextlib

from flask import jsonify

class ReadWrite:    
    def read_file(filename):        
        try:
            with contextlib.ExitStack() as stack:
                file = stack.enter_context(io.open(filename, mode='r', encoding='utf-8', errors='ignore'))
                data = file.read() #abre o arquivo.
                                        
            return jsonify(content = '{}'.format(data)), 200
            
        except Exception as e:
            error_message = repr(e) #retorna erro Exception.
                        
            return jsonify(Error = '{}'.format(error_message)), 404
        
    def make_file(filename, content):
        try:
            with contextlib.ExitStack() as stack:
                file = stack.enter_context(open(filename, mode='w', encoding='utf-8', errors='ignore'))
                file.write(content)  #cria o arquivo e escreve o conteúdo recebido.
                                
            return ReadWrite.read_file(filename) #retorna o conteúdo do arquivo quando bem sucedido.
            
        except Exception as e:
            error_message = repr(e)
                        
            return jsonify(Error = '{}'.format(error_message)), 500
        
    def edit_db(filename, line_number, new_content):
        try:
            with open(filename, mode='r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()

            if line_number < len(lines) and line_number >= 0: #se id < 0 retorna erro e se > que a quantidade de linhas, cria uma nova linha.
                lines[line_number] = new_content + '\n'

                with open(filename, mode='w', encoding='utf-8', errors='ignore') as file:
                    file.writelines(lines) #escreve nova linha
                
                return jsonify(content = '{}'.format(new_content)), 200 #retorna nova linha quando bem sucedido.
            
            else:
                if line_number < 0: #se id < 0 retorna erro.
                    return jsonify(Error = 'Out of bounds.'), 409
                
                else: #se não, cria uma nova linha.
                    with open(filename, mode='a', encoding='utf-8', errors='ignore') as file: 
                        file.write(new_content + '\n')
                    
                    return jsonify(content = '{}'.format(new_content)), 200
    
            
        except Exception as e:
            error_message = repr(e)

            return jsonify(Error = '{}'.format(error_message)), 404
        
    def rm_file(filename, storage):        
        try:
            os.remove(filename)
                                        
            return jsonify(Databases = os.listdir(storage)), 410
            
        except Exception as e:
            error_message = repr(e) #retorna erro Exception.
                        
            return jsonify(Error = '{}'.format(error_message)), 404
        