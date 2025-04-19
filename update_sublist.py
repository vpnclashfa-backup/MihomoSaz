import os
import urllib.parse
import re
import logging
from typing import List, Tuple

logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class URLProcessor:
    def __init__(self):
        self.simple_list = "Simple_URL_List.txt"
        self.complex_list = "Complex_URL_list.txt"
        self.template_file = "mihomo_template.txt"
        self.output_dir = "Sublist"

    def _process_url(self, url: str, convert: bool) -> str:
        """تبدیل URL فقط برای لیست پیچیده"""
        if not convert:
            return url
        
        encoded_url = urllib.parse.quote(url, safe=':/?&=')
        return (
            "https://url.v1.mk/sub?&url="
            f"{encoded_url}&target=clash&config="
            "https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2FSleepyHeeead"
            "%2Fsubconverter-config%40master%2Fremote-config"
            "%2Funiversal%2Furltest.ini&emoji=false"
            "&append_type=true&append_info=true&scv=true"
            "&udp=true&list=true&sort=false&fdn=true"
            "&insert=false"
        )

    def _load_entries(self, file_path: str, convert: bool) -> List[Tuple[str, str]]:
        """بارگذاری لیست با مدیریت منحصر به فرد هر URL"""
        entries = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "|" not in line:
                        continue
                    filename, url = line.strip().split("|", 1)
                    processed_url = self._process_url(url.strip(), convert)
                    entries.append((filename.strip(), processed_url))
                    logging.debug(f"بارگذاری: {filename} ➜ {processed_url[:30]}...")
        except FileNotFoundError:
            logging.error(f"فایل {file_path} یافت نشد!")
        return entries

    def _generate_files(self, entries: List[Tuple[str, str]]) -> None:
        """تولید فایل‌های خروجی با URLهای منحصر به فرد"""
        with open(self.template_file, "r", encoding="utf-8") as f:
            template = f.read()

        for filename, url in entries:
            output_path = os.path.join(self.output_dir, filename)
            modified_content = re.sub(
                r'url:\s*.+', 
                f'url: {url}', 
                template
            )
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(modified_content)
            logging.info(f"فایل {filename} با URL منحصر به فرد ساخته شد")

    def run(self):
        """اجرای اصلی برنامه"""
        # ادغام لیست‌ها با اولویت ساده
        simple_entries = self._load_entries(self.simple_list, convert=False)
        complex_entries = self._load_entries(self.complex_list, convert=True)
        
        # جلوگیری از تکرار نام‌ها
        unique_entries = {}
        for name, url in simple_entries + complex_entries:
            if name not in unique_entries:
                unique_entries[name] = url

        # تولید خروجی
        os.makedirs(self.output_dir, exist_ok=True)
        self._generate_files(list(unique_entries.items()))

if __name__ == "__main__":
    try:
        processor = URLProcessor()
        processor.run()
        logging.info("✅ پردازش موفقیت‌آمیز بود!")
    except Exception as e:
        logging.critical(f"❌ خطای بحرانی: {str(e)}", exc_info=True)
