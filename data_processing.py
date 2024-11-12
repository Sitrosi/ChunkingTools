import os
from file_utils import file_exists, load_json


def get_item_data(resources_dir, item, titles, quick=False):
    """Process and retrieve data for a region item."""
    image_file = f'{resources_dir}/{item.get("image")}'
    regions = []
    image_file_missing = False

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


def ds_generator(resources_dir, data_fp, titles_fp, quick=False):
    """Generate region data using item and title JSON files."""
    region_titles = load_json(os.path.join(resources_dir, titles_fp))
    region_items = load_json(os.path.join(resources_dir, data_fp))

    for item in region_items:
        item_data = get_item_data(resources_dir, item, region_titles, quick)
        yield item_data
