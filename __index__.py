from flask import Flask, request, render_template, redirect, Response, send_file
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from math import pi, log
import re

app = Flask(__name__)

cors = CORS(app, resource = {r"/*":{"origins": "*"}})

upload_folder = './static/arquivos'
dowload_folder = './static/resultados'
allowed_extensions = {'txt'}
app.config['upload_folder'] = upload_folder
app.config['dowload_folder'] = dowload_folder


@app.route('/BEB/<nome>', methods=['GET', 'POST'])
def BEB(nome, energia_inicio=1, energia_fim=500):
    nomef=nome
    #Retira a extensão do nome do input
    nome = nome.replace(".txt", "")

    #Seta as variaveis de dentro da função
    ar = nome
    T = energia_inicio
    Tf = energia_fim

    #Variaveis do BEB e definição da lista vazia
    a = 0.5292
    R = 13.61
    soma = 0
    Tx = []
    Secao = []

    #Abre o arquivo que foi enviado e que esta salvo e executa o BEB em si
    with open("./static/arquivos/{}.txt".format(ar), "r") as data:
        dados = data.read().split('\n')
        d=[]

        for i in range(0, len(dados)):
            dados[i]=list(map(float, dados[i].split('\t')))
        
        while T<Tf:
            soma = 0

            for j in range(0, len(dados)):

                U=dados[j][0]
                B=dados[j][1]
                N=dados[j][2]
                
                t=T/B
                u=U/B
                S=4*pi*(a**2)*N*((R**2)/(B**2))
                sBEB = (S/(t+u+1))*( (log(t)/2)*(1-(1/(t**2))) + 1 - (1/t) - (log(t)/(t+1)) )
                if T>B:
                    soma = soma + sBEB
                
            Tx.append(T)
            Secao.append(soma)
            T = T + 1

        #Salva no arquivo resposta
        with open("./static/resultados/{}.txt".format(ar), "w") as n:
            
            for u in range(0, len(Tx)):
                n.write(str(Tx[u])+" "+str(Secao[u])+"\n")


    filename = nomef
    filename = filename.replace(".txt", "")

    path = "./static/resultados/{}.txt".format(filename)
    
    return send_file(path, as_attachment=True)

@app.route('/', methods=['GET', 'POST'])
def main():
    positivo = None
    filename = None
    try:
        
        if request.method == "POST":
            
            if request.files:
                
                A = request.files['arquivo']
                filename = secure_filename(A.filename)
                A.save(os.path.join(app.config['upload_folder'], filename))
                A.save(os.path.join(app.config['dowload_folder'], filename))

                positivo = 1
        
    except:
        positivo = 0
    

    return render_template("index.html", positivo = positivo, filename = filename)

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
