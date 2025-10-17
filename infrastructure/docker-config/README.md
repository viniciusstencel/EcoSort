# 🐳 Configuração e Orquestração Docker Compose

Esta pasta contém os arquivos necessários para construir e orquestrar todos os serviços do Projeto EcoSort, garantindo que a comunicação interna e a persistência de dados funcionem corretamente.

### 📝 Arquivos Chave

| Arquivo | Descrição |
| :--- | :--- |
| **`docker-compose.yml`** | Define todos os serviços, redes internas e volumes persistentes. Orquestra a construção e a inicialização de todos os contêineres. |
| **`.env`** | Armazena **variáveis de ambiente sensíveis** (senhas do PostgreSQL, portas de acesso, etc.). **ATENÇÃO: Não comite este arquivo publicamente!** |
| **`mosquitto/`** | Configurações opcionais para o broker MQTT (se estiver rodando um broker dedicado no Docker). |

### 🔗 Comunicação de Rede

O `docker-compose` estabelece uma rede interna (`ecosort_net`). Os serviços se comunicam usando o nome do serviço definido no YAML (ex: `postgres-db`, `ia-python`).

* O **Backend Java** se comunica com a **IA Python** via HTTP interno.
* O **Backend Java** se comunica com o **PostgreSQL** via conexão de banco de dados.

### 💾 Persistência de Dados

Utilizamos **Volumes Persistentes** para o contêiner do PostgreSQL, garantindo que todos os logs e relatórios de coleta sejam mantidos após reinicializações do Docker.