import os
import random
from typing import List, Dict, Optional, Union, Tuple
from pathlib import Path

def pdf_to_photos(
    pdf_path: str,
    output_folder: Optional[str] = None,
    dpi: int = 150,
    effects_config: Optional[Dict] = None,
    multi_page: bool = True,
    format: str = "jpg",
    quality: int = 90
) -> List[str]:
    """
    Конвертирует PDF в набор фотографий с эффектами реалистичности.
    
    Args:
        pdf_path: Путь к PDF файлу
        output_folder: Папка для сохранения (по умолчанию рядом с PDF)
        dpi: Качество изображения (150-300)
        effects_config: Настройки эффектов (см. ниже)
        multi_page: True - каждая страница отдельно, False - только первая
        format: Формат вывода (jpg, png, webp)
        quality: Качество JPG (1-100)
    
    Returns:
        Список путей к созданным изображениям
        
    Пример effects_config:
        {
            'blur_radius': 0.7,
            'grain_intensity': 1.5,
            'vignette_strength': 15,
            'warm_tone': True,
            'paper_texture': 'textures/paper.jpg',
            'perspective_angle': 1.0,
            'shadow_effect': True,
            'border_radius': 10
        }
    """
    try:
        from pdf2image import convert_from_path
        from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageOps
        import numpy as np
    except ImportError as e:
        print("❌ Необходимо установить библиотеки:")
        print("   pip install pdf2image Pillow numpy")
        raise e
    
    # Создаем папку для вывода
    pdf_path = Path(pdf_path)
    if output_folder is None:
        output_folder = pdf_path.parent / f"{pdf_path.stem}_photos"
    else:
        output_folder = Path(output_folder)
    
    output_folder.mkdir(exist_ok=True, parents=True)
    
    # Настройки эффектов по умолчанию
    default_effects =  {
    'blur_radius': 1,           # Размытие для сглаживания
    'grain_intensity': 1.0,       # Зернистость
    'vignette_strength': 0,       # Виньетка ВЫКЛЮЧЕНА (важно!)
    'warm_tone': True,            # Тёплый оттенок
    'paper_texture': None,        # Без текстуры
    'perspective_angle': 5,       # Без поворота (если не нужен)
    'shadow_effect': False,       # Тень ВЫКЛЮЧЕНА (важно!)
    'border_radius': 0,           # Без закругления углов
    'brightness': 1.05,
    'contrast': 1.1,
    'color_temperature': 1.05
}
    
    if effects_config:
        default_effects.update(effects_config)
    effects = default_effects
    
    print(f"📄 Загружаем PDF: {pdf_path.name}")
    print(f"📁 Выходная папка: {output_folder}")
    print(f"🎛️  Настройки эффектов:")
    for key, value in effects.items():
        if value:
            print(f"   • {key}: {value}")
    
    # Конвертируем PDF в изображения
    try:
        poppler_path = r"C:\Program Files (x86)\Release-25.12.0-0\poppler-25.12.0\Library\bin"
        images = convert_from_path(
            str(pdf_path),
            dpi=dpi,
            fmt='png',  # Временный формат для качества
            thread_count=2,
            poppler_path=poppler_path
        )
    except Exception as e:
        print(f"❌ Ошибка при чтении PDF: {e}")
        print("   Убедитесь, что установлен poppler:")
        print("   Windows: скачайте с http://blog.alivate.com.au/poppler-windows/")
        print("   Linux: sudo apt-get install poppler-utils")
        print("   macOS: brew install poppler")
        raise e
    
    print(f"✅ PDF загружен: {len(images)} страниц")
    
    # Ограничиваем количество страниц если нужно
    if not multi_page and len(images) > 1:
        print(f"⚠️  Многостраничный PDF, но multi_page=False")
        print(f"   Будет обработана только первая страница")
        images = [images[0]]
    
    output_paths = []
    
    for i, img in enumerate(images):
        print(f"🔄 Обрабатываю страницу {i+1}/{len(images)}...")
        
        # Применяем эффекты
        processed_img = apply_effects(img, effects, page_num=i)
        
        # Сохраняем изображение
        page_suffix = f"_page_{i+1:02d}" if len(images) > 1 else ""
        output_filename = f"{pdf_path.stem}{page_suffix}.{format}"
        output_path = output_folder / output_filename
        
        save_options = {}
        if format.lower() == 'jpg':
            save_options['quality'] = quality
            save_options['optimize'] = True
        
        processed_img.save(str(output_path), **save_options)
        output_paths.append(str(output_path))
        
        print(f"   💾 Сохранено: {output_filename}")
    
    print(f"\n✅ Готово! Создано {len(output_paths)} изображений:")
    for path in output_paths:
        print(f"   📸 {Path(path).name}")
    
    return output_paths


