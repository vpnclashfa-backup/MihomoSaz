import os
import yaml

url_file = 'Simple_URL_List.txt'
template_file = 'mihomo_template.txt'
output_dir = 'Sublist'
cache_file = '.last_urls.txt'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

previous = {}
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        for line in f:
            name, old_url = line.strip().split('|', 1)
            previous[name] = old_url

new_cache = []
changes_detected = False

with open(url_file, 'r') as f:
    lines = [line.strip() for line in f if '|' in line]

for line in lines:
    filename, new_url = line.split('|', 1)
    old_url = previous.get(filename)
    new_cache.append(f'{filename}|{new_url}')

    if new_url != old_url:
        changes_detected = True
        print(f'در حال ساخت فایل جدید برای: {filename}')

        with open(template_file, 'r', encoding='utf-8') as tf:
            data = yaml.safe_load(tf)

        if 'proxy-providers' not in data or 'proxy' not in data['proxy-providers']:
            raise Exception('ساختار proxy-providers یافت نشد!')

        data['proxy-providers']['proxy']['url'] = new_url

        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as outf:
            yaml.dump(data, outf, default_flow_style=False, allow_unicode=True)

with open(cache_file, 'w') as f:
    f.write('\n'.join(new_cache))

if not changes_detected:
    print('✅ تغییری در URLها وجود نداشت.')
