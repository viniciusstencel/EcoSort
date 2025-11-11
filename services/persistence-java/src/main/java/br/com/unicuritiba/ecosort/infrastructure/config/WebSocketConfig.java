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
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        // /topic é para broadcast (novas classificações para todos)
        // /queue é para mensagens privadas (o histórico para um usuário)
        registry.enableSimpleBroker("/topic", "/queue");

        registry.setApplicationDestinationPrefixes("/app");

        // Define o prefixo para destinos de usuário (essencial para @SendToUser)
        registry.setUserDestinationPrefix("/user");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // Seu endpoint de conexão
        registry.addEndpoint("/ws-connect")
                //.setAllowedOrigins("chrome-extension://lhbjghocjpcoecemiikamjijoonopgll", "http://127.0.0.1:5500")
                .setAllowedOriginPatterns("*")
                .withSockJS();
    }
}