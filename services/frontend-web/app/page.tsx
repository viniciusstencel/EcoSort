"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import DistribuicaoTipo from "./graph";
import useEcoSortWS from "@/app/hooks/useEcoSortWS";

// Material Icons
import ScienceIcon from "@mui/icons-material/Science";
import DescriptionIcon from "@mui/icons-material/Description";
import ConstructionIcon from "@mui/icons-material/Construction";
import LocalBarIcon from "@mui/icons-material/LocalBar";
import GrassIcon from "@mui/icons-material/Grass";
import EnergySavingsLeafIcon from "@mui/icons-material/EnergySavingsLeaf";
import PieChartIcon from "@mui/icons-material/PieChart";
import HistoryIcon from "@mui/icons-material/History";

// 🔥 TRADUÇÃO: BACK-END (EN) → FRONT-END (PT)
const traduzir = {
  plastic: "Plástico",
  paper: "Papel",
  metal: "Metal",
  glass: "Vidro",
  organic: "Orgânico",
};

export default function Home() {
  const { historico, novos } = useEcoSortWS();

  // Combinação dos dados recebidos
  const eventos = [...novos, ...historico];

  // Categorias base (PT)
  const categoriasBase = [
    { nome: "Plástico", cor: "#3b82f6", icone: <ScienceIcon className="text-blue-500" /> },
    { nome: "Papel", cor: "#facc15", icone: <DescriptionIcon className="text-yellow-500" /> },
    { nome: "Metal", cor: "#9ca3af", icone: <ConstructionIcon className="text-gray-500" /> },
    { nome: "Vidro", cor: "#22c55e", icone: <LocalBarIcon className="text-green-500" /> },
    { nome: "Orgânico", cor: "#ef4444", icone: <GrassIcon className="text-red-500" /> },
  ];

  // Contagem por categoria (comparando textos em inglês vindos do backend)
  const contagem = categoriasBase.map((cat) => ({
    ...cat,
   items: eventos.filter(
  (e) =>
    traduzir[e.classification?.toLowerCase() as keyof typeof traduzir] ===
    cat.nome
).length,
  }));

  // Peso mockado / até receber dado real
  const totalItems = contagem.reduce((a, b) => a + b.items, 0) || 1;

  const impactosPercent = contagem.map((cat) =>
    Math.round((cat.items / totalItems) * 100)
  );

  return (
    <main className="flex flex-col min-h-screen bg-white text-black p-8 space-y-8">

      {/* Header */}
      <div className="flex items-center space-x-4">
        <div className="w-20 h-20 bg-green-200 flex items-center justify-center rounded-full overflow-hidden">
          <Image
            src="/ecosort.png"
            alt="Logo EcoSort"
            width={80}
            height={80}
            className="object-contain"
          />
        </div>

        <div>
          <h1 className="text-3xl font-bold text-green-600">EcoSort</h1>
          <p className="mt-1 text-sm text-gray-700">Monitor de Reciclagem Inteligente</p>
        </div>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        
        <div className="bg-green-100 p-4 rounded-lg shadow flex flex-col">
          <h2 className="text-lg font-semibold text-black">Total de Items</h2>
          <span className="text-2xl font-bold text-black">{totalItems}</span>
        </div>

        <div className="bg-green-100 p-4 rounded-lg shadow flex flex-col">
          <h2 className="text-lg font-semibold text-black">Peso Total</h2>
          <span className="text-2xl font-bold text-black">{(totalItems * 0.08).toFixed(2)} kg</span>
        </div>

        <div className="bg-green-100 p-4 rounded-lg shadow flex flex-col">
          <h2 className="text-lg font-semibold text-black">Taxa de Reciclagem</h2>
          <span className="text-2xl font-bold text-black">78%</span>
        </div>

        <div className="bg-green-100 p-4 rounded-lg shadow flex flex-col">
          <h2 className="text-lg font-semibold text-black">Categorias Ativas</h2>
          <span className="text-2xl font-bold text-black">5</span>
        </div>

      </div>

      {/* Categorias */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold text-black mb-4">Categorias de Resíduos</h2>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">

          {contagem.map((cat, idx) => (
            <div key={cat.nome} className="bg-gray-100 p-4 rounded-lg shadow flex flex-col h-32">
              
              <div className="flex items-center space-x-3">
                {cat.icone}
                <span className="text-lg font-semibold text-black">{cat.nome}</span>
                <span className="text-sm text-gray-700 ml-auto">{cat.items} itens</span>
              </div>

              <div className="w-full bg-gray-300 h-3 rounded-full mt-3">
                <div
                  className="bg-green-500 h-3 rounded-full"
                  style={{ width: `${impactosPercent[idx]}%` }}
                ></div>
              </div>

              <div className="text-xs text-gray-500 mt-1">{impactosPercent[idx]}% impacto</div>

            </div>
          ))}

        </div>
      </div>

      {/* Distribuição + Atividade */}
      <div className="flex flex-col md:flex-row md:space-x-8">

        <div className="md:w-1/2 bg-gray-100 p-6 rounded-lg shadow">
          <div className="flex items-center gap-2 mb-4">
            <PieChartIcon className="text-green-600" />
            <h2 className="text-lg font-semibold">Distribuição por tipo</h2>
          </div>

          <DistribuicaoTipo
            categorias={contagem.map((cat, idx) => ({
              nome: cat.nome,
              cor: cat.cor,
              percentual: impactosPercent[idx],
            }))}
          />
        </div>

        <div className="md:w-1/2 bg-gray-100 p-6 rounded-lg shadow mt-8 md:mt-0">
          <div className="flex items-center gap-2">
            <HistoryIcon className="text-green-600" />
            <h2 className="text-lg font-semibold">Atividade recente</h2>
          </div>

          <div className="flex flex-col space-y-4 mt-4">
            {eventos.slice(0, 5).map((e, idx) => (
              <div key={idx} className="flex items-center justify-between bg-white p-3 rounded-lg shadow">
                <span className="font-semibold capitalize">
                  {traduzir[e.classification?.toLowerCase() as keyof typeof traduzir] ?? e.classification}
                </span>
                <span className="text-sm text-gray-600">{e.timestamp}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </main>
  );
}
