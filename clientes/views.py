from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
# Create your views here.


def clientes(request):
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        # verificar se o cpf do cliente já nao está cadastrado

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            # retorna no formulários com os dados preenchidos
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos)})
            # return HttpResponse("Cliente já existe")

        # validação de email - verificar se email é valido -
        # re (expressões regulares)
        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)})
            # return HttpResponse('Email inválido')

            # print(carro)
            # print(placa)
            # print(ano)
            # Importando a classe Cliente do models (banco de dados) -
            # referencia colunas do banco de dados para as variáveis de cliente
        cliente = Cliente(
            nome=nome,
            sobrenome=sobrenome,
            email=email,
            cpf=cpf
        )

        cliente.save()

        # zip uma tupla dentro de uma lista, ele correlaciona
        # as ordens das listas
        # x = list(zip(carro, placa, ano))
        # print(x)

        for carro, placa, ano in zip(carros, placas, anos):
            carro = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)

            carro.save()

        return HttpResponse("Teste")

def att_cliente(request):
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    print("Cliende :" + cliente)
    cliente_json = json.loads(serializers.serialize('json', 'cliente'))[0]['fields']
    print("Cliente Serialize: " + cliente_json)
    return JsonResponse(cliente_json)
