#include <WiFi.h>
#include <ESPAsyncWebServer.h> // Servidor Assíncrono
#include <AsyncTCP.h>          // Dependência
#include "esp_camera.h"
#include <ESP32Servo.h>

// ================= CONFIGURAÇÕES DE REDE ===================

// --- Credenciais Wi-Fi ---
const char* ssid = "Felipe";
const char* password = "1610242126";

// ================= CONFIGURAÇÕES DO SISTEMA ===================
#define ENABLE_CAMERA true 

// --- CORREÇÃO DA CÂMERA (MODELO) ---
#define CAMERA_MODEL_M5STACK_ESP32CAM 
#include "camera_pins.h" 

// Servos
Servo servoInferior;
Servo servoSuperior;
#define SERVO_PIN_INFERIOR 13
#define SERVO_PIN_SUPERIOR 12

// Posições dos servos
#define SERVO_INFERIOR_INICIAL 90
#define SERVO_SUPERIOR_INICIAL 120
#define SERVO_INFERIOR_PAPER 40
#define SERVO_SUPERIOR_PAPER 140
#define SERVO_INFERIOR_PLASTIC 140
#define SERVO_SUPERIOR_PLASTIC 45
#define SERVO_INFERIOR_ORGANIC 40
#define SERVO_SUPERIOR_ORGANIC 45
#define SERVO_INFERIOR_METAL 140
#define SERVO_SUPERIOR_METAL 140

// Variáveis para o reset automático
unsigned long lastMoveTime = 0;
bool resetPending = false;
#define RESET_DELAY 3000 // 3 segundos para resetar

// MUDANÇA: Usando AsyncWebServer
AsyncWebServer server(80);

// ================= FUNÇÃO DE CLASSIFICAÇÃO ===================
void handleClassification(String command) {
  Serial.print(">>> CLASSIFY REQUEST RECEIVED: ");
  Serial.println(command);

  int targetInferior = SERVO_INFERIOR_INICIAL;
  int targetSuperior = SERVO_SUPERIOR_INICIAL;

  if (command == "paper") {
    targetInferior = SERVO_INFERIOR_PAPER;
    targetSuperior = SERVO_SUPERIOR_PAPER;
  } else if (command == "plastic") {
    targetInferior = SERVO_INFERIOR_PLASTIC;
    targetSuperior = SERVO_SUPERIOR_PLASTIC;
  } else if (command == "organic") {
    targetInferior = SERVO_INFERIOR_ORGANIC;
    targetSuperior = SERVO_SUPERIOR_ORGANIC;
  } else if (command == "metal") {
    targetInferior = SERVO_INFERIOR_METAL;
    targetSuperior = SERVO_SUPERIOR_METAL;
  } else {
    Serial.println("Comando desconhecido. Nenhum motor foi movido.");
    return;
  }

  servoInferior.write(targetInferior);
  servoSuperior.write(targetSuperior);

  Serial.printf("Servos movidos -> Inferior: %d | Superior: %d\n", targetInferior, targetSuperior);
  
  lastMoveTime = millis(); 
  resetPending = true;     
}

