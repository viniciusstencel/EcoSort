import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import matplotlib.pyplot as plt
import os

# --- 1. Parâmetros de Configuração ---
DATA_DIR = 'data'
IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 15 # Quantidade de vezes que o modelo verá o dataset completo
MODEL_SAVE_PATH = 'models/ecosort_classifier_v1.keras' # Onde salvar o modelo treinado

# Verifica se o diretório do dataset existe
if not os.path.exists(DATA_DIR) or not os.listdir(DATA_DIR):
    print(f"Erro: O diretório '{DATA_DIR}' não existe ou está vazio.")
    print("Por favor, crie-o e organize suas imagens de treinamento dentro dele.")
    exit()

# --- 2. Carregar e Preparar o Dataset ---
print("Carregando e preparando o dataset...")
# Carrega o dataset a partir dos diretórios, dividindo em treino (80%) e validação (20%)
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE
)

# Obtém os nomes das classes (serão os nomes das pastas: 'metal', 'papel', etc.)
class_names = train_ds.class_names
NUM_CLASSES = len(class_names)
print(f"Classes encontradas: {class_names}")

# Otimização de performance: pré-busca de dados
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# --- 3. Construir o Modelo (Transfer Learning) ---
print("Construindo o modelo com MobileNetV2...")

# Camada de aumento de dados (Data Augmentation) para evitar overfitting
data_augmentation = keras.Sequential([
    layers.RandomFlip("horizontal", input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# Carrega o modelo MobileNetV2 pré-treinado, sem a camada de classificação final
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_HEIGHT, IMG_WIDTH, 3),
    include_top=False, # Crucial para transfer learning
    weights='imagenet'
)

# Congela o modelo base para não treinar suas camadas
base_model.trainable = False

# Cria o modelo final
model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255), # Normaliza os pixels para o intervalo [0, 1]
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2), # Ajuda a prevenir overfitting
    layers.Dense(NUM_CLASSES, activation='softmax') # Nossa camada de classificação
])

# --- 4. Compilar o Modelo ---
print("Compilando o modelo...")
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

model.summary() # Mostra a arquitetura do modelo

# --- 5. Treinar o Modelo ---
print(f"Iniciando o treinamento por {EPOCHS} épocas...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# --- 6. Salvar o Modelo Treinado ---
print(f"Treinamento concluído! Salvando modelo em '{MODEL_SAVE_PATH}'...")
model.save(MODEL_SAVE_PATH)
print("Modelo salvo com sucesso!")

# --- (Opcional) 7. Visualizar Resultados ---
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(EPOCHS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Acurácia de Treino')
plt.plot(epochs_range, val_acc, label='Acurácia de Validação')
plt.legend(loc='lower right')
plt.title('Acurácia de Treino e Validação')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Perda de Treino')
plt.plot(epochs_range, val_loss, label='Perda de Validação')
plt.legend(loc='upper right')
plt.title('Perda de Treino e Validação')
plt.savefig('models/training_results.png')
print("Gráficos de resultado salvos em 'models/training_results.png'")