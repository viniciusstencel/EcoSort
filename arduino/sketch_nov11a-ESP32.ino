#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncTCP.h>
#include "esp_camera.h"
#include <ESP32Servo.h>
#include <ESPmDNS.h>

// ================= CONFIGURAÇÕES DE REDE ===================
const char* ssid = "Wifi-Janete";
const char* password = "Math3,14";

#define ENABLE_CAMERA true

#define CAMERA_MODEL_M5STACK_ESP32CAM
#include "camera_pins.h"

// Servos
Servo servoInferior;
Servo servoSuperior;
#define SERVO_PIN_INFERIOR 2
#define SERVO_PIN_SUPERIOR 13

// Posições
#define SERVO_INFERIOR_INICIAL 90
#define SERVO_SUPERIOR_INICIAL 95
#define SERVO_INFERIOR_PAPER 35
#define SERVO_SUPERIOR_PAPER 120
#define SERVO_INFERIOR_PLASTIC 110
#define SERVO_SUPERIOR_PLASTIC 20
#define SERVO_INFERIOR_ORGANIC 35
#define SERVO_SUPERIOR_ORGANIC 50
#define SERVO_INFERIOR_METAL 140
#define SERVO_SUPERIOR_METAL 120

unsigned long lastMoveTime = 0;
bool resetPending = false;
#define RESET_DELAY 3000

AsyncWebServer server(80);

// ====== CONTROLE DE MOVIMENTO SUAVE =======
int currentInferior = SERVO_INFERIOR_INICIAL;
int currentSuperior = SERVO_SUPERIOR_INICIAL;
int targetInferior = SERVO_INFERIOR_INICIAL;
int targetSuperior = SERVO_SUPERIOR_INICIAL;
unsigned long lastStepTime = 0;
#define STEP_INTERVAL 15

void updateServoSmooth() {
  if (millis() - lastStepTime < STEP_INTERVAL) return;
  lastStepTime = millis();

  bool moved = false;

  if (currentInferior < targetInferior) { currentInferior++; moved = true; }
  else if (currentInferior > targetInferior) { currentInferior--; moved = true; }

  if (currentSuperior < targetSuperior) { currentSuperior++; moved = true; }
  else if (currentSuperior > targetSuperior) { currentSuperior--; moved = true; }

  if (moved) {
    servoInferior.write(currentInferior);
    servoSuperior.write(currentSuperior);
  }
}

// ================= FUNÇÃO DE CLASSIFICAÇÃO ===================
void handleClassification(String command) {
  Serial.print(">>> CLASSIFY REQUEST RECEIVED: ");
  Serial.println(command);

  if (command == "default") {
    targetInferior = SERVO_INFERIOR_INICIAL;
    targetSuperior = SERVO_SUPERIOR_INICIAL;
  }
  else if (command == "paper") {
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
    Serial.println("Comando desconhecido.");
    return;
  }

  lastMoveTime = millis();
  resetPending = true;
}

// ================= HTML COMPLETO ===================
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
  max-width: 640px;
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
  box-shadow: 0 4px #aaa;
  flex: 1 1 120px;
}
button:active {
  transform: translateY(2px) scale(0.98);
  box-shadow: 0 2px #aaa;
}
#capture { background: #b1a0c7; color: #3d354b; }
#paper { background: #ffd966; color: #5c4b1e; }
#plastic { background: #ff6961; color: #5f2725; }
#organic { background: #77dd77; color: #2c522c; }
#metal { background: #aec6cf; color: #435054; }
#status { margin-top: 20px; font-weight: bold; color: #444; font-size: 18px; }
.image-container {
  max-width: 640px;
  width: 100%;
  padding: 10px;
}
.image-item { text-align: center; }
#captured-img {
  border: 2px solid #2a7d2e;
  border-radius: 8px;
  width: 100%;
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
  fetch(`/classify?cmd=${cmd}`)
  .then(r=>r.text())
  .then(()=>{
    const status = document.getElementById('status');
    status.innerText = `Comando enviado: ${cmd}`;
    setTimeout(()=>status.innerText='Aguardando comando...',3000);
  });
}

function captureImage(){
  document.getElementById('status').innerText='Capturando...';
  fetch('/capture')
  .then(r=>r.blob())
  .then(b=>{
    const imgURL = URL.createObjectURL(b);
    document.getElementById('captured-img').src = imgURL;
    document.getElementById('status').innerText='Imagem capturada!';
  });
}
</script>
</body>
</html>
)rawliteral";
}

// ================= CAPTURA ===================
void handleCapture(AsyncWebServerRequest *request) {
  if (!ENABLE_CAMERA) {
    request->send(204, "text/plain", "Camera disabled");
    return;
  }
  
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    request->send(500, "text/plain", "Camera capture failed");
    return;
  }

  AsyncWebServerResponse *response =
    request->beginResponse(200, "image/jpeg", fb->buf, fb->len);

  response->addHeader("Content-Disposition","inline; filename=capture.jpg");

  request->send(response);

  esp_camera_fb_return(fb);
}

// ================= SETUP ===================
void setup() {
  Serial.begin(115200);
  delay(1000);

  servoInferior.attach(SERVO_PIN_INFERIOR, 500, 2500);
  servoSuperior.attach(SERVO_PIN_SUPERIOR, 600, 2400);
  servoInferior.write(SERVO_INFERIOR_INICIAL);
  servoSuperior.write(SERVO_SUPERIOR_INICIAL);

  currentInferior = SERVO_INFERIOR_INICIAL;
  currentSuperior = SERVO_SUPERIOR_INICIAL;

  if (ENABLE_CAMERA) {
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
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

    esp_camera_init(&config);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Conectando");
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }

  Serial.println("\nWiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  if (MDNS.begin("ecosort")) {
      Serial.println("mDNS ativo: http://ecosort.local");
  } else {
      Serial.println("Erro ao iniciar mDNS");
  }

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *req){
    req->send(200, "text/html", htmlPage());
  });

  server.on("/classify", HTTP_GET, [](AsyncWebServerRequest *req){
    handleClassification(req->arg("cmd"));
    req->send(200, "text/plain", "OK");
  });

  server.on("/capture", HTTP_GET, handleCapture);

  server.begin();
  Serial.println("Servidor iniciado!");
}

// ================= LOOP ===================
void loop() {
  updateServoSmooth();

  if (resetPending && (millis() - lastMoveTime > RESET_DELAY)) {
    handleClassification("default");
    resetPending = false;
  }
}
