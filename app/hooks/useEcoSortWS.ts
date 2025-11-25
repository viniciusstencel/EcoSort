"use client";

import { useEffect, useState, useRef } from "react";
import SockJS from "sockjs-client";
import { Client } from "@stomp/stompjs";

export interface Residuo {
  classification: string;
  reliability?: number;
  confidence?: number;
  date?: string;
  timestamp?: string;
}

export default function useEcoSortWS() {
  const [historico, setHistorico] = useState<Residuo[]>([]);
  const [novos, setNovos] = useState<Residuo[]>([]);
  const clientRef = useRef<Client | null>(null);

  useEffect(() => {
    const WS_URL = "http://localhost:8080/ws-connect";

    const TOPIC_UPDATES = "/topic/residues";
    const TOPIC_HISTORY_RECEIVE = "/user/queue/history";
    const APP_REQUEST_HISTORY = "/app/request-history";

    const socket = new SockJS(WS_URL);

    const client = new Client({
      webSocketFactory: () => socket,
      debug: () => {}, // Desativar logs
      reconnectDelay: 5000, // Reconn automática
    });

    client.onConnect = () => {
      console.log("Conectado ao WebSocket!");

      // Receber histórico
      client.subscribe(TOPIC_HISTORY_RECEIVE, (msg) => {
        const lista = JSON.parse(msg.body);
        setHistorico(lista);
      });

      // Receber atualizações em tempo real
      client.subscribe(TOPIC_UPDATES, (msg) => {
        const novo = JSON.parse(msg.body);
        setNovos((prev) => [novo, ...prev]);
      });

      // Enviar requisição pelo histórico
      client.publish({
        destination: APP_REQUEST_HISTORY,
        body: "",
      });
    };

    client.onStompError = (err) => {
      console.error("Erro no STOMP:", err);
    };

    client.activate();

    clientRef.current = client;

    return () => {
      client.deactivate();
    };
  }, []);

  return { historico, novos };
}
