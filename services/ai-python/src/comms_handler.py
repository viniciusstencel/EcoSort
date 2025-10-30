# comms_handler.py

import paho.mqtt.client as mqtt
import requests
import json
import time
import os

class CommsHandler:
    """ Gerencia as comunicações de saída (MQTT e HTTP POST). """
    
    def __init__(self, mqtt_host, mqtt_port, mqtt_topic, java_endpoint):
        self.mqtt_topic = mqtt_topic
        self.java_endpoint = java_endpoint
        
        self.http_session = requests.Session()
        print("Sessão HTTP iniciada.")
        
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
        
        # 1. Prepara o payload
        payload = {
            "timestamp_ns": time.time_ns(),
            "source_url": source_url,
            "detections": detections
        }
        payload_json = json.dumps(payload)

        # 2. Publica no MQTT
        if self.mqtt_client and self.mqtt_client.is_connected():
            try:
                self.mqtt_client.publish(self.mqtt_topic, payload_json)
                print(f"Publicado no MQTT (Tópico: {self.mqtt_topic})")
            except Exception as e:
                print(f"Erro ao publicar no MQTT: {e}")
        else:
            print("Cliente MQTT não conectado. Pulando publicação.")

        # 3. Envia POST para o serviço Java
        try:
            response = self.http_session.post(
                self.java_endpoint,
                data=payload_json,
                headers={'Content-Type': 'application/json'},
                timeout=2.0 
            )
            print(f"POST para Java API enviado (Status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar POST para Java API: {e}")

    def close(self):
        """ Encerra as conexões de forma limpa. """
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            print("Conexão MQTT encerrada.")
        self.http_session.close()
        print("Sessão HTTP encerrada.")