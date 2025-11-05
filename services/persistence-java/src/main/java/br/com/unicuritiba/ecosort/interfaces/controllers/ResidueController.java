package br.com.unicuritiba.ecosort.interfaces.controllers;


import br.com.unicuritiba.ecosort.application.services.ResidueNotificationService;
import br.com.unicuritiba.ecosort.domain.dto.ResidueDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/residues") // <-- Endpoint atualizado (antes era /api/test-residue)
public class ResidueController {

    private final ResidueNotificationService notificationService;

    @Autowired
    public ResidueController(ResidueNotificationService notificationService) {
        this.notificationService = notificationService;
    }

    /**
     * Endpoint principal para o serviço Python enviar uma nova classificação.
     * Recebe o DTO e o transmite via WebSocket.
     */
    @PostMapping("/classify") // <-- Endpoint atualizado (antes era /broadcast)
    public ResponseEntity<String> receiveResidueClassification(@RequestBody ResidueDTO residue) {

        // Envia a atualização para o front-end
        notificationService.sendResidueUpdate(residue);

        // Retorna "OK" para o Python
        return ResponseEntity.ok("Residue classification received: " + residue.classification());
    }

    /**
     * (Opcional) Endpoint de teste simples, caso você ainda precise.
     */
    @PostMapping("/test-broadcast") // <-- Endpoint atualizado (antes era /broadcast-simples)
    public ResponseEntity<String> testBroadcastSimples() {

        ResidueDTO residue = new ResidueDTO(
                "Simulated Test Residue",
                0.99f,
                LocalDateTime.now()
        );

        notificationService.sendResidueUpdate(residue);

        return ResponseEntity.ok("Simulated residue message sent.");
    }
}