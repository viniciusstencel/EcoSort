package br.com.unicuritiba.ecosort.interfaces.controllers;


import br.com.unicuritiba.ecosort.application.services.ResidueNotificationService;
import br.com.unicuritiba.ecosort.application.services.ResidueService;
import br.com.unicuritiba.ecosort.domain.dto.ResidueDTO;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/residues")
public class ResidueController {

    private final ResidueNotificationService notificationService;

    private final ResidueService residueService;

    @Autowired
    public ResidueController(ResidueNotificationService notificationService,
                             ResidueService residueService) {
        this.notificationService = notificationService;
        this.residueService = residueService;
    }

    /**
     * Endpoint principal para o serviço Python enviar uma nova classificação.
     * Recebe o DTO e o transmite via WebSocket.
     */
    @PostMapping("/classify") // <-- Endpoint atualizado (antes era /broadcast)
    public ResponseEntity<String> receiveResidueClassification(@RequestBody ResidueDTO residue) {

        try {
            // Delega TODA a lógica para o ResidueService
            residueService.saveAndNotify(residue);

            // Retorna "OK" para o Python
            return ResponseEntity.ok("Residue classification received and saved: " + residue.classification());

        } catch (Exception e) {
            return ResponseEntity.status(500).body("Error processing residue: " + e.getMessage());
        }
    }

    @PostMapping("/test-broadcast") // <-- Endpoint de residuo teste.
    public ResponseEntity<String> testBroadcastSimples() {

        ResidueDTO residue = new ResidueDTO(
                "Simulated Test Residue",
                0.99f,
                LocalDateTime.now()
        );

        //notificationService.sendResidueUpdate(residue);

        residueService.saveAndNotify(residue);

        return ResponseEntity.ok("Simulated residue message sent.");
    }
}