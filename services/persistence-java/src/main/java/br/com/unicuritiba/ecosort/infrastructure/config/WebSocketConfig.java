package br.com.unicuritiba.ecosort.infrastructure.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.messaging.simp.config.MessageBrokerRegistry;
import org.springframework.web.socket.config.annotation.EnableWebSocketMessageBroker;
import org.springframework.web.socket.config.annotation.StompEndpointRegistry;
import org.springframework.web.socket.config.annotation.WebSocketMessageBrokerConfigurer;

@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry){
        /*
         * Configura o "broker" de mensagens.
         * /topic: Destinos que começam com "/topic" são roteados para o broker
         * (ou seja, transmitidos para todos os clientes inscritos).
         * É para onde o Java vai enviar os dados.
         */
        registry.enableSimpleBroker("/topic");

        /*
         * (Opcional, mas recomendado)
         * Define o prefixo para destinos de "aplicação".
         * Se o front-end quisesse ENVIAR uma mensagem para o back-end (não é o seu caso),
         * ele enviaria para algo como "/app/algumaCoisa".
         */
        registry.setApplicationDestinationPrefixes("/app");

    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        /*
         * Expõe o endpoint HTTP onde o front-end irá se conectar
         * para iniciar a comunicação WebSocket.
         * * O front-end vai se conectar a "http://localhost:8080/ws-connect"
         */
        registry.addEndpoint("/ws-connect")

                // Permite conexões de qualquer origem.
                // MUITO IMPORTANTE para desenvolvimento (React/Angular/etc)
                .setAllowedOrigins("*")

                // Adiciona suporte a SockJS como um "fallback" para navegadores
                // que não suportam WebSockets nativamente.
                .withSockJS();
    }


}
