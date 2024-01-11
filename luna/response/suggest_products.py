def suggest_products(slot: dict[str, str], products: list[dict[str, str]], active='suggest'):
    suggested_product = []
    template_product_benefit = {
        'blouse': {
            'unique_feature/benefit': 'lightweight fabric, perfect for various shades and patterns.',
            'occasion/usage': 'ideal for office wear, casual meet-ups, or layering options.'
        },
        'jacket': {
            'unique_feature/benefit': 'durability and style, suitable for varied tones and styles.',
            'occasion/usage': 'great for outdoor activities, travel, and transitional weather.'
        },
        'shirt': {
            'unique_feature/benefit': 'versatile design, complements both patterned and solid options.',
            'occasion/usage': 'suitable for casual outings, formal events, or daily office wear.'
        },
        'dress': {
            'unique_feature/benefit': 'elegant and comfortable, highlighting hues and elegance.',
            'occasion/usage': 'perfect for special occasions, dinner dates, or stylish everyday wear.'
        },
        'tshirt': {
            'unique_feature/benefit': 'casual and trendy, showcasing vibrant colors and fun patterns.',
            'occasion/usage': 'ideal for relaxed weekends, gym sessions, or as a layering piece.'
        },
        'trousers': {
            'unique_feature/benefit': 'classic fit, tailored for sophistication in various colors and patterns.',
            'occasion/usage': 'appropriate for professional settings, evening events, or stylish casual wear.'
        },
        'sweater': {
            'unique_feature/benefit': 'cozy and chic, blends beautifully with different color palettes and textures.',
            'occasion/usage': 'best for chilly days, relaxed evenings, or as a comfortable work attire.'
        },
        'skirt': {
            'unique_feature/benefit': 'feminine flair, accentuates color vibrancy and pattern diversity.',
            'occasion/usage': 'suitable for social outings, artistic events, or office settings.'
        },
        'shoes': {
            'unique_feature/benefit': 'comfort meets style in every step with color and pattern versatility.',
            'occasion/usage': 'great for daily wear, long walks, or adding a touch of style to any outfit.'
        },
        'tank top': {
            'unique_feature/benefit': 'summer essential, highlights freshness and playfulness.',
            'occasion/usage': 'perfect for hot days, beach outings, or layering under jackets.'
        }
    }
    template_response = {
        '1': [
            'I recommend our [type] in [color] with a [pattern] design. The [sleeveLength] sleeves make it a great option for [occasion/usage], and it includes [unique_feature/benefit].'
        ],
        '2': [
            '1. For your preferences, consider our [type] in [color] with a [pattern] pattern and [sleeveLength] sleeves, [occasion/usage].',
            '2. Another great choice is the [color] [type] featuring a [pattern] design and [sleeveLength] sleeves, [unique_feature/benefit].'
        ],
        '3': [
            '1. [type] in [color] with a [pattern] pattern and [sleeveLength] sleeves, [occasion/usage].',
            '2. Our [color] [type] with a [pattern] design and [sleeveLength] sleeves, [unique_feature/benefit].',
            '3. Also, consider the [type] in [color] and [pattern], featuring [sleeveLength] sleeves, [unique_feature/benefit].'
        ],
        '4': [
            '1. First option is a [type] in [color] with [pattern] and [sleeveLength] sleeves, [occasion/usage].',
            '2. Try our [color] [type], which comes with a [pattern] design and [sleeveLength] sleeves, [unique_feature/benefit].',
            '3. Consider our [type] in [color] and [pattern], with [sleeveLength] sleeves, [unique_feature/benefit].',
            '4. Lastly, our [type] in [color], featuring a [pattern] pattern and [sleeveLength] sleeves, [occasion/usage].'
        ],
        '5': [
            '1. We have a [type] in [color] with a [pattern] pattern and [sleeveLength] sleeves, [occasion/usage].',
            '2. Try our [color] [type] with a [pattern] design and [sleeveLength] sleeves, [unique_feature/benefit].',
            '3. Check out the [type] in [color] and [pattern], featuring [sleeveLength] sleeves, [unique_feature/benefit].',
            '4. Our [color] [type], with a [pattern] pattern and [sleeveLength] sleeves, [occasion/usage].',
            '5. Finally, consider our [type] in [color] with [pattern] and [sleeveLength] sleeves, [unique_feature/benefit].'
        ]
    }
    user_ask_response = 'Based on your preferences for [color], [pattern], [sleeveLength], I recommend this product. It\'s [occasion/usage], offering both style and comfort.'

    for product in products:
        if all(value in product[key] for key, value in slot.items()):
            suggested_product.append(product)

    if len(suggested_product) == 0:
        return 'Sorry, we don\'t have any product that match your preferences.', suggested_product

    number_of_products = 5 if len(
        suggested_product) > 5 else len(suggested_product)
    number_of_products = number_of_products if active == 'suggest' else 1

    responses = template_response[str(number_of_products)] if active == 'suggest' else [
        user_ask_response]

    for idx, product in enumerate(suggested_product[:number_of_products]):
        if product['type'] in template_product_benefit:
            if 'unique_feature/benefit' in responses[idx]:
                responses[idx] = responses[idx].replace(
                    '[unique_feature/benefit]', template_product_benefit[product['type']]['unique_feature/benefit'])

            if 'occasion/usage' in responses[idx]:
                responses[idx] = responses[idx].replace(
                    '[occasion/usage]', template_product_benefit[product['type']]['occasion/usage'])

        for key, value in product.items():
            responses[idx] = responses[idx].replace(f'[{key}]', str(value))

    return '\n'.join(responses), suggested_product[:number_of_products]
