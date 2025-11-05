# comms_handler.py

import paho.mqtt.client as mqtt
import requests
import json
import time
import os
import datetime # <-- Import necessário

class CommsHandler:
    """ Gerencia as comunicações de saída (MQTT e HTTP POST). """
    
    def __init__(self, mqtt_host, mqtt_port, mqtt_topic, java_endpoint):
        self.mqtt_topic = mqtt_topic
        self.java_endpoint = java_endpoint
        
        self.http_session = requests.Session()
        print("Sessão HTTP iniciada. Endpoint Java:", self.java_endpoint)
        
        self.mqtt_client = self._setup_mqtt(mqtt_host, mqtt_port)
        if self.mqtt_client:
            self.mqtt_client.loop_start() # Inicia loop em thread separada
            
    def _setup_mqtt(self, host, port):
        """ Configura e conecta o cliente MQTT. """
        
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Conectado ao Broker MQTT em {host}")
            else:
                print(f"Falha ao conectar ao MQTT, código de retorno: {rc}")

        def on_disconnect(client, userdata, rc):
            print("Desconectado do Broker MQTT.")

        try:
            client_id = f'python-detector-{os.getpid()}'
            client = mqtt.Client(client_id)
            client.on_connect = on_connect
            client.on_disconnect = on_disconnect
            client.connect(host, port, 60)
            return client
        except Exception as e:
            print(f"Não foi possível iniciar o cliente MQTT: {e}")
            return None

    def publish_results(self, detections, source_url):
        """ Envia os dados de detecção para MQTT e Java API. """
        
        # --- 1. LÓGICA DO MQTT (SEM ALTERAÇÃO) ---
        # Prepara o payload de LOTE para o MQTT
        mqtt_payload = {
            "timestamp_ns": time.time_ns(),
            "source_url": source_url,
            "detections": detections
        }
        mqtt_payload_json = json.dumps(mqtt_payload)

        # Publica no MQTT
        if self.mqtt_client and self.mqtt_client.is_connected():
            try:
                self.mqtt_client.publish(self.mqtt_topic, mqtt_payload_json)
                print(f"Publicado no MQTT (Tópico: {self.mqtt_topic})")
            except Exception as e:
                print(f"Erro ao publicar no MQTT: {e}")
        else:
            print("Cliente MQTT não conectado. Pulando publicação.")

        # --- 2. LÓGICA DO POST PARA O JAVA (ALTERADO) ---
        # Itera sobre cada detecção e envia individualmente
        
        if not detections:
            return # Se não houver detecções, não faz nada
            
        print(f"Enviando {len(detections)} classificações para o Java API...")

        for detection in detections:
            
            # Pega a data/hora atual no formato ISO (exigido pelo LocalDateTime)
            now_iso_format = datetime.datetime.now().isoformat()

            # Mapeia os dados do Python para o formato esperado pelo ResidueDTO
            java_payload = {
                "classification": detection.get("class_name", "Desconhecido"),
                "reliability": detection.get("score", 0.0),
                "date": now_iso_format
            }
            
            java_payload_json = json.dumps(java_payload)

            # Envia o POST para o endpoint /api/residues/classify
            try:
                response = self.http_session.post(
                    self.java_endpoint,
                    data=java_payload_json, # <-- Envia o payload individual
                    headers={'Content-Type': 'application/json'},
                    timeout=2.0 
                )
                
                # Log para sabermos se o item foi enviado
                if 200 <= response.status_code < 300:
                    print(f"  -> Sucesso ({response.status_code}): {java_payload['classification']}")
                else:
                    print(f"  -> Erro ({response.status_code}) ao enviar: {java_payload['classification']}")
                    print(f"     Resposta do servidor: {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"  -> Exceção de conexão ao enviar: {e}")

    def close(self):
        """ Encerra as conexões de forma limpa. """
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("Conexão MQTT encerrada.")
        self.http_session.close()
        print("Sessão HTTP encerrada.")