def apply_effects(
    image,
    effects: Dict,
    page_num: int = 0
):
    """
    Применяет эффекты реалистичности к изображению.
    """
    from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageOps
    import numpy as np
    import random
    import math
    
    # Делаем копию для редактирования
    img = image.copy()
    
    # 1. Тёплый оттенок
    if effects['warm_tone']:
        # Создаем теплый фильтр (желтоватый оттенок)
        warm_filter = Image.new('RGB', img.size, (255, 240, 220))
        img = Image.blend(img, warm_filter, alpha=0.05)
    
    # 2. Добавляем зернистость (шум)
    if effects['grain_intensity'] > 0:
        # Создаем шумовое изображение
        width, height = img.size
        noise = np.random.normal(0, effects['grain_intensity'], (height, width, 3))
        noise = np.clip(noise, -20, 20).astype(np.uint8)
        noise_img = Image.fromarray(noise, mode='RGB')
        
        # Наложение шума с прозрачностью
        img = Image.blend(img, noise_img, alpha=0.1)
    
    # 3. Размытие для сглаживания шрифта
    if effects['blur_radius'] > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=effects['blur_radius']))
    
    # 4. Коррекция яркости и контраста
    if effects['brightness'] != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(effects['brightness'])
    
    if effects['contrast'] != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(effects['contrast'])
    
    # 5. Виньетирование (затемнение краёв)
    if effects['vignette_strength'] > 0:
        width, height = img.size
        vignette = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(vignette)
        
        # Рисуем эллиптический градиент
        for i in range(0, effects['vignette_strength'], 2):
            ellipse_box = [
                i, i,
                width - i, height - i
            ]
            alpha = int(255 * (1 - i / effects['vignette_strength']))
            draw.ellipse(ellipse_box, fill=alpha)
        
        # Применяем виньетирование
        vignette = vignette.filter(ImageFilter.GaussianBlur(radius=width*0.1))
        img.putalpha(255)  # Добавляем альфа-канал
        img.paste(vignette, (0, 0), vignette)
        img = img.convert('RGB')  # Убираем альфа-канал
    
    # 6. Легкий поворот для реалистичности
    if effects['perspective_angle'] > 0:
        # Случайный угол в пределах заданного
        angle = random.uniform(
            -effects['perspective_angle'], 
            effects['perspective_angle']
        )
        img = img.rotate(angle, expand=False, fillcolor=(240, 240, 240))
    
    # 7. Наложение текстуры бумаги (если есть)
    if effects['paper_texture']:
        try:
            texture = Image.open(effects['paper_texture']).convert('RGB')
            texture = texture.resize(img.size)
            # Наложение с прозрачностью
            img = Image.blend(img, texture, alpha=0.1)
        except Exception as e:
            print(f"⚠️ Не удалось загрузить текстуру: {e}")
    
    # 8. Эффект тени (создаем мягкую тень по краям)
    if effects['shadow_effect']:
        # Создаем изображение с тенью
        shadow_size = (img.width + 20, img.height + 20)
        shadow_img = Image.new('RGB', shadow_size, (240, 240, 240))
        
        # Добавляем тень
        shadow_offset = 8
        shadow_box = (
            shadow_offset,
            shadow_offset,
            img.width + shadow_offset,
            img.height + shadow_offset
        )
        
        # Создаем маску для размытой тени
        shadow_mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(shadow_mask)
        draw.rectangle([0, 0, img.width, img.height], fill=100)
        shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(10))
        
        # Рисуем тень
        shadow_color = Image.new('RGB', img.size, (100, 100, 100))
        shadow_img.paste(shadow_color, shadow_box[:2], shadow_mask)
        
        # Вставляем оригинальное изображение поверх тени
        shadow_img.paste(img, (0, 0))
        img = shadow_img
    
    # 9. Закругление углов
    if effects['border_radius'] > 0:
        radius = effects['border_radius']
        width, height = img.size
        
        # Создаем маску с закругленными углами
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # Рисуем прямоугольник с закругленными углами
        draw.rounded_rectangle(
            [0, 0, width, height],
            radius=radius,
            fill=255
        )
        
        # Применяем маску
        img.putalpha(mask)
        img = img.convert('RGB')
    
    return img


