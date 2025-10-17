package br.com.unicuritiba.ecosort.domain.models;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Getter;
import lombok.Setter;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "residues")
@Getter
@Setter
public class Residue {

    @Id
    UUID id;

    String classification;

    int numberOfClassification;

    float reliability;

    LocalDateTime date;


}
