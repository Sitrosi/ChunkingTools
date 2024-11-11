import json
import os


def file_exists(filename):
    return os.path.isfile(filename)


def get_item_data(resources_dir, item, titles, quick=False):
    image_file = f'{resources_dir}/{item.get("image")}'
    regions = []
    image_file_missing = False  # Flag to track if image is missing

    if not file_exists(image_file):
        image_file_missing = True
        if quick:
            print(f'[WARNING] Image file "{image_file}" does not exist')

    for region, color in item['regions'].items():
        title = titles.get(region, f'Unknown title for "{region}"')
        if title == f'Unknown title for "{region}"':
            if quick:
                print(f'[WARNING] Title for "{region}" not found')
        else:
            regions.append({
                'key': region,
                'title': title,
                'color': color
            })

    return {
        'source_image': image_file,
        'regions': regions,
        'image_file_missing': image_file_missing
    }


def load_json(filepath):
    """Load JSON data from a file."""
    if not file_exists(filepath):
        raise FileNotFoundError(f'File "{filepath}" does not exist')
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def ds_generator(resources_dir, data_fp, titles_fp, quick=False):
    region_titles = load_json(os.path.join(resources_dir, titles_fp))
    region_items = load_json(os.path.join(resources_dir, data_fp))

    for item in region_items:
        item_data = get_item_data(resources_dir, item, region_titles, quick)
        yield item_data


def check_images(resources_dir, json_images):
    png_files = {f for f in os.listdir(resources_dir) if f.endswith('.png')}
    missing_images = png_files - set(json_images)
    extra_images = set(json_images) - png_files

    if missing_images:
        for img in missing_images:
            print(f"[WARN] PNG file '{img}' in dir but not in JSON.")

    if extra_images:
        for img in extra_images:
            print(f"[INFO] '{img}' in JSON, but not in dir.")

    return not (missing_images or extra_images)


def main():
    source_dir = 'resources/portugal'
    data_fp, titles_fp = 'portugal.json', 'portugal_en.json'

    print("\n[INFO] Running quick verification...")
    json_images = []
    valid_images = True

    for item_data in ds_generator(source_dir, data_fp, titles_fp, quick=True):
        if item_data['image_file_missing']:
            valid_images = False
        json_images.append(os.path.basename(item_data['source_image']))

    if not check_images(source_dir, json_images):
        valid_images = False

    if not valid_images:
        print("\n[ERROR] Issues found - fix and re-run.")
        return

    print("\n[INFO] Validation passed. Proceeding with further processing...")
    for item_data in ds_generator(source_dir, data_fp, titles_fp, quick=False):
        print(f"[INFO] Processing image: {item_data['source_image']}")


if __name__ == "__main__":
    main()
