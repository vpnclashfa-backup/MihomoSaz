import os
import re
import urllib.parse
import logging
from typing import List, Tuple

# تنظیمات لاگ
logging.basicConfig(
    filename="update.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class ConfigProcessor:
    def __init__(self):
        self.template_path = "mihomo_template.txt"
        self.output_dir = "Sublist"
        self.target_section = r'proxy-providers:\s*\n\s+proxy:\s*\n\s+type:\s*http\s*\n\s+url:\s*>?-?\s*\n\s+'

    def _replace_proxy_url(self, template: str, new_url: str) -> str:
        """جایگزینی دقیق URL در بخش proxy-providers با حفظ ساختار YAML"""
        pattern = re.compile(
            r'(proxy-providers:\s*\n\s+proxy:\s*\n\s+type:\s*http\s*\n\s+url:\s*>-?\s*\n\s+)([^\n]+)',
            re.DOTALL
        )
        return pattern.sub(rf'\g<1>{new_url}', template)

    def _process_url(self, url: str, is_complex: bool) -> str:
        """پردازش URL بر اساس نوع لیست"""
        if is_complex:
            encoded = urllib.parse.quote(url, safe=':/?&=')
            return (
                "https://url.v1.mk/sub?&url="
                f"{encoded}&target=clash&config="
                "https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2FSleepyHeeead"
                "%2Fsubconverter-config%40master%2Fremote-config"
                "%2Funiversal%2Furltest.ini&emoji=false"
                "&append_type=true&append_info=true&scv=true"
                "&udp=true&list=true&sort=false&fdn=true"
                "&insert=false"
            )
        return url

    def _load_entries(self, file_path: str, is_complex: bool) -> List[Tuple[str, str]]:
        """بارگذاری لیست URLها"""
        entries = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "|" not in line:
                        continue
                    filename, url = line.strip().split("|", 1)
                    processed_url = self._process_url(url.strip(), is_complex)
                    entries.append((filename.strip(), processed_url))
                    logging.debug(f"بارگذاری: {filename}")
        except FileNotFoundError:
            logging.error(f"فایل {file_path} یافت نشد!")
        return entries

    def generate_configs(self):
        """تولید فایل‌های پیکربندی"""
        # بارگذاری لیست‌ها
        simple_entries = self._load_entries("Simple_URL_List.txt", False)
        complex_entries = self._load_entries("Complex_URL_list.txt", True)
        
        # ادغام با اولویت ساده
        merged = {}
        for name, url in simple_entries + complex_entries:
            if name not in merged:
                merged[name] = url
                logging.info(f"ثبت: {name}")

        # خواندن تمپلیت اصلی
        with open(self.template_path, "r", encoding="utf-8") as f:
            original_template = f.read()

        # تولید فایل‌های خروجی
        os.makedirs(self.output_dir, exist_ok=True)
        
        for filename, url in merged.items():
            modified = self._replace_proxy_url(original_template, url)
            output_path = os.path.join(self.output_dir, filename)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(modified)
            
            logging.info(f"ساخته شد: {filename}")

if __name__ == "__main__":
    try:
        processor = ConfigProcessor()
        processor.generate_configs()
        logging.info("✅ پردازش با موفقیت انجام شد!")
    except Exception as e:
        logging.critical(f"❌ خطا: {str(e)}", exc_info=True)
