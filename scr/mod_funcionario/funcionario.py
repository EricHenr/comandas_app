from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from mod_login.login import validaToken
import requests
from funcoes import Funcoes
from settings import getHeadersAPI, ENDPOINT_FUNCIONARIO

bp_funcionario = Blueprint('funcionario', __name__, url_prefix="/funcionario", template_folder='templates')

@bp_funcionario.route('/', methods=['GET', 'POST'])
@validaToken
def formListaFuncionario():
    try:
        response = requests.get(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI())
        result = response.json()
        print(result)  # for testing
        print(response.status_code)  # for testing
        if response.status_code != 200:
            raise Exception(result)
        return render_template('formListaFuncionario.html', result=result[0])
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])


@bp_funcionario.route('/form-funcionario', methods=['GET', 'POST'])
@validaToken
def formFuncionario():
    return render_template('formFuncionario.html')


@bp_funcionario.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        # data sent via FORM
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.get_password_hash(request.form['senha'])

        # create the JSON payload to send to the API
        payload = {
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'grupo': grupo,
            'senha': senha
        }

        # execute the POST request to the API and store its response
        response = requests.post(ENDPOINT_FUNCIONARIO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)  # for testing
        print(response.status_code)  # for testing

        if response.status_code != 200:
            raise Exception(result)
        
        return redirect(url_for('funcionario.formListaFuncionario', msg='Usuario criado com sucesso'))
    
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=str(e))

@bp_funcionario.route("/form-edit-funcionario", methods=['POST'])
@validaToken
def formEditFuncionario():
    try:
        # ID enviado via FORM
        id_funcionario = request.form['id']
        
        # executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(result)
        
        # renderiza o form passando os dados retornados
        return render_template('formFuncionario.html', result=result[0])
    
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        # dados enviados via FORM
        id_funcionario = request.form['id']
        nome = request.form['nome']
        matricula = request.form['matricula']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        grupo = request.form['grupo']
        senha = Funcoes.cifraSenha(request.form['senha'])
        
        # monta o JSON para envio a API
        payload = {
            'id_funcionario': id_funcionario,
            'nome': nome,
            'matricula': matricula,
            'cpf': cpf,
            'telefone': telefone,
            'grupo': grupo,
            'senha': senha
        }
        
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return redirect(url_for('funcionario.formListaFuncionario', msg=result[0]))
    
    except Exception as e:
        return render_template('formListaFuncionario.html', msgErro=e.args[0])

@bp_funcionario.route('/delete', methods=['POST'])
@validaToken
def delete():
  try:
    id_funcionario = request.form['id']

    response = requests.delete(ENDPOINT_FUNCIONARIO + id_funcionario, headers=getHeadersAPI())
    result = response.json()

    if response.status_code != 200 or result[1] != 200:
      raise Exception(result)

    return redirect(url_for('funcionario.formListaFuncionario', msg='Usuario deletado com sucesso'))

  except Exception as e:
    return jsonify(erro=True, msgErro=str(e))
