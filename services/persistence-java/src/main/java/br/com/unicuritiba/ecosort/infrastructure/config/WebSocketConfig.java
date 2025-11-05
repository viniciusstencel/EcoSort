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
        registry.enableSimpleBroker("/topic");
        registry.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {

        // COLE O SEU ID DA EXTENSÃO AQUI
        // Ex: "chrome-extension://lhbjghocjpcoecemiikamjijoonopgll"
        String idDaSuaExtensao = "chrome-extension://COLE_SEU_ID_AQUI";


        registry.addEndpoint("/ws-connect")

                // Em vez de .allowedOriginPatterns("*"),
                // nós autorizamos explicitamente a extensão:
                .setAllowedOrigins("chrome-extension://lhbjghocjpcoecemiikamjijoonopgll")

                // A extensão precisa disto:
                .withSockJS();
    }
}