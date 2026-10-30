"""Transcrição dos áudios com Whisper small (roda no Colab com GPU T4).
Salva só o texto: os áudios ficam no Drive, fora do repositório (voz é dado pessoal)."""
import csv
from pathlib import Path

EXTENSOES = {".m4a", ".mp3", ".mp4", ".aac", ".wav", ".ogg", ".opus", ".flac", ".webm"}  # .ogg/.mp4 = áudios do WhatsApp


def carregar_audio(caminho, taxa=16000):
    """Lê o áudio direto do arquivo com o ffmpeg, em mono e 16 kHz.
    Ler pelo caminho (e não por streaming) funciona com .mp4, cujo índice fica no fim do arquivo."""
    import subprocess
    import numpy as np
    bruto = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(caminho),
                            "-ac", "1", "-ar", str(taxa), "-f", "f32le", "-"],
                           capture_output=True, check=True).stdout
    audio = np.frombuffer(bruto, np.float32)
    if audio.size == 0:
        raise ValueError(f"Áudio vazio ou ilegível: {caminho}")
    return audio


def transcrever_pasta(pasta_audios, saida_csv, modelo="openai/whisper-small"):
    import torch
    from transformers import pipeline
    asr = pipeline("automatic-speech-recognition", model=modelo,
                   device=0 if torch.cuda.is_available() else -1)
    arquivos = sorted(p for p in Path(pasta_audios).iterdir()
                      if p.suffix.lower() in EXTENSOES and p.stem.startswith("enu_"))
    linhas = []
    for p in arquivos:
        r = asr({"raw": carregar_audio(p), "sampling_rate": 16000},
                generate_kwargs={"language": "portuguese", "task": "transcribe"})
        linhas.append({"id": p.stem, "arquivo": p.name, "transcricao_bruta": r["text"].strip()})
        print(p.stem, "->", linhas[-1]["transcricao_bruta"])
    with open(saida_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "arquivo", "transcricao_bruta"])
        w.writeheader()
        w.writerows(linhas)
    return linhas
