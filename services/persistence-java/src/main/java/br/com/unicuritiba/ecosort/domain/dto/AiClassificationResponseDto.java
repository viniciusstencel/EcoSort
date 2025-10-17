package br.com.unicuritiba.ecosort.domain.dto;

import br.com.unicuritiba.ecosort.AiClassificationResponse;

public record AiClassificationResponseDto(
        int classId,
        String className,
        float confidence
) {
    public static AiClassificationResponseDto fromGrpcResponse(AiClassificationResponse grpcResponse) {
        return new AiClassificationResponseDto(
                grpcResponse.getClassId(),
                grpcResponse.getClassName(),
                grpcResponse.getConfidence()
        );
    }
}