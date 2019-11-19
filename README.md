
# Abandono de carrinho - Apache Beam - Python

## Sumário

O projeto em questão implementa uma solução para encontrar carrinhos abandonados pelos clientes de um e-commerce lendo os dados originais da pasta input e persistindo o resultado da transformação na pasta output.

## Pré-Requisitos

O código foi escrito em Python 3.5 . Caso você não tenha o python instalado, ele pode ser encontrado [aqui]. Caso você esteja usando uma versão de python inferior a 3.5, é possível fazer o upgrade usando o pip.

Para instalar o pip através da linha de comando use:
```sh
$ python -m ensurepip -- default-pip
```
Upgrade do pip:
```sh
$ python -m pip install -- upgrade pip setuptools wheel
```
Upgrade do Python:
```ssh
$ pip install python -- upgrade
```
Para instalar o Apache-Beam use:
```ssh
$ pip install apache-beam
```
 #### Recomendação 
 É recomendado que o processo seja executado no ambiente virtual.
 Para efetuar a instalação use:
 ```ssh
$ pip install --upgrade virtualenv
```

## Dados

Os dados possuem a seguinte estrutura:
```ssh
 { "timestamp": "2019-01-01 12:00:00", "customer": "customer-1", "page": "product", "product": "product-1" }
 { "timestamp": "2019-01-01 12:02:00", "customer": "customer-1", "page": "basket", "product": "product-1" }
 { "timestamp": "2019-01-01 12:04:00", "customer": "customer-1", "page": "checkout" }
```
## Execução
Para executar o script use o seguinte comando:
```ssh
$ python abandono.py
```

[//]: #

   [aqui]: <https://www.python.org/downloads/>

