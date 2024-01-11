import random


def answer_request_slots(request_slots: list[str], slot: dict[str, str], products: list[dict[str, str]]):
    template = {
        'availableSizes': [
            "We offer sizes ranging from [availableSizes_small] to [availableSizes_large] for this product.",
            "Sizes available include [availableSizes_list].",
            "You can choose from a variety of sizes: [availableSizes_list].",
            "This item is available in multiple sizes, from [availableSizes_small] to [availableSizes_large].",
            "We have this in sizes [availableSizes_list] currently in stock.",
            "Available sizes for this are [availableSizes_list].",
            "You can find this product in sizes ranging from [availableSizes_small] to [availableSizes_large].",
            "This comes in a wide range of sizes, from [availableSizes_small] to [availableSizes_large].",
            "Sizes [availableSizes_small] to [availableSizes_large] are currently available for this item.",
            "This product is offered in several sizes, including [availableSizes_list]."
        ],
        'brand': [
            "This product is by [brand], renowned for their quality.",
            "We carry the popular [brand] for this item.",
            "[brand], known for durability, makes this product.",
            "This is a premium item from the top [brand].",
            "Our featured brand for this is X, which specializes in this type of product.",
            "[brand], a leader in the field, offers this product.",
            "You'll find this item under the well-known [brand].",
            "This is from [brand], celebrated for their innovative designs.",
            "[brand], synonymous with excellence, produces this.",
            "Made by [brand], this item stands out for its exceptional quality.",
        ],
        'customerReview': [
            "Customers have rated this product [type] out of [customerReview] on average.",
            "This item generally receives positive reviews, with an average rating of [customerReview].",
            "Most customers have given this a rating of [customerReview] for its quality.",
            "It has received rave reviews, averaging [customerReview].",
            "The average customer review for this item is [customerReview].",
            "Users rate this highly, with most reviews around [customerReview].",
            "This product has an excellent customer satisfaction rating of [customerReview].",
            "With an average of [customerReview], customer feedback has been overwhelmingly positive.",
            "Customers love this product, giving it an average rating of [customerReview].",
            "It's a customer favorite, rated [customerReview] on average.",
        ],
        'size': [
            'To choose the right size, I recommend checking our size chart which provides detailed measurements. It will help you select the size that fits you best.'
        ],
        'price': [
            "The price of this item is set at $[price].",
            "This product is available for $[price].",
            "You can purchase this item for $[price].",
            "The cost of this product is $[price].",
            "This is priced at $[price].",
            "It is available at a price point of $[price].",
            "The selling price for this item is $[price].",
            "This comes at a price of $[price].",
            "For $[price], this product can be yours.",
            "This item is being offered at a price of $[price].",
        ],
        'availableSizes-brand': [
            "[brand] offers this product in sizes ranging from [availableSizes_small] to [availableSizes_large].",
            "For [brand]'s items, sizes available include [availableSizes_list].",
            "With [brand], you can find this in sizes [availableSizes_list].",
            "[brand] provides this in a variety of sizes, from [availableSizes_list].",
            "You can get this item from [brand] in sizes [availableSizes_list].",
            "Sizes [availableSizes_list] are available in the [brand] version of this product.",
            "[brand] has this product in sizes ranging from [availableSizes_list].",
            "This product by [brand] comes in sizes [availableSizes_list].",
            "In [brand], we offer this product in sizes [availableSizes_list].",
            "Sizes [availableSizes_list] for this item are offered by [brand].",
        ],
        'brand-customerReview': [
            "[brand]'s products, known for their quality, have an average customer review of [customerReview].",
            "Customers rate [brand]'s items highly, with an average review of [customerReview].",
            "[brand], receiving an average customer review of [customerReview], is known for its excellence.",
            "With an average review of [customerReview], [brand] stands out in customer satisfaction.",
            "[brand]'s products boast an average customer review score of [customerReview].",
            "Customers have consistently rated [brand]'s items with [customerReview] stars.",
            "[brand] has earned an average customer review of [customerReview] for its products.",
            "The average customer review for [brand] products is [customerReview].",
            "[brand]'s items are popular among customers, averaging [customerReview] in reviews.",
            "With customer reviews averaging [customerReview], [brand] maintains high standards.",
        ],
        'customerReview-price': [
            "This item, priced at $[price], has an average customer review of [customerReview].",
            "At $[price], this product has received a customer review average of [customerReview].",
            "With a price of $[price], it boasts a customer review average of [customerReview].",
            "Priced at $[price], this has an average review score of [customerReview] from customers.",
            "This product, with a review score of [customerReview], is available for $[price].",
            "For $[price], you get a product rated [customerReview] by customers.",
            "This, priced at $[price], has earned a review average of [customerReview].",
            "At the price point of $[price], it has garnered an average review of [customerReview].",
            "With an average review of [customerReview], this item is available at $[price].",
            "Customers rate this at [customerReview] stars, and it's priced at $[price].",
        ],
        'availableSizes-price': [
            "Sizes [availableSizes_list] for this item are priced at $[price].",
            "We offer this in sizes [availableSizes_list] at a price of $[price].",
            "This is available in sizes [availableSizes_list] for $[price].",
            "For $[price], you can find this product in sizes [availableSizes_list].",
            "This product, in sizes [availableSizes_list], comes at a price of $[price].",
            "Priced at $[price], sizes [availableSizes_list] are available.",
            "You can purchase this in sizes [availableSizes_list] for $[price].",
            "Sizes [availableSizes_list] of this item are available at $[price].",
            "This comes in a range of sizes from [availableSizes_list] at a cost of $[price].",
            "For a price of $[price], we offer this in sizes [availableSizes_list].",
        ]
    }

    response = ''

    if request_slots == ['availableSizes']:
        response = random.choice(template.get('availableSizes', []))
    elif request_slots == ['brand']:
        response = random.choice(template.get('brand', []))
    elif request_slots == ['customerReview']:
        response = random.choice(template.get('customerReview', []))
    elif request_slots == ['size']:
        response = random.choice(template.get('size', []))
    elif request_slots == ['price']:
        response = random.choice(template.get('price', []))
    elif 'availableSizes' in request_slots and 'brand' in request_slots:
        response = random.choice(template.get('availableSizes-brand', []))
    elif 'brand' in request_slots and 'customerReview' in request_slots:
        response = random.choice(template.get('brand-customerReview', []))
    elif 'customerReview' in request_slots and 'price' in request_slots:
        response = random.choice(template.get('customerReview-price', []))
    elif 'availableSizes' in request_slots and 'price' in request_slots:
        response = random.choice(template.get('availableSizes-price', []))
    else:
        response = 'Im sorry, I dont have information to answer your question.'

    for product in products:
        if all(value in product[key] for key, value in slot.items()):
            for request_slot in request_slots:
                response = response.replace(f'[{request_slot}]', str(product[request_slot]))
            break

    return response
