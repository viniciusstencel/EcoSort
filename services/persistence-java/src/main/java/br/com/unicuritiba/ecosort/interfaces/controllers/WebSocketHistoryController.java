package br.com.unicuritiba.ecosort.interfaces.controllers;

import br.com.unicuritiba.ecosort.application.services.ResidueService;
import br.com.unicuritiba.ecosort.domain.models.Residue;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.annotation.SendToUser;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
public class WebSocketHistoryController {

    private final ResidueService residueService;

    @Autowired
    public WebSocketHistoryController(ResidueService residueService) {
        this.residueService = residueService;
    }

    /**
     * Este método é acionado quando um cliente envia uma mensagem para "/app/request-history".
     * A anotação @SendToUser faz o Spring magicamente enviar o retorno
     * DE VOLTA apenas para o cliente que fez a requisição, no destino "/user/queue/history".
     */
    @MessageMapping("/request-history")
    @SendToUser("/queue/history")
    public List<Residue> fetchHistory() {
        // 1. O cliente chama "/app/request-history"
        System.out.println("Recebido pedido de histórico...");

        // 2. Busca no banco
        List<Residue> history = residueService.getHistory();

        // 3. O Spring envia a lista de volta para "/user/{session-id}/queue/history"
        return history;
    }

}
