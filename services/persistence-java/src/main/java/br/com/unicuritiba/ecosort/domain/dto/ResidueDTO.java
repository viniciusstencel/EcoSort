package br.com.unicuritiba.ecosort.domain.dto;

import java.time.Instant;
import java.time.LocalDateTime;

public record ResidueDTO(
        String classification,
        float reliability,
        LocalDateTime date

) {

}
