import sys
import time
import os
import requests
import random
import string
import datetime
from pydub import AudioSegment
from moviepy.editor import AudioFileClip
from flask import Flask, request, jsonify
from gradio_client import Client
from pytubefix import YouTube
from pytubefix.cli import on_progress

app = Flask(__name__)
gradio_client = Client("http://127.0.0.1:7860/")

proxies = {
    "http": "http://USERNAME:PASSWORD@IP:PORT",
    "https": "http://USERNAME:PASSWORD@IP:PORT"
}

def print_colored_message(message):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\033[1;36m[{current_datetime}]\033[0m {message}")

def generate_unique_name():
    folder_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    file_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)) + '.mp3'
    return folder_name, file_name

@app.route('/generate_voice', methods=['POST'])
def generate_voice():
    try:
        input_base = 'ru-RU-SvetlanaNeural-Female'
        input_text = request.json['text']
        input_speaker = request.json['speaker']
        input_transpose = 0
        
        if input_speaker == "sandy":
            input_transpose = 12
            
        if input_speaker == "puff":
            input_transpose = 10
        
        print_colored_message("Озвучка диалога: [" + input_speaker + '] ' + input_text)
        
        result = gradio_client.predict(
            input_speaker,
            10,
            input_text,
            input_base,
            input_transpose,
            "pm",
            1,
            0.33,
            fn_index=0
        )

        audio_wav_path = result[2]

        return jsonify({'audio_wav_path': audio_wav_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_mashup', methods=['POST'])
def generate_mashup():
    print_colored_message("Новый запрос на генерацию мешапа")
    print_colored_message("Скачиваем аудио...")
    
    youtube_url = request.json['url']
    speaker_name = request.json['speaker']
    
    downloads_folder = "downloads"
    os.makedirs(downloads_folder, exist_ok=True)
    
    unique_folder_name, unique_audio_filename = generate_unique_name()
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    try:
        yt = YouTube(youtube_url,proxies=proxies,on_progress_callback = on_progress)
        video = yt.streams.filter(only_audio=True).first()
    except Exception as e:
        print_colored_message("Произошла ошибка при скачивании видео")
        print(e)
        return None
    
    unique_folder_path = os.path.join(script_directory, 'downloads', unique_folder_name)
    os.makedirs(unique_folder_path, exist_ok=True)
    print_colored_message("Скачали: " + unique_folder_path)
    
    out_file = video.download(output_path=unique_folder_path, filename=unique_audio_filename)

    audio = AudioSegment.from_file(out_file)
    audio = audio - 10
    audio.export(out_file, format="mp3")

    audio_vol = AudioFileClip(out_file)
    audio_length = audio_vol.duration
    if audio_length > 600:  # 600 сек = 10 мин
        print_colored_message("ОШИБКА! Аудио слишком длинное. Максимальная длина - 10 мин.")
        return None
    else:
        print_colored_message("Проверка на длину аудиофайла пройдена успешно")
    
    print_colored_message("Начинаем извлечение вокала и инструментала...")
    time.sleep(5)
    
    vocal_file_path = None
    max_extraction_attempts = 5
    extraction_attempt = 1
    
    while vocal_file_path is None and extraction_attempt <= max_extraction_attempts:
        print_colored_message(f"Попытка извлечения {extraction_attempt} из {max_extraction_attempts}")
        
        response = requests.post("http://localhost:7897/run/uvr_convert", json={
            "data": [
                "HP2_all_vocals",
                unique_folder_path,
                "opt",
                {"name": "zip.zip", "data": "data:@file/octet-stream;base64,UEsFBgAAAAAAAAAAAAAAAAAAAAAAAA=="},
                "opt",
                "10",
                "wav"
            ]
        }).json()
        
        if response.get('data') is not None:
            print(response)
            
            vocal_file_candidates = [f for f in os.listdir(os.path.join(script_directory, 'opt')) if f.startswith("vocal_") and unique_audio_filename in f]
            if len(vocal_file_candidates) == 1:
                vocal_file_path = os.path.join(script_directory, 'opt', vocal_file_candidates[0])
        else:
            print_colored_message("ОШИБКА! Не удалось разделить вокал и инструментал")
        
        time.sleep(3)
        
        extraction_attempt += 1
    
    print_colored_message("Вокал и инструментал были успешно разделены")
    time.sleep(1)
    
    print_colored_message("Выбираем оригинальный вокал: " + vocal_file_path)
    print_colored_message("Очищаем кеш RVC")
    
    response = requests.post("http://localhost:7897/run/infer_clean", json={
        "data": []
    }).json()
    
    if response.get('data') is None:
        print_colored_message("ОШИБКА! Не удалось очистить кеш RVC")
        return None
        
    print_colored_message("Кеш успешно очищен")
    print(response)
    
    print_colored_message("Выбираем голос: " + speaker_name)
    
    response = requests.post("http://localhost:7897/run/infer_set", json={
        "data": [
            speaker_name + ".pth",
            0.33,
            0.33
        ]
    }).json()
    
    if response.get('data') is None:
        print_colored_message("ОШИБКА! Не удалось выбрать голос")
        return None
    
    print_colored_message("Голос успешно выбран")
    print(response)
    
    print_colored_message("Запускаем переозвучку...")
    
    response = requests.post("http://localhost:7897/run/infer_convert", json={
        "data": [
            0,
            vocal_file_path,
            0,
            None,
            "pm",
            "",
            "logs/" + speaker_name + ".index",
            0.75,
            3,
            0,
            0.25,
            0.33,
        ]
    }).json()
    
    if response.get('data') is None:
        print_colored_message("ОШИБКА! Не удалось выполнить переозвучку")
        return None
    
    revoiced_vocal_file_path = response["data"][1]["name"]
    print_colored_message("Обновлённый вокал: " + revoiced_vocal_file_path)
    
    revoiced_vocal = AudioSegment.from_wav(revoiced_vocal_file_path)
    revoiced_vocal = revoiced_vocal + 2
    revoiced_vocal.export(revoiced_vocal_file_path, format="wav")
    
    instrumental_file_candidates = [f for f in os.listdir(os.path.join(script_directory, 'opt')) if f.startswith(f"instrument_{unique_audio_filename}")]
    
    if len(instrumental_file_candidates) == 0:
        return jsonify({'error': 'No matching instrumental file found.'}), 500
    elif len(instrumental_file_candidates) > 1:
        return jsonify({'error': 'Multiple matching instrumental files found.'}), 500
    
    instrumental_file_path = os.path.join(script_directory, 'opt', instrumental_file_candidates[0])
    print_colored_message("Инструментал: " + instrumental_file_path)
    original_instrumental = AudioSegment.from_wav(instrumental_file_path)
    
    min_length = min(len(revoiced_vocal), len(original_instrumental))
    revoiced_vocal = revoiced_vocal[:min_length]
    original_instrumental = original_instrumental[:min_length]
    print_colored_message("Объединяем новый вокал и инструментал...")
    
    combined_filename = f"combined_{unique_audio_filename}"
    combined_audio_path = os.path.join(script_directory, 'opt', f"{combined_filename}.wav")
    combined_audio = revoiced_vocal.overlay(original_instrumental)
    combined_audio.export(combined_audio_path, format="wav")
    print_colored_message("Объединение успешно завершено: " + combined_audio_path)
    print_colored_message("Удаляем обработанные файлы...")
    
    try:
        os.remove(instrumental_file_path)
        print_colored_message("Инструментал ... ОК")
    except OSError as e:
        print_colored_message(f"Инструментал ... Ошибка удаления файла")
        print(e)
        
    try:
        os.remove(vocal_file_path)
        print_colored_message("Оригинальный вокал ... ОК")
    except OSError as e:
        print_colored_message(f"Оригинальный вокал ... Ошибка удаления файла")
        print(e)
        
    try:
        os.remove(revoiced_vocal_file_path)
        print_colored_message("Обновленный вокал ... ОК")
    except OSError as e:
        print_colored_message(f"Обновленный вокал ... Ошибка удаления файла")
        print(e)
    
    print_colored_message("Генерация мешапа завершена успешно")
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    return jsonify({'audio_wav_path': combined_audio_path})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
