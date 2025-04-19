import os
import urllib.parse
import re

def load_url_list(file_path, convert_complex=False):
    entries = []
    if not os.path.exists(file_path):
        return entries

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if "|" not in line:
                continue
            filename, url = line.strip().split("|", 1)
            if convert_complex:
                encoded_url = urllib.parse.quote(url, safe='')
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
            # چاپ برای دیباگ
            print(f"🧪 {filename} ➜ {'[COMPLEX]' if convert_complex else '[SIMPLE]'} ➜ {url}")
            entries.append((filename, url))
    return entries

def replace_url_in_text(text, new_url):
    pattern = r'(url:\s*)([^\n]+)'
    return re.sub(pattern, rf'\1{new_url}', text, count=1)

def read_previous_urls(cache_file):
    previous = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            for line in f:
                if "|" not in line:
                    continue
                name, old_url = line.strip().split("|", 1)
                previous[name] = old_url
    return previous

def write_current_urls(cache_file, entries):
    with open(cache_file, "w", encoding="utf-8") as f:
        for name, url in entries:
            f.write(f"{name}|{url}\n")

def read_previous_mtime(mtime_file):
    try:
        with open(mtime_file, "r", encoding="utf-8") as f:
            return float(f.read().strip())
    except:
        return None

def write_current_mtime(mtime_file, mtime):
    with open(mtime_file, "w", encoding="utf-8") as f:
        f.write(str(mtime))

def main():
    url_file_simple = "Simple_URL_List.txt"
    url_file_complex = "Complex_URL_list.txt"
    template_file = "mihomo_template.txt"
    output_dir = "Sublist"
    cache_file = ".last_urls.txt"
    mtime_file = ".last_template_mtime"

    # آماده‌سازی پوشه خروجی
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # بارگذاری کش قبلی URLs
    previous_urls = read_previous_urls(cache_file)

    # بارگذاری کش قبلی mtime قالب
    previous_mtime = read_previous_mtime(mtime_file)
    current_mtime = os.path.getmtime(template_file)

    # تشخیص اینکه آیا قالب تغییر کرده
    template_changed = (previous_mtime is None) or (current_mtime != previous_mtime)
    if template_changed:
        print("🛠 قالب mihomo_template.txt تغییر کرده؛ بازسازی همه فایل‌ها")

    # بارگذاری لیست URL‌ها
    print("🔎 شروع بارگذاری لیست‌های URL...")
    entries = []
    entries += load_url_list(url_file_simple)
    entries += load_url_list(url_file_complex, convert_complex=True)

    # برای ذخیره کش جدید
    new_cache_entries = []
    changes_detected = False

    # بررسی هر URL برای تغییرات
    for filename, new_url in entries:
        old_url = previous_urls.get(filename)
        new_cache_entries.append((filename, new_url))

        # اگر URL تغییر کرده یا قالب تغییر کرده، بازسازی کن
        if template_changed or (new_url != old_url):
            changes_detected = True
            print(f"🛠 ساخت فایل جدید برای: {filename}")

            with open(template_file, "r", encoding="utf-8") as tf:
                original_text = tf.read()

            modified_text = replace_url_in_text(original_text, new_url)

            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as outf:
                outf.write(modified_text)

    # به‌روزرسانی کش‌ها
    write_current_urls(cache_file, new_cache_entries)
    write_current_mtime(mtime_file, current_mtime)

    if not changes_detected and not template_changed:
        print("✅ هیچ تغییری در URL‌ها یا قالب وجود نداشت.")

if __name__ == "__main__":
    main()
