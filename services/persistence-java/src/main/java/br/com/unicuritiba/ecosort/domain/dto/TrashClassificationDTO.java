package br.com.unicuritiba.ecosort.domain.dto;

import java.time.Instant;

public record TrashClassificationDTO(
        String lixoClassificado,
        Instant timestamp,
        double confianca
) {

}
