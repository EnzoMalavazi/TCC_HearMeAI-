import whisper
import sounddevice as sd
import numpy as np
import queue
import threading
import tkinter as tk
from tkinter import scrolledtext

# Configurações
SAMPLERATE = 16000  # Taxa de amostragem do áudio (16 kHz)
CHUNK_SIZE = 2048   # Tamanho de cada pedaço de áudio (em frames)
MODEL_TYPE = "small"  # Escolha o modelo do Whisper (tiny, base, small, medium, large)

# Carregar o modelo Whisper
print("Carregando modelo Whisper...")
model = whisper.load_model(MODEL_TYPE)
print("Modelo carregado!")

# Fila para armazenar os chunks de áudio
audio_queue = queue.Queue()

# Função para capturar áudio em tempo real
def capturar_audio():
    def callback(indata, frames, time, status):
        if status:
            print(status, flush=True)
        audio_queue.put(indata.copy())

    with sd.InputStream(samplerate=SAMPLERATE, channels=1, dtype='float32', callback=callback):
        print("Capturando áudio... Pressione Ctrl+C para parar.")
        while True:
            sd.sleep(1000)

# Função para transcrever áudio em tempo real
def transcrever_audio():
    while True:
        if not audio_queue.empty():
            # Coletar chunks de áudio da fila
            chunks = []
            while not audio_queue.empty():
                chunks.append(audio_queue.get())

            # Concatenar os chunks em um único array
            audio_data = np.concatenate(chunks)

            # Verificar se o áudio tem um tamanho razoável
            if len(audio_data) > 0:
                try:
                    # Converter o áudio para o formato esperado pelo Whisper (16 kHz, mono)
                    audio_data = audio_data.astype(np.float32)  # Certificar-se de que está no formato float32
                    audio_data = audio_data.flatten()  # Certificar-se de que está em formato mono

                    # Transcrever o áudio usando o Whisper
                    result = model.transcribe(audio_data, language="pt")
                    texto = result["text"]

                    # Exibir o texto transcrito na interface
                    texto_transcrito.insert(tk.END, texto + "\n")
                    texto_transcrito.see(tk.END)  # Rolagem automática para o final
                except Exception as e:
                    print(f"Erro durante a transcrição: {e}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Transcrição em Tempo Real com Whisper")

texto_transcrito = scrolledtext.ScrolledText(root, height=20, width=80)
texto_transcrito.pack()

# Iniciar threads para captura e transcrição
threading.Thread(target=capturar_audio, daemon=True).start()
threading.Thread(target=transcrever_audio, daemon=True).start()

root.mainloop()