import os
import urllib.parse
import re
import logging
from typing import List, Tuple

# تنظیمات لاگ
logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class ListProcessor:
    def __init__(self):
        self.url_file_simple = "Simple_URL_List.txt"
        self.url_file_complex = "Complex_URL_list.txt"
        self.template_file = "mihomo_template.txt"
        self.output_dir = "Sublist"
        self.cache_file = ".last_urls.txt"
        self.mtime_file = ".last_template_mtime"

    def load_url_list(self, file_path: str, convert_complex: bool = False) -> List[Tuple[str, str]]:
        """بارگذاری لیست URL‌ها با مدیریت خطا"""
        entries = []
        if not os.path.exists(file_path):
            logging.error(f"فایل {file_path} یافت نشد!")
            return entries

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "|" not in line:
                    continue
                
                filename, url = line.split("|", 1)
                filename = filename.strip()
                url = url.strip()

                if convert_complex:
                    encoded_url = urllib.parse.quote(url, safe=':/?&=')
                    url = (
                        "https://url.v1.mk/sub?&url="
                        f"{encoded_url}&target=clash&config="
                        "https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2FSleepyHeeead"
                        "%2Fsubconverter-config%40master%2Fremote-config"
                        "%2Funiversal%2Furltest.ini&emoji=false"
                        "&append_type=true&append_info=true&scv=true"
                        "&udp=true&list=true&sort=false&fdn=true"
                        "&insert=false"
                    )

                logging.debug(f"بارگذاری: {filename} ➜ {'[COMPLEX]' if convert_complex else '[SIMPLE]'}")
                entries.append((filename, url))
        
        return entries

    def process_entries(self) -> None:
        """پردازش اصلی و مدیریت منطق برنامه"""
        # بررسی وجود فایل‌های ضروری
        self._check_required_files()

        # بارگذاری و ادغام لیست‌ها
        simple_entries = self.load_url_list(self.url_file_simple)
        complex_entries = self.load_url_list(self.url_file_complex, convert_complex=True)
        
        # مدیریت نام‌های تکراری با اولویت ساده
        seen = set()
        final_entries = []
        
        for name, url in simple_entries + complex_entries:
            if name in seen:
                logging.warning(f"نام تکراری '{name}' حذف شد!")
                continue
            seen.add(name)
            final_entries.append((name, url))

        # بررسی تغییرات قالب
        current_mtime = os.path.getmtime(self.template_file)
        previous_mtime = self._read_previous_mtime()
        template_changed = current_mtime != previous_mtime

        # تولید خروجی
        self._generate_outputs(final_entries, template_changed)
        self._update_cache(current_mtime)

    def _check_required_files(self) -> None:
        """بررسی وجود فایل‌های ضروری"""
        required_files = [
            self.url_file_simple,
            self.url_file_complex,
            self.template_file
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                error_msg = f"فایل ضروری '{file}' وجود ندارد!"
                logging.critical(error_msg)
                raise FileNotFoundError(error_msg)

    def _generate_outputs(self, entries: List[Tuple[str, str]], template_changed: bool) -> None:
        """تولید فایل‌های خروجی"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        with open(self.template_file, "r", encoding="utf-8") as f:
            template_content = f.read()

        changes_detected = False
        for filename, url in entries:
            output_path = os.path.join(self.output_dir, filename)
            
            # جایگزینی URL در قالب
            modified_content = re.sub(
                r'url:\s*.+',
                f'url: {url}',
                template_content,
                count=1
            )

            # ذخیره فایل در صورت نیاز
            if template_changed or not os.path.exists(output_path):
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(modified_content)
                changes_detected = True
                logging.info(f"فایل {filename} به‌روزرسانی شد")

        if not changes_detected:
            logging.info("هیچ تغییری شناسایی نشد")

    def _read_previous_mtime(self) -> float:
        """خواندن زمان آخرین تغییر قالب از کش"""
        try:
            with open(self.mtime_file, "r", encoding="utf-8") as f:
                return float(f.read().strip())
        except:
            return 0.0

    def _update_cache(self, mtime: float) -> None:
        """به‌روزرسانی اطلاعات کش"""
        with open(self.mtime_file, "w", encoding="utf-8") as f:
            f.write(str(mtime))

if __name__ == "__main__":
    try:
        processor = ListProcessor()
        processor.process_entries()
        logging.info("پردازش با موفقیت انجام شد")
    except Exception as e:
        logging.critical(f"خطای بحرانی: {str(e)}", exc_info=True)
        raise
