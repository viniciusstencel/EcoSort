# 📨 Funcionalidade do Apache Kafka no Projeto EcoSort

O **Apache Kafka** atua como o **Registro Central de Eventos** do nosso sistema, sendo o intermediário obrigatório para garantir que todos os resultados de classificação da Inteligência Artificial sejam entregues ao nosso banco de dados de forma confiável.

Ele garante a **integridade dos dados** em nossa arquitetura orientada a eventos.

---

## 💡 Papel e Atuação no Fluxo do Resíduo

O Kafka entra em ação imediatamente após o Serviço IA (Python) classificar o material:

### 1. Garantir a Captura da Classificação (Produtor)

* **Quem Faz:** O **Serviço IA (Python)**.
* **Ação:** Assim que a IA determina o tipo de resíduo (ex: "Plástico - 95%"), ela publica essa informação no **Tópico Kafka: `classification-result`**.
* **Benefício:** O Python pode retornar a atenção ao stream de vídeo imediatamente, sem ter que esperar que o Java receba e salve os dados. O evento está seguro no Kafka.

### 2. Preservar o Histórico (Armazenamento Durável)

* **Ação:** O Kafka armazena o evento de classificação de forma durável.
* **Benefício:** Se o nosso **Serviço de Persistência (Java)** estiver passando por uma manutenção, estiver reiniciando ou ficar sobrecarregado, **nenhum dado de separação é perdido**. O Kafka guarda o evento, e o Java o consumirá assim que estiver pronto.

### 3. Assegurar o Salvamento no Banco (Consumidor)

* **Quem Faz:** O **Serviço de Persistência (Java)**.
* **Ação:** O Java atua como **Consumidor Kafka**, lendo o tópico `classification-result`. Ele retira o evento e é o único responsável por salvá-lo de forma segura no banco de dados PostgreSQL.
* **Benefício:** O Serviço Java tem controle total sobre a integridade dos dados, e garante que o registro histórico de todas as separações esteja sempre atualizado e disponível para o Dashboard.

---

## 🎯 Resumo da Contribuição do Kafka

| Funcionalidade | Resultado no Projeto |
| :--- | :--- |
| **Desacoplamento** | O Serviço IA e o Backend Java trabalham de forma totalmente independente, aumentando a robustez. |
| **Tolerância a Falhas** | Nenhuma classificação de resíduo é perdida se o banco de dados ou o servidor Java falhar temporariamente. |
| **Escalabilidade** | Permite que o Serviço IA publique milhares de eventos por segundo sem sobrecarregar o Backend Java, pois o Kafka absorve o volume. |