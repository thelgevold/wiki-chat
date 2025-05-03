import wikipediaapi

def get_article(title):

    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent="MyApp/1.0 (https://mywebsite.com; contact@myemail.com)")

    page = wiki_wiki.page(title)

    if page.exists():
        return page.text[0:15000]
    else:
        raise ValueError(f"Article '{title}' does not exist.")

    
