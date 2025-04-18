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
                url = f"https://url.v1.mk/sub?&url={encoded_url}&target=clash&config=https%3A%2F%2Fcdn.jsdelivr.net%2Fgh%2FSleepyHeeead%2Fsubconverter-config%40master%2Fremote-config%2Funiversal%2Furltest.ini&emoji=false&append_type=true&append_info=true&scv=true&udp=true&list=true&sort=false&fdn=true&insert=false"
            entries.append((filename, url))
    return entries

def replace_url_in_text(text, new_url):
    pattern = r'(url:\s*)([^\n]+)'
    return re.sub(pattern, rf'\1{new_url}', text, count=1)

def main():
    url_file_simple = "Simple_URL_List.txt"
    url_file_complex = "Complex_URL_list.txt"
    template_file = "mihomo_template.txt"
    output_dir = "Sublist"
    cache_file = ".last_urls.txt"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load previous cache
    previous = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            for line in f:
                name, old_url = line.strip().split("|", 1)
                previous[name] = old_url

    # Load new entries
    entries = []
    entries += load_url_list(url_file_simple)
    entries += load_url_list(url_file_complex, convert_complex=True)

    new_cache = []
    changes_detected = False

    for filename, new_url in entries:
        old_url = previous.get(filename)
        new_cache.append(f"{filename}|{new_url}")

        if new_url != old_url:
            changes_detected = True
            print(f"🛠 ساخت فایل جدید برای: {filename}")

            # Read template as text
            with open(template_file, "r", encoding="utf-8") as tf:
                original_text = tf.read()

            # Replace only the URL
            modified_text = replace_url_in_text(original_text, new_url)

            # Save new YAML file
            with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as outf:
                outf.write(modified_text)

    # Save updated cache
    with open(cache_file, "w", encoding="utf-8") as f:
        f.write("\n".join(new_cache))

    if not changes_detected:
        print("✅ هیچ تغییری در URLها وجود نداشت.")

if __name__ == "__main__":
    main()
