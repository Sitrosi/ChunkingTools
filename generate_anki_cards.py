import genanki
import json
import os


def load_deck_metadata(model_dir):
    data_path = os.path.join(model_dir, 'base.json')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing base.json in {model_dir}")

    with open(data_path, 'r') as f:
        return json.load(f)


def load_html_template(model_dir, template_filename):
    template_path = os.path.join(model_dir, f'{template_filename}')
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


def get_template(config, qfmt, afmt, assets):
    template = {
        'name': config['template_name'],
        'qfmt': qfmt,
        'afmt': afmt,
    }

    # Add optional CSS/JS if available
    if 'css' in assets:
        template['css'] = assets['css']
    if 'js' in assets:
        template['js'] = assets['js']

    return template


def get_templates(model_dir, config):
    assets = load_optional_assets(model_dir)
    templates = []

    for template_config in config['templates']:
        qfmt = load_html_template(model_dir, template_config['qfmt'])
        afmt = load_html_template(model_dir, template_config['afmt'])
        template = get_template(template_config, qfmt, afmt, assets)
        templates.append(template)

    return templates


def create_anki_model(id, model_dir):
    config = load_deck_metadata(model_dir)
    templates = get_templates(model_dir, config)
    return genanki.Model(
        id,
        config['name'],
        fields=config['fields'],
        templates=templates
    )


base_model_idx = 2**30
simple_text = create_anki_model(base_model_idx, 'templates/simple_text')
simple_image = create_anki_model(base_model_idx+1, 'templates/simple_image')
simple_sound = create_anki_model(base_model_idx+2, 'templates/simple_sound')


base_deck_idx = 2**30
deck = genanki.Deck(
    base_deck_idx,
    'Minimal Q&A Deck'
)

media_path = 'resources/basics'
questions = [
    {
        'model': simple_text,
        'fields': ['What is the capital of France?', 'Paris']
    },
    {
        'model': simple_text,
        'fields': ['What is your name?', 'My name is Sir Lancelot of Camelot']
    },
    {
        'model': simple_text,
        'fields': ['What is your quest?', 'To seek the Holy Grail']
    },
    {
        'model': simple_text,
        'fields': ['What is your favourite colour?', 'Blue']
    },
    {
        'model': simple_image,
        'fields': ['What animal is this?', 'Dog', '<img src="Bark.jpg">']
    },
    {
        'model': simple_sound,
        'fields': ['What animal makes this sound?', 'Dog', '[sound:Bark.ogg]']
    },
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
