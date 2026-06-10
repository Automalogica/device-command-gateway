```
$$$$$$\                                                                  
$$  __$$\                                                                 
$$ /  \__| $$$$$$\  $$$$$$\$$$$\   $$$$$$\   $$$$$$\   $$$$$$\           
$$ |       \____$$\ $$  _$$  _$$\ $$  __$$\ $$  __$$\ $$  __$$\          
$$ |       $$$$$$$ |$$ / $$ / $$ |$$$$$$$$ |$$ |  \__|$$$$$$$$ |         
$$ |  $$\ $$  __$$ |$$ | $$ | $$ |$$   ____|$$ |      $$   ____|         
\$$$$$$  |\$$$$$$$ |$$ | $$ | $$ |\$$$$$$$\ $$ |      \$$$$$$$\          
 \______/  \_______|\__| \__| \__| \_______|\__|       \_______|         

          $$$$$$\                                    $$\                  
         $$  __$$\                                   $$ |                 
         $$ /  $$ | $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$\                 
         $$$$$$$$ |$$  __$$\ $$  __$$\ $$  __$$\ \_$$  _|                
         $$  __$$ |$$ /  $$ |$$$$$$$$ |$$ |  $$ |  $$ |                  
         $$ |  $$ |$$ |  $$ |$$   ____|$$ |  $$ |  $$ |$$\               
         $$ |  $$ |\$$$$$$$ |\$$$$$$$\ $$ |  $$ |  \$$$$  |              
         \__|  \__| \____$$ | \_______|\__|  \__|   \____/                
                   $$\   $$ |                                             
                   \$$$$$$  |                                             
                    \______/                                              
```

<p align="center">
    <em>Agente Docker para execução de comandos de câmeras via MQTT e Telnet, com persistência em PostgreSQL</em>
</p>

<p align="center">
<a href="" target="_blank">
    <img src="https://img.shields.io/badge/21-2596be?style=flat&logo=openjdk&logoColor=white&label=Java&labelColor=gray"
    alt="Java 21">
</a>
<a href="" target="_blank">
    <img src="https://img.shields.io/badge/5.7-6db33f?style=flat&logo=eclipsemosquitto&logoColor=white&label=EMQX&labelColor=gray"
    alt="EMQX 5.7">
</a>
<a href="" target="_blank">
    <img src="https://img.shields.io/badge/16-336791?style=flat&logo=postgresql&logoColor=white&label=PostgreSQL&labelColor=gray"
    alt="PostgreSQL 16">
</a>
<a href="" target="_blank">
    <img src="https://img.shields.io/badge/0.00%25-red?style=flat&logo=checkmarx&logoColor=white&label=Coverage&labelColor=gray"
    alt="Coverage">
</a>
</p>

---

# Visão Geral

O **Camera Agent** é um serviço Docker que consome comandos XML publicados pelo Elipse E3 via MQTT,
persiste cada comando no PostgreSQL e os executa assincronamente nas câmeras IP via protocolo Telnet (CMS 2.2).
O resultado é publicado de volta ao SCADA via `camera/feedback`.

```
Elipse E3 → [camera/command] → EMQX → Camera Agent → Telnet → Câmeras IP
Elipse E3 ← [camera/feedback] ← EMQX ← Camera Agent ← PostgreSQL
```

---

# Develop Checklist

1 - Pegue uma issue em [Issues](https://github.com/Automalogica/camera-agent/issues)

2 - Crie uma branch chamada **issue_XXX** a partir de [main](https://github.com/Automalogica/camera-agent/tree/main)

3 - [Configure o ambiente e instale as dependências](#configurar-ambiente)

4 - Faça suas modificações

5 - [Rode os testes](#testes)

6 - Garanta 100% no [Coverage Report](#coverage-report)

7 - Crie um PR da sua **issue_XXX** para **main**

8 - Solicite revisão ao tech leader

9 - Se negado, volte ao passo 4

10 - Se aceito, faça o merge da **issue_XXX** e delete a branch

11 - O deploy automático será disparado

---

# Configurar Ambiente

### Pré-requisitos

- Docker >= 24
- Docker Compose >= 2.24
- Python 3.13

### Variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env preenchendo as senhas antes de subir os containers
```

### Subir infraestrutura

```bash
docker compose up -d
```

Os containers sobem na seguinte ordem (via `healthcheck`):

1. `camera_postgres` — PostgreSQL 16 + criação automática do schema via `init.sql`
2. `camera_emqx` — EMQX 5.7 com ACL restrita aos tópicos `camera/command` e `camera/feedback`
3. `camera_agent` — Camera Agent (aguarda EMQX e Postgres estarem saudáveis)

---

# Tópicos MQTT

| Tópico | Direção | Descrição |
|---|---|---|
| `camera/command` | Elipse E3 → Camera Agent | Comando XML com `request_id`, `command` e `params` |
| `camera/feedback` | Camera Agent → Elipse E3 | Retorno XML com `request_id` e `status` (DONE / ERROR) |

### Exemplo de payload

```xml
<!-- Envio -->
<camera_command>
  <request_id>lucas_20260610143022847</request_id>
  <command>share</command>
  <params>P1 D1 2</params>
</camera_command>

<!-- Retorno -->
<camera_feedback>
  <request_id>lucas_20260610143022847</request_id>
  <status>DONE</status>
</camera_feedback>
```

O `request_id` segue o formato `{user_name}_{yyyyMMddHHmmssSSS}`, garantindo unicidade mesmo sob alta frequência.

---

# Testes

```bash
docker compose up -d

./mvnw test

docker compose down
```

### Todos os testes devem passar

---

# Coverage Report

```bash
n/a
```

### Deve ser 100%

---

# Estrutura do Projeto

```
camera-agent/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── config/
│   ├── emqx/
│   │   └── acl.conf          # ACL EMQX — restringe aos 2 tópicos
│   └── postgres/
│       └── init.sql          # Schema + índices criados automaticamente
└── src/
    └── main/
        └── ...               # Código-fonte do Camera Agent
```

---

# Variáveis de Configuração

| Variável | Padrão | Descrição |
|---|---|---|
| `WORKER_POOL_SIZE` | `10` | Número de workers paralelos |
| `TELNET_TIMEOUT_MS` | `5000` | Timeout por comando Telnet (ms) |
| `MQTT_TOPIC_COMMAND` | `camera/command` | Tópico de entrada |
| `MQTT_TOPIC_FEEDBACK` | `camera/feedback` | Tópico de retorno |
| `DB_HOST` | `postgres` | Host do PostgreSQL |
| `MQTT_HOST` | `emqx` | Host do EMQX |