from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm import tqdm

def download_file(url, filename):
    try:
        # Получаем размер файла
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB

        progress_bar = tqdm(
            total=total_size,
            unit='iB',
            unit_scale=True,
            desc=filename,
            leave=True
        )

        with open(filename, "wb") as f:
            for data in response.iter_content(block_size):
                f.write(data)
                progress_bar.update(len(data))

        progress_bar.close()
        print(f"✅ {filename} успешно загружен.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при загрузке {filename}: {e}")

files = {
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf": "file1.pdf",
    "https://www.learningcontainer.com/wp-content/uploads/2020/04/sample-text-file.txt": "file2.txt",
    "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4": "file3.mp4"
    # "https://example.com/notfoundfile.zip": "file4.zip"  # пример несуществующего файла
}

with ThreadPoolExecutor(max_workers=3) as executor:
    for url, filename in files.items():
        executor.submit(download_file, url, filename)
