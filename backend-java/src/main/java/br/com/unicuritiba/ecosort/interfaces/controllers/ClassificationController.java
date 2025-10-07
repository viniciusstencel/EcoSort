package br.com.unicuritiba.ecosort.interfaces.controllers;

import br.com.unicuritiba.ecosort.application.services.ClassificationService;
import br.com.unicuritiba.ecosort.domain.dto.AiClassificationResponseDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/analisar")
public class ClassificationController {

    @Autowired
    private ClassificationService service;

    @PostMapping
    public ResponseEntity<AiClassificationResponseDto> analyzeResidue(MultipartFile image) {
        return ResponseEntity.ok(service.classificationResidue(image));
    }
}
