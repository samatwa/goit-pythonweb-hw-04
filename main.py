#!/usr/bin/env python3

import asyncio
import logging
import argparse
from aiopath import AsyncPath
from aioshutil import copyfile

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def copy_file(file_path: AsyncPath, target_root: AsyncPath) -> None:
    """Копіює файл у папку з назвою його розширення."""
    try:
        ext = file_path.suffix[1:] or "no_extension"
        target_dir = target_root / ext
        await target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_path.name

        await copyfile(file_path, target_path)
        logger.info(f"Скопійовано файл {file_path} у {target_path}")
    except Exception as e:
        logger.error(f"Помилка при копіюванні {file_path}: {e}")


async def read_folder(source: AsyncPath, target: AsyncPath) -> None:
    """Читає папку та копіює файли у папки з назвою їх розширення."""
    tasks = []
    async for item in source.iterdir():
        if await item.is_dir():
            tasks.append(read_folder(item, target))
        elif await item.is_file():
            tasks.append(copy_file(item, target))

    if tasks:
        await asyncio.gather(*tasks)


async def main():
    # Парсер аргументів командного рядка
    parser = argparse.ArgumentParser(
        description="Асинхронне сортування файлів за розширенням"
    )
    parser.add_argument("source", help="Шлях до вихідної папки")
    parser.add_argument("output", help="Шлях до цільової папки")
    args = parser.parse_args()

    # Ініціалізація асинхронних шляхів
    source_path = AsyncPath(args.source)
    output_path = AsyncPath(args.output)

    # Перевірки на існування
    if not await source_path.exists():
        logger.error(f"Папка {source_path} не існує")
        return

    # Перевірки на валідність
    if not await source_path.is_dir():
        logger.error(f"Папка {source_path} не є директорією")
        return

    # Створення цільової папки output_folder, якщо вона не існує
    if not await output_path.exists():
        await output_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Створено цільову директорію: {output_path}")

    logger.info(f"Починається сортування з {source_path} до {output_path}")
    await read_folder(source_path, output_path)
    logger.info("Сортування завершено успішно")


if __name__ == "__main__":
    asyncio.run(main())
