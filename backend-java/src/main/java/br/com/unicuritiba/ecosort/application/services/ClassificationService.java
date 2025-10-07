package br.com.unicuritiba.ecosort.application.services;

import br.com.unicuritiba.ecosort.AiClassificationRequest;
import br.com.unicuritiba.ecosort.AiClassificationResponse;
import br.com.unicuritiba.ecosort.domain.dto.AiClassificationResponseDto;
import br.com.unicuritiba.ecosort.integrations.ai.ClassificationServiceClient;
import com.google.protobuf.ByteString;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class ClassificationService {

    private final ClassificationServiceClient grpcClient;

    public AiClassificationResponseDto classificationResidue(MultipartFile image) {
        AiClassificationResponse residue = analyzeClassification(image);
        return AiClassificationResponseDto.fromGrpcResponse(residue);
    }

    public AiClassificationResponse analyzeClassification(MultipartFile image) {
        try {
            byte[] imageBytes = image.getBytes();
            ByteString data = ByteString.copyFrom(imageBytes);

            AiClassificationRequest request = AiClassificationRequest.newBuilder()
                    .setData(data)
                    .build();

            return grpcClient.analyze(request);

        } catch (Exception e) {
            System.err.println("❌ Erro ao chamar IA via gRPC: " + e.getMessage());
            e.printStackTrace();
            throw new RuntimeException("Erro ao chamar serviço de IA", e);
        }
    }
    public ClassificationService(ClassificationServiceClient grpcClient) {
        this.grpcClient = grpcClient;
    }
}
