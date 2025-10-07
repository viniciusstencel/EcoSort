package br.com.unicuritiba.ecosort.integrations.ai;

import br.com.unicuritiba.ecosort.AiClassificationRequest;
import br.com.unicuritiba.ecosort.AiClassificationResponse;
import br.com.unicuritiba.ecosort.AiClassificationServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class ClassificationServiceClient {
    @Value("${grpc.server.host}")
    private String host;

    @Value("${grpc.server.port}")
    private int port;

    private AiClassificationServiceGrpc.AiClassificationServiceBlockingStub stub;

    @PostConstruct
    public void init() {
        ManagedChannel channel = ManagedChannelBuilder
                .forAddress(host, port)
                .usePlaintext()
                .build();

        this.stub = AiClassificationServiceGrpc.newBlockingStub(channel);
    }

    public AiClassificationResponse analyze(AiClassificationRequest request) {
        return stub.aiClassification(request);
    }
}
