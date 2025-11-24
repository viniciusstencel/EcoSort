"use client";

import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartOptions,
} from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";

ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

interface DistribuicaoTipoProps {
  categorias: {
    nome: string;
    cor: string;
    percentual: number;
  }[];
}

export default function DistribuicaoTipo({ categorias }: DistribuicaoTipoProps) {
  const pieData = {
    labels: categorias.map((cat) => cat.nome),
    datasets: [
      {
        data: categorias.map((cat) => cat.percentual),
        backgroundColor: categorias.map((cat) => cat.cor),
        borderWidth: 1,
      },
    ],
  };

  const pieOptions: ChartOptions<"pie"> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
      datalabels: {
        color: (ctx: any) => ctx.dataset.backgroundColor[ctx.dataIndex],
        font: { weight: "bold", size: 12 },
        formatter: (value: number, ctx: any) => {
          const label = ctx.chart.data.labels[ctx.dataIndex];
          return `${label}: ${value}%`;
        },
        anchor: "end",
        align: "end",
        offset: 10,
      },
    },
    layout: { padding: 20 },
    radius: "65%",
  };

  return (
    <div className="flex items-center justify-center w-full h-96">
      <Pie data={pieData} options={pieOptions} />
    </div>
  );
}
