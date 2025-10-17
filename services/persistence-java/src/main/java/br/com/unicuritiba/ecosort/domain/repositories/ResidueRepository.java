package br.com.unicuritiba.ecosort.domain.repositories;

import br.com.unicuritiba.ecosort.domain.models.Residue;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.UUID;

public interface ResidueRepository extends JpaRepository<Residue, UUID> {
}
