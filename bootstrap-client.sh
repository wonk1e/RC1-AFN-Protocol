#!/usr/bin/env bash

# Atualizar lista de pacotes
sudo apt-get update -y

# Instalar Python e pip
sudo apt-get install -y python3 python3-pip

# Instalar dependências adicionais se necessário
sudo apt-get install -y net-tools iputils-ping
