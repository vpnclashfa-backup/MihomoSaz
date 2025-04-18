import os
import urllib.parse
from ruamel.yaml import YAML

# فایل‌ها
simple_list = "Simple_URL_List.txt"
complex_list = "Complex_URL_List.txt"
template_file = "mihomo_template.txt"
output_dir = "Sublist"
cache_file = ".last_urls.txt"

yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

os.makedirs(output_dir, exist_ok=True)

# کش قبلی
previous = {}
if os.path.exists(cache_file):
    with open(cache_file, "r", encoding="utf-8") as f:
        for line in f:
            name, old_url = line.strip().split("|", 1)
            previous[name] = old_url

new_cache = []
changes_detected = False

# بارگذاری خطوط از فایل
def load_lines(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if "|" in line]
    return []

lines = load_lines(simple_list)

# پردازش فایل پیچیده‌تر
complex_lines = load_lines(complex_list)
for line in complex_lines:
    filename, original_url = line.split("|", 1)
    encoded_url = urllib.parse.quote(original_url, safe='')
    converted_url = (
        f"https://url.v1.mk/sub?&url={encoded_url}"
        f"&target=clash&config=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2FSleepyHeeead%2Fsubconverter-config%40master%2Fremote-config%2Funiversal%2Furltest.ini"
        f"&emoji=false&append_type=true&append_info=true&scv=true&udp=true&list=true&sort=false&fdn=true&insert=false"
    )
    lines.append(f"{filename}|{converted_url}")

# بررسی تغییرات
for line in lines:
    filename, new_url = line.split("|", 1)
    old_url = previous.get(filename)
    new_cache.append(f"{filename}|{new_url}")

    if new_url != old_url:
        changes_detected = True
        print(f"🔄 در حال ساخت فایل: {filename}")

        with open(template_file, "r", encoding="utf-8") as tf:
            data = yaml.load(tf)

        if "proxy-providers" not in data or "proxy" not in data["proxy-providers"]:
            raise Exception("❌ ساختار proxy-providers.proxy یافت نشد!")

        data["proxy-providers"]["proxy"]["url"] = new_url

        with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as outf:
            yaml.dump(data, outf)

# ذخیره کش جدید
with open(cache_file, "w", encoding="utf-8") as f:
    f.write("\n".join(new_cache))

if not changes_detected:
    print("✅ تغییری وجود نداشت.")
