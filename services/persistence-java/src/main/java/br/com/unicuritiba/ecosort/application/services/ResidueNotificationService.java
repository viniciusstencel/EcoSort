package br.com.unicuritiba.ecosort.application.services;

import br.com.unicuritiba.ecosort.domain.dto.ResidueDTO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

@Service
public class ResidueNotificationService {

    // Adicionar estas duas linhas:
    private static final Logger logger = LoggerFactory.getLogger(ResidueNotificationService.class);

    public static final String DESTINATION_TOPIC = "/topic/residues";

    private final SimpMessagingTemplate messagingTemplate;

    @Autowired
    public ResidueNotificationService(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;
    }

    public void sendResidueUpdate(ResidueDTO residue) {
        try {
            logger.info("Tentando enviar resíduo para o tópico: {}", DESTINATION_TOPIC); // <-- Adicionar
            messagingTemplate.convertAndSend(DESTINATION_TOPIC, residue);
            logger.info("Resíduo enviado com sucesso: {}", residue.classification()); // <-- Adicionar

        } catch (Exception e) {
            // Se algo der errado, veremos isso no log do Spring Boot
            logger.error("!!! FALHA AO ENVIAR MENSAGEM WEBSOCKET !!!", e); // <-- Adicionar
        }
    }
}