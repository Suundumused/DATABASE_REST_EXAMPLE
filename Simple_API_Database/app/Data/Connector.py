import os
import sys
import io
import contextlib
import csv
import random

import pandas as pd

from flask import jsonify

class ReadWrite: 
    def read_file(filename, range, column):        
        try:
            data = []
            data2 = []

            df = pd.read_csv(filename)
            
            if column == "": #se coluna não especificada, resulta em todas as colunas.
                data =  [df.columns.tolist()] + df.values.tolist()
                
            else:
                data =  [column] + df[column].values.tolist() #filtra a list com a coluna especificada
                
            if range[0] == 0 and range[1] == 0: #se Range = [0,0] obtém todos as linhas.
                return jsonify({'Values': data}), 200
            
            elif range[0] != 0 and range[1] == 0:   #se range[algumvalor, 0] retorna linhas a partir do especificado até o final.
                try:
                    data2 = data[range[0]:]
                    
                    return jsonify({'Values': data2}), 200

                except:
                    return jsonify({'Values': ["Out of bounds."]}), 409
                
            else:
                try:
                    data2 = data[range[0]:range[1]+1]
                    
                    return jsonify({'Values': data2}), 200

                except:
                    return jsonify({'Values': ["Out of bounds."]}), 409
            
        except Exception as e:
            error_message = repr(e) #retorna erro Exception.
            
            return jsonify({'Values': ["{}".format(error_message)]}), 404
        
    def make_file(filename, content):
        try:
            df = pd.DataFrame(content) #cria o arquivo e escreve o conteúdo recebido.
            
            df.to_csv(filename, index=False)
                                            
            return ReadWrite.read_file(filename, [0,0], "") #retorna o conteúdo do arquivo quando bem sucedido.
            
        except Exception as e:
            error_message = repr(e)
            
            return jsonify({'Values': ["{}".format(error_message)]}), 500
        
    def edit_db(filename, column_number, line_number, new_content, rmvalue):
        try:        
            df = pd.read_csv(filename)
                    
            if rmvalue:
                if line_number == 0: #se linha passada pelo usuário for 0, irá deletar a coluna e todos os filhos.
                    try:
                        df = df.drop(column_number, axis=1)
                        
                        df.to_csv(filename, index=False)
                        
                        return ReadWrite.read_file(filename, [0,0], "")
                    
                    except:
                        return jsonify({'Values': ["Out of bounds."]}), 409
                           
                    #new_content = ""
                    
                else:
                    try:
                        df.at[line_number, column_number] = None #remove conteúdo especificado.
                        
                        df.to_csv(filename, index=False)
                        
                        return ReadWrite.read_file(filename, [0,0], "")
                    
                    except:
                        return jsonify({'Values': ["Out of bounds."]}), 409
                    #new_content = ""
                
            else: #cria ou edita valor novo
                try:
                    if column_number not in df.columns:
                        df[column_number] = None

                    # Adicionando/trocando o valor na linha e coluna específicas
                    if line_number >= len(df):
                        df.loc[line_number] = None  # Criando uma nova linha, se necessário
                    df.at[line_number, column_number] = new_content
                    
                    df.to_csv(filename, index=False) #SALVANDO ARQUIVO
                    
                    return ReadWrite.read_file(filename, [0,0], "")        
                
                except:
                    return jsonify({'Values': ["Out of bounds."]}), 409 
    
        except Exception as e:
            error_message = repr(e)
            
            return jsonify({'Values': ["{}".format(error_message)]}), 404
        
    def rm_file(filename, storage):        
        try:
            os.remove(filename)
                                        
            return jsonify({'Values': os.listdir(storage)}), 410
            
        except Exception as e:
            error_message = repr(e) #retorna erro Exception.
            
            return jsonify({'Values': ["{}".format(error_message)]}), 404        
