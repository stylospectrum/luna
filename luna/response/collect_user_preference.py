import random
from typing import Dict


def collect_user_preference(slot: Dict[str, str]):
    template = {
        '1': [
            'We have an exciting range of [type] available. Would you like to see our latest collection?',
            'Looking for [type]? We have a variety of styles that might interest you',
            'Our collection of [type] includes various designs and materials. What are you exactly looking for?',
            'I can help you find the perfect [type]. Do you have any specific requirements?',
            'We offer a wide selection of [type]. Are there any particular features you\'re interested in?'
        ],
        '2-pattern': [
            'I found some amazing [type] with [pattern] patterns. What color are you thinking of?',
            'Our [type] in [pattern] patterns are quite popular. Do you have a preferred sleeve length?',
            'Looking for [type] with a unique [pattern]? We have several options in different colors.'
            'We offer [type] with [pattern] patterns. Would you like to see our exclusive range?',
            'I can show you our [type] collection with [pattern] patterns. Do you have any color preferences?'
        ],
        '2-sleeveLength': [
            'We have some stylish [type] with [sleeveLength] sleeves. Would you like to explore different patterns?',
            'Looking for [type] with [sleeveLength] sleeves? We have a variety of options in various colors.',
            'Our [type] comes in various sleeve lengths including [sleeveLength]. Any particular pattern you prefer?',
            'I can help you find the perfect [type] with [sleeveLength] sleeves. What color are you interested in?',
            'We offer [type] in different [sleeveLength] sleeves. Would you like to check out different patterns?'
        ],
        '2-color': [
            'I see you\'re interested in [color] [type]. What about patterns or sleeve lengths?',
            'Our collection of [color] [type] is quite diverse. Are you looking for a specific pattern?',
            'We have a range of [type] in [color]. Do you have any preference for sleeve length?',
            'Looking for [type] in [color]? We can show you options with various patterns and sleeve lengths.',
            'Our [color] [type] are popular choices. Would you like to explore different patterns and sleeve lengths?'
        ],
        '3-pattern-sleeveLength': [
            'Check out our [type] with [pattern] patterns and [sleeveLength] sleeves. Any color preferences?',
            'We have a selection of [type] featuring [pattern] patterns and [sleeveLength] sleeves. What color would you like?',
            'Our [type] with [pattern] and [sleeveLength] sleeves are available in various colors. Interested in exploring?',
            'Looking for [type] with a [pattern] pattern and [sleeveLength] sleeves? Let\'s find the perfect color for you.',
            'We offer [type] with [pattern] patterns and [sleeveLength] sleeves. Do you have a preferred color?',
        ],
        '3-pattern-color': [
            'We have [type] in [color] with a [pattern] pattern. What sleeve length are you looking for?',
            'Looking for [type] with [pattern] patterns in [color]? We have various sleeve lengths available.',
            'Our [type] in [color] with a [pattern] pattern comes in different sleeve lengths. Which one interests you?',
            'I can show you our [type] collection in [color] with [pattern] patterns. What about sleeve length?',
            'We offer [type] with [pattern] patterns in [color]. Would you like to specify the sleeve length?',
        ],
        '3-sleeveLength-color': [
            'We offer [type] with [sleeveLength] sleeves in [color]. Do you have a pattern preference?',
            'Looking for [type] in [color] with [sleeveLength] sleeves? Let\'s explore patterns available.',
            'Our [type] with [sleeveLength] sleeves comes in a beautiful [color]. Interested in seeing more?',
            'We have a range of [type] in [color] with [sleeveLength] sleeves. Any specific pattern in mind?',
            'I can help you find the perfect [type] in [color] with [sleeveLength] sleeves. Do you prefer a certain pattern?',
            'Discover our collection of [type] in [color] with [sleeveLength] sleeves. Which patterns would you like to see?'
        ],
    }
    match str(len(slot)):
        case '1':
            return random.choice(template['1'])

        case '2':
            if 'pattern' in slot:
                return random.choice(template['2-pattern'])

            if 'sleeveLength' in slot:
                return random.choice(template['2-sleeveLength'])

            if 'color' in slot:
                return random.choice(template['2-color'])

        case '3':
            if 'pattern' in slot and 'sleeveLength' in slot:
                return random.choice(
                    template['3-pattern-sleeveLength'])

            if 'pattern' in slot and 'color' in slot:
                return random.choice(template['3-pattern-color'])

            if 'sleeveLength' in slot and 'color' in slot:
                return random.choice(template['3-sleeveLength-color'])