// ================= FRONT-END HTML SIMPLIFICADO ===================
String htmlPage() {
  return R"rawliteral(
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EcoSort IOT - Captura</title>
<style>
body { 
  font-family: Arial, sans-serif; 
  text-align: center; 
  background: #f3f3f3; 
  margin: 0; 
  padding: 20px; 
  display: flex;
  flex-direction: column;
  align-items: center;
}
h1 { color: #2a7d2e; }
.button-container { 
  display: flex; 
  justify-content: center; 
  flex-wrap: wrap; 
  margin-top: 10px; 
  margin-bottom: 20px; 
  max-width: 640px; /* Limita o container dos botões */
  width: 100%;
}
button { 
  padding: 12px 22px; 
  margin: 8px; 
  border: none; 
  border-radius: 8px; 
  cursor: pointer; 
  font-size: 16px; 
  font-weight: bold; 
  transition: transform 0.1s, box-shadow 0.1s; 
  box-shadow: 0 4px #aaa;
  flex: 1 1 120px; /* Botões flexíveis */
}
button:active {
    transform: translateY(2px) scale(0.98); 
    box-shadow: 0 2px #aaa;
}
#capture { background: #b1a0c7; color: #3d354b; } /* Roxo para o botão de foto */
#paper { background: #ffd966; color: #5c4b1e; } /* Amarelo */
#plastic { background: #ff6961; color: #5f2725; } /* Vermelho */
#organic { background: #77dd77; color: #2c522c; } /* Verde */
#metal { background: #aec6cf; color: #435054; } /* Cinza/Azul */
#status { margin-top: 20px; margin-bottom: 20px; font-weight: bold; color: #444; font-size: 18px; }

/* Container focado em uma única imagem */
.image-container {
  max-width: 640px; 
  width: 100%;
  padding: 10px;
}
.image-item {
    text-align: center;
}

/* Estilo para a foto capturada */
#captured-img {
    border: 2px solid #2a7d2e; 
    border-radius: 8px; 
    width: 100%; 
    height: auto;
    display: block;
    margin: 10px 0;
} 
</style>
</head>
<body>
<h1>EcoSort - Captura e Classificação</h1>

<div class="button-container">
  <button id="capture" onclick="captureImage()">Tirar Foto</button>
  <button id="paper" onclick="sendCommand('paper')">Papel</button>
  <button id="plastic" onclick="sendCommand('plastic')">Plástico</button>
  <button id="organic" onclick="sendCommand('organic')">Orgânico</button>
  <button id="metal" onclick="sendCommand('metal')">Metal</button>
</div>
<div id="status">Aguardando comando...</div>

<div class="image-container">
    <div class="image-item">
        <h2>Última Foto Capturada</h2>
        <img id="captured-img" src="https://placehold.co/640x480/cccccc/333333?text=Clique+em+'Tirar+Foto'" alt="Foto Capturada">
    </div>
</div>

<script>
function sendCommand(cmd){
  fetch(`/classify?cmd=${cmd}`).then(r=>r.text()).then(res=>{
    let statusEl = document.getElementById('status');
    let cmdText = cmd.charAt(0).toUpperCase() + cmd.slice(1);
    
    statusEl.innerText = `Comando Enviado: ${cmdText}. Servos em movimento.`;
    
    // Reseta o status após um tempo
    setTimeout(() => {
        if (statusEl.innerText.startsWith('Comando Enviado:')) {
            statusEl.innerText = 'Aguardando comando...';
        }
    }, 4000); 
  }).catch(error => {
    document.getElementById('status').innerText = 'ERRO: Não foi possível alcançar o ESP32.';
    console.error('Fetch error:', error);
  });
}

function captureImage(){
  document.getElementById('status').innerText = 'Capturando imagem... Aguarde...';
  
  // Faz o fetch do endpoint de captura estática
  fetch('/capture')
    .then(response => {
      if (!response.ok) {
        throw new Error('Falha ao capturar imagem. Status: ' + response.status);
      }
      return response.blob();
    })
    .then(imageBlob => {
      // Cria uma URL local para o blob da imagem
      const imageUrl = URL.createObjectURL(imageBlob);
      document.getElementById('captured-img').src = imageUrl;
      document.getElementById('status').innerText = 'Imagem capturada com sucesso! Pronto para classificação.';
    })
    .catch(error => {
      document.getElementById('status').innerText = 'ERRO: Falha na captura. Verifique o console.';
      console.error('Capture error:', error);
    });
}
</script>
</body>
</html>
)rawliteral";
}

