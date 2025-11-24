📘 EcoSort – Monitor de Reciclagem Inteligente

Interface web desenvolvida em Next.js + React, utilizando TailwindCSS v3 e Chart.js, voltada para visualização e análise de dados sobre resíduos reciclados.

🚀 Tecnologias Utilizadas

Next.js 14+

React 18+

TailwindCSS 3

Chart.js + react-chartjs-2

chartjs-plugin-datalabels

TypeScript

📦 Instalação do Projeto
1️⃣ Clone o repositório (ou abra sua pasta existente)
git clone <url-do-seu-repo>
cd meu-site

📥 Instalar Dependências
🔧 Dependências do Next.js / React
npm install

🎨 Instalar TailwindCSS (versão 3)

Instalação recomendada:

npm install -D tailwindcss@3 postcss autoprefixer


Gerar arquivos de config:

npx tailwindcss init -p

Certifique-se de que tailwind.config.js contém:
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: { extend: {} },
  plugins: [],
};


E que globals.css possui:

@tailwind base;
@tailwind components;
@tailwind utilities;

📊 Instalar bibliotecas de gráficos
npm install chart.js react-chartjs-2 chartjs-plugin-datalabels

▶️ Rodando o projeto
npm run dev


O projeto iniciará em:

http://localhost:3000

📁 Estrutura Simplificada
meu-site/
 ├─ app/
 │   ├─ page.tsx           → Página principal
 │   ├─ graph.tsx          → Componente do gráfico
 │   └─ globals.css        → Estilos globais
 ├─ public/                → Imagens, ícones, etc.
 ├─ package.json
 ├─ tailwind.config.js
 └─ README.md

📌 Funcionalidades

Dashboard com métricas gerais

Gráfico de distribuição de resíduos com:

Cores personalizadas

Labels externos

Percentuais calculados via peso e quantidade

Cards das categorias de resíduos

Card de Atividade Recente com eventos automáticos

Layout responsivo

🛠️ Comandos úteis
Ação	Comando
Instalar dependências	npm install
Iniciar servidor	npm run dev
Build para produção	npm run build
Rodar build otimizado	npm start