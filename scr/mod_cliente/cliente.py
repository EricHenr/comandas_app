from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import requests
from funcoes import Funcoes
from settings import getHeadersAPI, ENDPOINT_CLIENTE
from mod_login.login import validaToken

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')

@bp_cliente.route('/', methods=['GET', 'POST'])
@validaToken
def formListaCliente():
    try:
        response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
        result = response.json()
        print(result)  # for testing
        print(response.status_code)  # for testing
        if response.status_code != 200:
            raise Exception(result)
        return render_template('formListaCliente.html', result=result[0])
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/form-cliente', methods=['GET'])
@validaToken
def formCliente():
    return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        # data sent via FORM
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        
        # create the JSON payload to send to the API
        payload = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone
        }
        
        # execute the POST request to the API and store its response
        response = requests.post(ENDPOINT_CLIENTE, headers=getHeadersAPI(), json=payload)
        result = response.json()
        print(result)  # for testing
        print(response.status_code)  # for testing

        if response.status_code != 200:
            raise Exception(result)
        
        return redirect(url_for('cliente.formListaCliente', msg='Cliente criado com sucesso'))
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=str(e))

@bp_cliente.route("/form-edit-cliente", methods=['POST'])
@validaToken
def formEditCliente():
    try:
        # ID enviado via FORM
        id_cliente = request.form['id']
        
        # execute the GET request to the API to retrieve the selected cliente,
        # obtaining the JSON response
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()
        
        if response.status_code != 200:
            raise Exception(result)
        
        # render the form passing the returned data
        return render_template('formCliente.html', result=result[0])
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        # data sent via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        
        # create the JSON payload to send to the API
        payload = {
            'id_cliente': id_cliente,
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone
        }
        
        # execute the PUT request to the API and store its response
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if response.status_code != 200 or result.get('status_code', 200) != 200:
            raise Exception(result)
        
        return redirect(url_for('cliente.formListaCliente', msg=('msg', 'Update successful')))
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=str(e))

@bp_cliente.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        id_cliente = request.form['id']

        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()

        if response.status_code != 200 or result[1] != 200:
            raise Exception(result)

        return redirect(url_for('cliente.formListaCliente', msg='Cliente deletado com sucesso'))

    except Exception as e:
        return jsonify(erro=True, msgErro=str(e))
