import genanki
import json
import os
from data_processing import ds_generator


def load_deck_metadata(model_dir):
    data_path = os.path.join(model_dir, 'base.json')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing base.json in {model_dir}")

    with open(data_path, 'r') as f:
        return json.load(f)


def load_html_template(model_dir, template_filename):
    template_path = os.path.join(model_dir, template_filename)
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Missing {template_filename} in {model_dir}")

    with open(template_path, 'r') as f:
        return f.read()


def load_optional_assets(model_dir):
    css_path = os.path.join(model_dir, 'styling.css')
    js_path = os.path.join(model_dir, 'scripts.js')

    assets = {}
    if os.path.exists(css_path):
        with open(css_path, 'r') as f:
            assets['css'] = f.read()
    if os.path.exists(js_path):
        with open(js_path, 'r') as f:
            assets['js'] = f.read()
    return assets


def get_templates(model_dir, config):
    templates = []
    for template_config in config['templates']:
        qfmt = load_html_template(model_dir, template_config['qfmt'])
        afmt = load_html_template(model_dir, template_config['afmt'])
        templates.append({
            'name': template_config['template_name'],
            'qfmt': qfmt,
            'afmt': afmt,
        })
    return templates


def create_anki_model(id, model_dir):
    config = load_deck_metadata(model_dir)
    templates = get_templates(model_dir, config)
    assets = load_optional_assets(model_dir)

    return genanki.Model(
        id,
        config['name'],
        fields=config['fields'],
        templates=templates,
        css=assets.get('css', '')
    )


base_model_idx = 2**30
simple_text = create_anki_model(base_model_idx, 'templates/simple_text')
simple_image = create_anki_model(base_model_idx+1, 'templates/simple_image')
simple_sound = create_anki_model(base_model_idx+2, 'templates/simple_sound')
labeled_image = create_anki_model(base_model_idx+3, 'templates/labeled_image')
labeled_image_rotated = create_anki_model(
    base_model_idx+4,
    'templates/labeled_rotated_image'
)


def create_minimal_qa():
    base_deck_idx = 2**30
    deck = genanki.Deck(base_deck_idx, 'Minimal Q&A Deck')
    media_path = 'resources/basics'

    questions = [
        {'model': simple_text, 'fields': [
            'What is the capital of France?', 'Paris'
        ]},
        {'model': simple_text, 'fields': [
            'What is your name?', 'Sir Lancelot of Camelot'
        ]},
        {'model': simple_image, 'fields': [
            'What animal is this?', 'Dog', '<img src="Bark.jpg">'
        ]},
        {'model': simple_sound, 'fields': [
            'Which animal is this?', 'Dog', '[sound:Bark.ogg]'
        ]},
    ]

    for q in questions:
        note = genanki.Note(
            model=q['model'],
            fields=q['fields']
        )
        deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = [f'{media_path}/Bark.jpg', f'{media_path}/Bark.ogg']
    package.write_to_file('Basic_QA_Deck.apkg')
    print("Created Basic_QA_Deck.apkg with media in subdirectories.")


def add_cards_from_generator(
        deck, model, source_dir, data_fp, titles_fp, media_files
        ):
    def format_region(r):
        return f"{r['title']}:{r['color']}"

    for item in ds_generator(source_dir, data_fp, titles_fp, quick=True):
        # Add media file path for the image
        source_image = item["source_image"]
        media_files.append(source_image)

        # Create the note with the specified model and fields
        note = genanki.Note(
            model=model,
            fields=[
                f'<img src="{os.path.basename(source_image)}">',
                ','.join(map(format_region, item['regions']))
            ]
        )
        deck.add_note(note)


def create_portugal_deck():
    source_dir = 'resources/portugal'
    dfp, tfp = 'portugal.json', 'portugal_en.json'
    base_deck_idx = 2**31
    deck = genanki.Deck(base_deck_idx, 'Portugal Deck')
    media_files = []

    # First pass: Add cards with labeled image model (standard)
    add_cards_from_generator(
        deck, labeled_image, source_dir, dfp, tfp, media_files
        )

    # Second pass: Add cards with labeled rotated image model
    add_cards_from_generator(
        deck, labeled_image_rotated, source_dir, dfp, tfp, media_files
        )

    # Package the deck
    package = genanki.Package(deck)
    package.media_files = media_files  # Assign the collected media files
    package.write_to_file('Portugal_Deck.apkg')
    print("Created Portugal_Deck.apkg with generated media files.")


if __name__ == '__main__':
    create_portugal_deck()
