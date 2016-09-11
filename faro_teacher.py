import math
from PIL import Image

suites = ['Heart', 'Club', 'Diamond', 'Spade']
values = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King']


class Card:
    suit = None
    value = None
    
    image_dimensions = 71, 96
    image_pad = 2
    
    def __init__ (self, suit, value):
        self.suit = int(suit)
        self.value = int(value)
    
    def __str__ (self):
        return "%s of %ss (%s)" % (values[self.value], suites[self.suit], self.get_color())
    
    def get_color (self):
        return 'Black' if (self.suit % 2) else 'Red'
    
    def get_card_image (self):
        suit_translation = [2,0,3,1][self.suit]
    
        im = Image.open('cards.png')
        x = self.image_pad * (self.value + 1) + self.value * self.image_dimensions[0]
        y = 1 + self.image_pad * suit_translation + suit_translation * self.image_dimensions[1]
        return im.crop((
            x, 
            y, 
            x + self.image_dimensions[0], 
            y + self.image_dimensions[1]
        ))

def build_new_deck ():
    deck = []
    for i in range(0, 52):
        suit = math.floor(i/13)
        value = i % 13
        if i >= 26:
            value = 12 - value
            
        deck.append(Card(
            suit,
            value
        ))
    return deck
    
def faro_shuffle (deck):
    half_count = len(deck)/2
    left_cut = deck[:half_count]
    right_cut = deck[half_count:]
    new_deck = []
    for i in range(0, half_count):
        new_deck.append(right_cut[i])
        new_deck.append(left_cut[i])
    return new_deck

def longest_sequences (deck):
    max_suite_sequence = 0
    max_value_sequence = 0
    max_color_sequence = 0
    
    previous_suite = None
    previous_value = None
    previous_color = None
    current_value_direction = None # -1 descending, 0 duplicates, 1 ascending 
    
    current_suite_sequence = 0
    current_value_sequence = 0
    current_color_sequence = 0
    
    for card in deck:
        if card.suit != previous_suite:
            max_suite_sequence = max(max_suite_sequence, current_suite_sequence)
            current_suite_sequence = 0
            
        if card.value == previous_value:
            if current_value_direction != 0:
                max_value_sequence = max(max_value_sequence, current_value_sequence)
                current_value_direction = 0
                current_value_sequence = 1
        elif card.value - 1 == previous_value:
            if current_value_direction != 1:
                max_value_sequence = max(max_value_sequence, current_value_sequence)
                current_value_direction = 1
                current_value_sequence = 1
        elif card.value + 1 == previous_value:
            if current_value_direction != -1:
                max_value_sequence = max(max_value_sequence, current_value_sequence)
                current_value_direction = -1
                current_value_sequence = 1
        else:
            max_value_sequence = max(max_value_sequence, current_value_sequence)
            current_value_direction = None
            current_value_sequence = 0
        
        if card.get_color() != previous_color:
            max_color_sequence = max(max_color_sequence, current_color_sequence)
            current_color_sequence = 0
            
        current_suite_sequence += 1
        current_value_sequence += 1
        current_color_sequence += 1
        
        previous_suite = card.suit
        previous_value = card.value
        previous_color = card.get_color()
    
    max_suite_sequence = max(max_suite_sequence, current_suite_sequence)
    max_value_sequence = max(max_value_sequence, current_value_sequence)
    max_color_sequence = max(max_color_sequence, current_color_sequence)
    
    return max_suite_sequence, max_value_sequence, max_color_sequence

def print_deck (deck):
    for card in deck:
        print(card)
    
def save_deck_image (deck, name):
    til = Image.new("RGB",(834,95))
    x = 0
    for card in deck:
        til.paste(card.get_card_image(),(x,0))
        x += 15
    til.save("images/%s.png" % name)



deck = build_new_deck()
for i in range(0, 100):
    max_suite_sequence, max_value_sequence, max_color_sequence = longest_sequences(deck)
    save_deck_image(deck, '%s - %s, %s, %s' % (i, max_suite_sequence, max_value_sequence, max_color_sequence))
    deck = faro_shuffle(deck)
