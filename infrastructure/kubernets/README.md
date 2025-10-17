# 🐳 Funcionalidade do Kubernetes (K8s) no Projeto EcoSort

O **Kubernetes** é a nossa plataforma de orquestração, atuando como o **gerente de infraestrutura** de todos os nossos microsserviços (IA Python, Backend Java, Kafka, PostgreSQL).

Sua principal funcionalidade é garantir que o sistema EcoSort seja **altamente disponível, escalável e resiliente** em um ambiente de produção.

---

## 💡 Papel e Atuação no Ciclo de Vida do Serviço

O Kubernetes gerencia tudo o que acontece após o código ser construído, assegurando que o sistema opere continuamente:

### 1. Garantia de Estabilidade (Autocorreção)

* **O Problema:** O Serviço IA (Python) é complexo e pode falhar devido a erros de processamento de imagem ou falta de memória.
* **Ação do K8s:** O Kubernetes monitora constantemente o estado de todos os *Pods*. Se o Pod do Serviço IA falhar ou parar de responder, o K8s o **derruba e reinicia automaticamente** em segundos.
* **Benefício:** O sistema tem **autocorreção** e o tempo de inatividade (downtime) é minimizado sem intervenção humana.

### 2. Controle de Demanda (Escalabilidade Automática)

* **O Problema:** Em momentos de alto volume de resíduos (muitos itens passando pela câmera IoT), o Serviço IA pode ficar sobrecarregado.
* **Ação do K8s:** Utilizando o **Horizontal Pod Autoscaler (HPA)**, o Kubernetes observa métricas como o uso de CPU. Se a carga subir, ele **cria automaticamente novos Pods** (instâncias) do Serviço IA e do Backend Java para distribuir o trabalho.
* **Benefício:** A performance é mantida sob demanda, e os recursos são utilizados de forma eficiente.

### 3. Comunicação Estável (Descoberta de Serviços)

* **O Problema:** Os Pods (instâncias) de IA, Java e Kafka estão sempre mudando de endereço IP no cluster.
* **Ação do K8s:** O K8s usa o objeto **Service** para fornecer um nome de rede e um IP interno **estável e fixo** para cada componente (ex: `kafka-broker`, `postgres-db`).
* **Benefício:** O Serviço IA sabe que pode acessar o Kafka simplesmente pelo nome `kafka-broker`, e o Kubernetes se encarrega de rotear o tráfego para a instância correta.

### 4. Atualizações Seguras (*Rolling Updates*)

* **O Problema:** Implantar uma nova versão do Backend Java pode exigir que o serviço fique fora do ar por alguns minutos.
* **Ação do K8s:** O K8s executa atualizações (*Deployments*) sem interrupção (zero downtime). Ele sobe a nova versão do Pod, garante que ela está saudável, e só então derruba a versão antiga.
* **Benefício:** Lançamentos de novas funcionalidades ou correções de bugs são rápidos e não afetam a operação contínua do sistema de separação de resíduos.

---

## 🎯 Resumo da Contribuição do Kubernetes

| Funcionalidade | Resultado no Projeto |
| :--- | :--- |
| **Resiliência** | O sistema se cura automaticamente de falhas de software ou hardware. |
| **Performance** | Otimiza o uso de recursos e escala serviços críticos (IA e Persistência) sob demanda. |
| **Implantação** | Permite que o código seja levado à produção de forma rápida, segura e contínua. |