def batch_process_pdfs(
    input_folder: str,
    output_base: str,
    dpi: int = 150,
    effects_preset: str = "standard"
) -> Dict[str, List[str]]:
    """
    Пакетная обработка всех PDF в папке.
    
    Args:
        input_folder: Папка с PDF файлами
        output_base: Базовая папка для результатов
        dpi: Качество изображений
        effects_preset: Пресет эффектов ("minimal", "standard", "premium")
    
    Returns:
        Словарь {pdf_name: [список_изображений]}
    """
    input_path = Path(input_folder)
    output_base = Path(output_base)
    
    # Пресеты эффектов
    presets = {
        "minimal": {
            'blur_radius': 0,
            'grain_intensity': 1.0,
            'vignette_strength': 5,
            'warm_tone': False,
            'shadow_effect': False,
        },
        "standard": {
            'blur_radius': 0,
            'grain_intensity': 0.6,
            'vignette_strength': 12,
            'warm_tone': True,
            'shadow_effect': True,
            'border_radius': 8,
        },
        "premium": {
            'blur_radius': 0,
            'grain_intensity': 1.0,
            'vignette_strength': 20,
            'warm_tone': True,
            'shadow_effect': True,
            'border_radius': 12,
            'perspective_angle': 1.5,
            'paper_texture': 'textures/high_quality_paper.jpg'
        }
    }
    
    effects = presets.get(effects_preset, presets["standard"])
    
    results = {}
    pdf_files = list(input_path.glob("*.pdf"))
    
    print(f"🔍 Найдено {len(pdf_files)} PDF файлов в {input_folder}")
    
    for pdf_path in pdf_files:
        print(f"\n📄 Обрабатываю: {pdf_path.name}")
        
        # Создаем отдельную папку для каждого PDF
        output_folder = output_base / pdf_path.stem
        
        try:
            output_paths = pdf_to_photos(
                pdf_path=str(pdf_path),
                output_folder=str(output_folder),
                dpi=dpi,
                effects_config=effects,
                multi_page=True,
                format="jpg",
                quality=90
            )
            results[pdf_path.name] = output_paths
        except Exception as e:
            print(f"❌ Ошибка при обработке {pdf_path.name}: {e}")
            results[pdf_path.name] = []
    
    return results


def create_collage(
    image_paths: List[str],
    output_path: str,
    cols: int = 2,
    spacing: int = 20,
    background_color: Tuple[int, int, int] = (245, 245, 245)
):
    """
    Создает коллаж из нескольких изображений.
    """
    from PIL import Image
    
    images = [Image.open(path) for path in image_paths]
    
    if not images:
        return None
    
    # Определяем размеры коллажа
    rows = math.ceil(len(images) / cols)
    
    # Находим максимальные размеры ячеек
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Создаем холст
    collage_width = cols * max_width + (cols + 1) * spacing
    collage_height = rows * max_height + (rows + 1) * spacing
    
    collage = Image.new('RGB', (collage_width, collage_height), background_color)
    
    # Размещаем изображения
    for i, img in enumerate(images):
        row = i // cols
        col = i % cols
        
        x = col * max_width + (col + 1) * spacing
        y = row * max_height + (row + 1) * spacing
        
        # Центрируем изображение в ячейке
        x_offset = (max_width - img.width) // 2
        y_offset = (max_height - img.height) // 2
        
        collage.paste(img, (x + x_offset, y + y_offset))
    
    collage.save(output_path, quality=95)
    return output_path
