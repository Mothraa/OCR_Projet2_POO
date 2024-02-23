

def book_title(page_parsed):
    """extract the title of a book"""
    title = page_parsed.find('div', {'class': 'col-sm-6 product_main'}).find('h1').contents[0]
    return title