// ================= HANDLER DE CAPTURA ESTÁTICA ===================
void handleCapture(AsyncWebServerRequest *request) {
  if (!ENABLE_CAMERA) {
    request->send(204, "text/plain", "Camera disabled");
    return;
  }
  
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Falha ao capturar frame para foto");
    request->send(500, "text/plain", "Camera capture failed");
    return;
  }

  // Envia o JPEG estático
  AsyncWebServerResponse *response = request->beginResponse(200, "image/jpeg", fb->buf, fb->len);
  
  response->addHeader("Content-Disposition", "inline; filename=capture.jpg");
  
  request->send(response);
  
  esp_camera_fb_return(fb);
}

// REMOVIDA A FUNÇÃO handleStream

// Handler de 404
void notFound(AsyncWebServerRequest *request) {
  request->send(404, "text/plain", "Not found");
}


// ================= SETUP ===================
void setup() {
  Serial.begin(115200);
  delay(3000);
  Serial.println("\n\n===== INICIALIZANDO SISTEMA EcoSort =====");

  servoInferior.attach(SERVO_PIN_INFERIOR);
  servoSuperior.attach(SERVO_PIN_SUPERIOR);
  servoInferior.write(SERVO_INFERIOR_INICIAL);
  servoSuperior.write(SERVO_SUPERIOR_INICIAL);

  if (ENABLE_CAMERA) {
    camera_config_t config;

    // ========================================================
    // == INÍCIO DA REFATORAÇÃO (CORREÇÃO DE TIMER) ==
    //
    // Mudamos o timer da câmera de 0 para 1.
    // A biblioteca ESP32Servo usa o TIMER_0 por padrão.
    // A biblioteca da Câmera também usava o TIMER_0.
    // Esse conflito pelo mesmo recurso de hardware causa
    // a tremedeira (jitter) nos servos.
    //
    // Ao mover a câmera para o TIMER_1, liberamos o TIMER_0
    // exclusivamente para os servos.
    
    config.ledc_channel = LEDC_CHANNEL_1; // Estava LEDC_CHANNEL_0
    config.ledc_timer = LEDC_TIMER_1;     // Estava LEDC_TIMER_0
    
    // == FIM DA REFATORAÇÃO ==
    // ========================================================
    
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 10000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_QVGA; 
    config.jpeg_quality = 10;           
    config.fb_count = 1;

    if (esp_camera_init(&config) != ESP_OK) {
      Serial.println("Falha ao iniciar câmera!");
    } else {
      Serial.println("Câmera iniciada com sucesso!");
    }
  }

  // --- Conexão WiFi ---
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Conectando à rede WiFi: ");
  Serial.println(ssid);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    attempts++;
    if (attempts > 30) { 
      Serial.println("\nFalha ao conectar. Reiniciando...");
      ESP.restart();
    }
  }

  Serial.println("\nWiFi conectado!");
  Serial.print("IP atual: ");
  Serial.println(WiFi.localIP()); 

  // Mapeamento das rotas para o Servidor Assíncrono
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", htmlPage());
  });

  server.on("/classify", HTTP_GET, [](AsyncWebServerRequest *request){
    String cmd = request->arg("cmd"); 
    handleClassification(cmd);
    request->send(200, "text/plain", "OK");
  });

  // ROTA PARA CAPTURA ESTÁTICA
  server.on("/capture", HTTP_GET, handleCapture);

  server.onNotFound(notFound);
  server.begin();

  Serial.println("Servidor HTTP Assíncrono iniciado com sucesso!");
}

// ================= LOOP ===================
void loop() {
  // O loop cuida apenas do reset dos servos após a classificação.
  if (resetPending && (millis() - lastMoveTime > RESET_DELAY)) {
    
    Serial.println("Resetando servos para a posição inicial...");
    
    servoInferior.write(SERVO_INFERIOR_INICIAL);
    delay(300);
    servoSuperior.write(SERVO_SUPERIOR_INICIAL);
    
    resetPending = false; 
  }
}