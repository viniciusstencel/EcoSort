# 🖥️ Aplicação Web Interativa (React.js)

O frontend é a interface de engajamento do usuário. Ele mostra relatórios e, mais importante, oferece **feedback visual e gamificação em tempo real** quando um resíduo é depositado.

### ✨ Recursos Principais

1.  **Conexão WebSocket:** Mantém uma conexão persistente com a API Java para receber notificações de classificação **ao vivo** e atualizar o placar e os efeitos visuais.
2.  **Gamificação:** Exibe um placar 🏆 e aciona animações de celebração 🎉 (via bibliotecas como Lottie ou Rive) para incentivar a reciclagem correta.
3.  **Dashboard de Métricas:** Apresenta relatórios gráficos sobre o volume de coleta por tipo e período, obtidos da API Java.

### 🌐 Comunicação

* **API REST:** Consome dados de relatórios via a API Java.
* **WebSockets:** Conecta-se ao endpoint `/ws/feed` da API Java para o fluxo de dados em tempo real.

### 📦 Como Construir e Rodar (Localmente)

1.  Certifique-se de que o Node.js está instalado.
2.  Instale as dependências:
    ```bash
    npm install
    ```
3.  Inicie o servidor de desenvolvimento:
    ```bash
    npm start
    ```
    *O app geralmente abre em `http://localhost:3000`.*