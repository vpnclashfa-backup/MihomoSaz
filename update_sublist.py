import os
import urllib.parse
import re

def load_url_list(file_path, convert_complex=False):
    entries = []
    if not os.path.exists(file_path):
        return entries

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            
            filename, url = line.split("|", 1)
            url = url.strip()
            
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
            
            entries.append((filename.strip(), url))
    
    print(f"\n✅ پردازش {len(entries)} آیتم از {file_path}")
    return entries

def replace_url_in_text(text, new_url):
    pattern = r'(url:[\s"\']*)([^\s"\']+)([\s"\']*)'
    return re.sub(pattern, rf'\g<1>{new_url}\g<3>', text, count=1, flags=re.MULTILINE)

def read_previous_urls(cache_file):
    previous = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "|" in line:
                    name, old_url = line.split("|", 1)
                    previous[name.strip()] = old_url.strip()
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

def generate_readme(output_dir, entries):
    readme_path = os.path.join(os.getcwd(), "README.md")
    
    # ... (همان محتوای قبلی generate_readme)

def process_entries(entries, previous, template_path, output_dir, cache_file):
    template_changed = check_template_changed(template_path)
    new_cache = []
    changes = False

    with open(template_path, "r", encoding="utf-8") as tf:
        template_content = tf.read()

    for filename, new_url in entries:
        old_url = previous.get(filename)
        new_cache.append((filename, new_url))

        if template_changed or (new_url != old_url):
            changes = True
            print(f"🔄 ایجاد فایل: {filename}")
            modified_content = replace_url_in_text(template_content, new_url)
            
            output_path = os.path.join(output_dir, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(modified_content)

    write_current_urls(cache_file, new_cache)
    return changes

def check_template_changed(template_file):
    mtime_file = ".last_template_mtime"
    previous_mtime = read_previous_mtime(mtime_file)
    current_mtime = os.path.getmtime(template_file)
    
    if previous_mtime != current_mtime:
        write_current_mtime(mtime_file, current_mtime)
        return True
    return False

def main():
    # تنظیمات اصلی
    config = {
        "simple_list": "Simple_URL_List.txt",
        "complex_list": "Complex_URL_list.txt",
        "template": "mihomo_template.txt",
        "output_dir": "Sublist",
        "simple_cache": ".cache_simple.txt",
        "complex_cache": ".cache_complex.txt"
    }

    # ایجاد پوشه خروجی
    os.makedirs(config["output_dir"], exist_ok=True)

    # پردازش لیست ساده
    print("\n🔨 شروع پردازش لیست ساده")
    simple_entries = load_url_list(config["simple_list"])
    simple_previous = read_previous_urls(config["simple_cache"])
    simple_changes = process_entries(
        entries=simple_entries,
        previous=simple_previous,
        template_path=config["template"],
        output_dir=config["output_dir"],
        cache_file=config["simple_cache"]
    )

    # پردازش لیست پیچیده
    print("\n🔨 شروع پردازش لیست پیچیده")
    complex_entries = load_url_list(config["complex_list"], convert_complex=True)
    complex_previous = read_previous_urls(config["complex_cache"])
    complex_changes = process_entries(
        entries=complex_entries,
        previous=complex_previous,
        template_path=config["template"],
        output_dir=config["output_dir"],
        cache_file=config["complex_cache"]
    )

    # تولید README
    all_entries = simple_entries + complex_entries
    generate_readme(config["output_dir"], all_entries)
    print("\n📖 README.md به روز شد")

    # نمایش خلاصه تغییرات
    print("\n✅ عملیات با موفقیت انجام شد!")
    print(f"تغییرات لیست ساده: {'✓' if simple_changes else '✗'}")
    print(f"تغییرات لیست پیچیده: {'✓' if complex_changes else '✗'}")

if __name__ == "__main__":
    main()
