import genanki

base_model_idx = 2**31
model_ids = {
    'simple_text': base_model_idx
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

base_deck_idx = 2**30
deck = genanki.Deck(
    base_deck_idx,
    'Minimal Q&A Deck'
)

mp = 'resources/basics'
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
    }
]

for q in questions:
    note = genanki.Note(
        model=q['model'],
        fields=q['fields']
    )
    deck.add_note(note)

package = genanki.Package(deck)
package.write_to_file("Basic_QA_Deck.apkg")
