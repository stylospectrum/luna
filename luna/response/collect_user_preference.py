import random
from typing import Dict


def collect_user_preference(slot: Dict[str, str]):
    template = {
        '1': [
            'Our range of [type] encompasses a diverse array of styles and compositions. What specifically caught your eye?',
            'Let me assist you in discovering the ideal [type]. Do you have any particular preferences or specifications in mind?',
            'Explore our extensive assortment of [type]. Is there a specific characteristic you\'re searching for?',
            'We provide a broad variety of [type] to suit different tastes and needs. What are you hoping to find in your [type]?',
            'Discover the perfect [type] from our collection, featuring a range of designs and materials. What appeals to you the most?',
            'Looking for a [type]? I\'m here to guide you. Any specific details or features you\'d like to prioritize?',
            'Whether it\'s [type] for practicality or aesthetics, we have a diverse selection. What are your preferences for your [type]?',
            'Our inventory of [type] is designed to meet various requirements. What stands out to you in a [type]?',
            'Selecting the right [type] is crucial. Do you have any specific criteria or preferences for your [type]?',
            'We take pride in offering an extensive range of [type]. What attributes are you prioritizing in your search for the perfect [type]?'
        ],
        '2-pattern': [
            'Explore these stunning [type] featuring captivating [pattern] patterns. What color palette are you envisioning?',
            'Our bestselling [type] with intricate [pattern] patterns are a hit. Are you leaning towards a specific sleeve length?',
            'Let me introduce you to our exquisite [type] collection showcasing elegant [pattern] patterns. Any particular colors you fancy?',
            'I stumbled upon some fantastic [type] adorned with mesmerizing [pattern] patterns. What\'s your preferred choice of colors?',
            'Check out these marvelous [type] options, each boasting unique [pattern] patterns. Any specific sleeve length you prefer?',
            'Our [type] line, featuring eye-catching [pattern] patterns, is worth exploring. What color combinations catch your interest?',
            'I came across our popular [type] series with stylish [pattern] patterns. Do you have a particular sleeve length in mind?',
            'Delve into our diverse [type] assortment showcasing enchanting [pattern] patterns. Any specific colors you\'re drawn to?',
            'Discover the charm of our [type] collection adorned with vibrant [pattern] patterns. What color preferences do you have?',
            'Take a look at these fabulous [type] choices, each boasting unique [pattern] patterns. Do you have any specific color combinations in mind?',
        ],
        '2-sleeveLength': [
            'Our [type] comes in various sleeve lengths including [sleeveLength]. Any particular pattern you prefer?',
            'I can help you find the perfect [type] with [sleeveLength] sleeves. What color are you interested in?',
            'Explore our diverse selection of [type] with sleeve options, including [sleeveLength]. Do you have a preferred pattern?',
            'Looking for a stylish [type] with [sleeveLength] sleeves? Let me know your color preferences.',
            'Check out our [type] collection featuring options with different sleeve lengths, such as [sleeveLength]. Any specific patterns you like?',
            'Discover the versatility of our [type] offerings, available with various sleeve lengths including [sleeveLength]. What color palette appeals to you?',
            'Our curated selection of [type] includes styles with [sleeveLength] sleeves. Do you have a particular color in mind?',
            'I found some fantastic [type] with [sleeveLength] sleeves. What color palette are you thinking of?',
            'In our [type] range, you\'ll find options with [sleeveLength] sleeves. Any preferences for patterns or colors?',
            'Let me show you our latest [type] arrivals, featuring stylish options with [sleeveLength] sleeves. What color suits your taste?'
        ],
        '2-color': [
            'Interested in exploring [color] [type]? What specific patterns or sleeve lengths catch your eye?',
            'Our diverse [color] [type] collection awaits. Do you have a particular pattern in mind, or are you focused on sleeve lengths?',
            'Delve into our array of [type] in [color]. Any specific sleeve length preferences, or are you drawn to particular patterns?',
            'Considering options in [color] [type]? Tell us, are you more inclined towards specific patterns or particular sleeve lengths?',
            'Feel free to share your thoughts on [color] [type]. Are you leaning towards a certain pattern, or do you have preferences for sleeve lengths?',
            'With the impressive variety in our [color] [type] collection, any specific pattern preferences you\'d like to explore along with sleeve lengths?',
            'Exploring our [color] [type] offerings - do you have preferences for patterns, or are you more focused on finding the ideal sleeve length?',
            'Our extensive [color] [type] selection caters to various preferences. Are you interested in specific patterns or particular sleeve lengths?',
            'When it comes to [color] [type], the choices are diverse. Do you have a preference for sleeve lengths, or are patterns more on your mind?',
            'Embarking on the journey of [color] [type]. What are your thoughts on patterns and sleeve lengths for customization?'
        ],
        '3-pattern-sleeveLength': [
            'Check out our [type] with [pattern] patterns and [sleeveLength] sleeves. Any color preferences?',
            'We have a selection of [type] featuring [pattern] patterns and [sleeveLength] sleeves. What color would you like?',
            'We offer [type] with [pattern] patterns and [sleeveLength] sleeves. Do you have a preferred color?',
            'Explore our diverse range of [type] with stylish [pattern] patterns and comfortable [sleeveLength] sleeves. Any specific color in mind?',
            'Discover the elegance of our [type] options, showcasing beautiful [pattern] patterns and versatile [sleeveLength] sleeves. What color palette are you interested in?',
            'Looking for a trendy [type] with eye-catching [pattern] patterns and your preferred [sleeveLength] sleeves? Let me know your color preferences.',
            'Our collection includes [type] choices with unique [pattern] patterns and various [sleeveLength] sleeves. What color combinations are you considering?',
            'Consider our [type] offerings, designed with attention-grabbing [pattern] patterns and your desired [sleeveLength] sleeves. Any color preferences?',
            'In our selection of [type], you\'ll find options with distinctive [pattern] patterns and different [sleeveLength] sleeves. Do you have a preferred color?',
            'The [type] collection we have includes stylish options with [pattern] patterns and comfortable [sleeveLength] sleeves. What color are you thinking of?'
        ],
        '3-pattern-color': [
            'We have [type] in [color] with a [pattern] pattern. What sleeve length are you looking for?',
            'Our [type] in [color] with a [pattern] pattern comes in different sleeve lengths. Which one interests you?',
            'I can show you our [type] collection in [color] with [pattern] patterns. What about sleeve length?',
            'Explore our [color] [type] options with a stylish [pattern] pattern. Any specific sleeve length you prefer?',
            'Considering [color] [type] with a distinctive [pattern] pattern? Let me know your preference for sleeve length.',
            'Our [color] [type] collection features unique [pattern] patterns. What sleeve length are you interested in?',
            'Looking for [type] in [color] with an attractive [pattern] pattern? Share your preference for sleeve length.',
            'Discover the elegance of our [color] [type] with a beautiful [pattern] pattern. What sleeve length suits your style?',
            'In our [color] [type] lineup, you\'ll find options with eye-catching [pattern] patterns. Any specific sleeve length you have in mind?',
            'Explore the variety of our [color] [type] with [pattern] patterns. What sleeve length are you leaning towards?'
        ],
        '3-sleeveLength-color': [
            'We offer [type] with [sleeveLength] sleeves in [color]. Do you have a pattern preference?',
            'We have a range of [type] in [color] with [sleeveLength] sleeves. Any specific pattern in mind?',
            'I can help you find the perfect [type] in [color] with [sleeveLength] sleeves. Do you prefer a certain pattern?',
            'Discover our collection of [type] in [color] with [sleeveLength] sleeves. Which patterns would you like to see?',
            'Considering [sleeveLength] sleeves in [color] [type]? Let me know if you have any specific pattern preferences.',
            'Explore our [color] [type] options with [sleeveLength] sleeves. Are there particular patterns you\'re interested in?',
            'Looking for a [type] in [color] with [sleeveLength] sleeves? Share your thoughts on the preferred pattern.',
            'Our [color] [type] lineup includes options with [sleeveLength] sleeves. Do you have a specific pattern in mind?',
            'In our selection of [color] [type] with [sleeveLength] sleeves, we have various patterns. What are you leaning towards?',
            'Discover the versatility of our [color] [type] with [sleeveLength] sleeves. Any particular pattern you\'d like to explore?'
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
