import genanki

base_model_idx = 2**31
model_ids = {
    'simple_text': base_model_idx,
    'simple_image': base_model_idx + 1,
    'simple_sound': base_model_idx + 2,
}

text_model = genanki.Model(
    model_ids['simple_text'],
    'Basic Q&A',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'}
    ],
    templates=[
        {
            'name': 'Text Card',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        }
    ]
)

image_model = genanki.Model(
    model_ids['simple_image'],
    'Basic I&A',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Image'}
    ],
    templates=[
        {
            'name': 'Image Card',
            'qfmt': '{{Front}}<br>{{Image}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        }
    ]
)

sound_model = genanki.Model(
    model_ids['simple_sound'],
    'Basic S&A',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Sound'}
    ],
    templates=[
        {
            'name': 'Sound Card',
            'qfmt': '{{Front}}<br>{{Sound}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        },
    ],
)

base_deck_idx = 2**30
deck = genanki.Deck(
    base_deck_idx,
    'Minimal Q&A Deck'
)

media_path = 'resources/basics'
questions = [
    {
        'model': text_model,
        'fields': ['What is the capital of France?', 'Paris']
    },
    {
        'model': text_model,
        'fields': ['What is your name?', 'My name is Sir Lancelot of Camelot']
    },
    {
        'model': text_model,
        'fields': ['What is your quest?', 'To seek the Holy Grail']
    },
    {
        'model': text_model,
        'fields': ['What is your favourite colour?', 'Blue']
    },
    {
        'model': image_model,
        'fields': ['What animal is this?', 'Dog', '<img src="Bark.jpg">']
    },
    {
        'model': sound_model,
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
