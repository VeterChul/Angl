import time
from faster_whisper import WhisperModel

# Явно указываем GPU и float16 (для ускорения)
model = WhisperModel("tiny", device="cuda", compute_type="float16")

print("Модель загружена. Параметры:")
print(f"  device = cuda")
print(f"  compute_type = float16")

# Если есть тестовый аудиофайл, раскомментируйте и проверьте
# start = time.time()
# segments, info = model.transcribe("audio.wav", beam_size=5)
# for seg in segments:
#     print(f"[{seg.start:.2f} -> {seg.end:.2f}] {seg.text}")
# print(f"Время транскрибации: {time.time()-start:.2f} сек")