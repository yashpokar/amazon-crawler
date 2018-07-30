def filter_price_in(self, values):
    for value in values:
        value = value.replace('\t', '').replace('\n', '').strip('from').strip()

        if value:
            yield value

def filter_price_out(self, values):
    return '${}'.format('.'.join(values)[2:])
