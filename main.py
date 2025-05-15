import asyncio
import logging
from aiopath import AsyncPath
from aioshutil import copyfile

# Налаштування логування
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)

SOURCE_DIR = AsyncPath("source_folder")
OUTPUT_DIR = AsyncPath("output_folder")


async def copy_file(file_path: AsyncPath, target_root: AsyncPath):
    """Копіює файл у папку з назвою його розширення."""

    try:
        ext = file_path.suffix[1:] or "no_extension"
        target_dir = target_root / ext
        await target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_path.name

        await copyfile(file_path, target_path)
        logger.info(f"Скопійовано: {file_path} в {target_path}")
    except Exception as e:
        logger.error(f"Помилка при копіюванні {file_path}: {e}")


async def read_folder(source: AsyncPath, target: AsyncPath):
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
    if not await SOURCE_DIR.exists() or not await SOURCE_DIR.is_dir():
        logger.error(f"Папка {SOURCE_DIR} не існує або не є директорією")
        return

    await read_folder(SOURCE_DIR, OUTPUT_DIR)
    logger.info("Сортування завершено.")


if __name__ == "__main__":
    asyncio.run(main())
