def filter_price_in(self, values):
    for value in values:
        value = value.replace('\t', '').replace('\n', '').strip()

        if value:
            yield value
