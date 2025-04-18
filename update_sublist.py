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
                if "|" in line:
                    name, old_url = line.strip().split("|", 1)
                    previous[name] = old_url

    # Load entries
    simple_entries = load_url_list(url_file_simple, convert_complex=False)
    complex_entries = load_url_list(url_file_complex, convert_complex=True)
    all_entries = simple_entries + complex_entries

    print("📥 URLهایی که باید پردازش شوند:")
    for filename, url in all_entries:
        print(f"  - {filename} | {url}")

    new_cache = []
    changes_detected = False

    for filename, new_url in all_entries:
        old_url = previous.get(filename)
        new_cache.append(f"{filename}|{new_url}")

        if new_url != old_url:
            changes_detected = True
            print(f"🛠 ساخت یا به‌روزرسانی فایل: {filename}")

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
