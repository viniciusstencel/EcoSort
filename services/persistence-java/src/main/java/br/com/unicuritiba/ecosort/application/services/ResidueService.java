package br.com.unicuritiba.ecosort.application.services;

import br.com.unicuritiba.ecosort.domain.dto.ResidueDTO;
import br.com.unicuritiba.ecosort.domain.models.Residue;
import br.com.unicuritiba.ecosort.domain.repositories.ResidueRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ResidueService {

    private final ResidueRepository residueRepository;

    private final ResidueNotificationService notificationService;

    @Autowired
    public ResidueService(
            ResidueRepository residueRepository,
            ResidueNotificationService residueNotificationService ){

        this.residueRepository = residueRepository;
        this.notificationService = residueNotificationService;
    }

    @Transactional
    public Residue saveAndNotify(ResidueDTO dto) {

        Residue residueEntity = new Residue();
        residueEntity.setClassification(dto.classification());
        residueEntity.setReliability(dto.reliability());
        residueEntity.setDate(dto.date());

        Residue savedResidue = residueRepository.save(residueEntity);

        notificationService.sendResidueUpdate(dto);

        return savedResidue;

    }

    public List<Residue> getHistory() {
        // Busca todos, ordenando por "date" em ordem descendente
        return residueRepository.findAll(Sort.by(Sort.Direction.DESC, "date"));
    }


}
