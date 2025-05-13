import wikipediaapi

def get_article(title):
    # with open(f"{title}.txt", "r", encoding="utf-8") as f:
    #     content = f.read()
    #     return content

    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent="MyApp/1.0 (https://mywebsite.com; contact@myemail.com)")

    page = wiki_wiki.page(title)

    return get_flat_sections(page)

    # if page.exists():
    #     with open(f"{title}.txt", "w", encoding="utf-8") as f:
    #         f.write(page.text)
    #     return page.text
    # else:
    #     raise ValueError(f"Article '{title}' does not exist.")

def extract_flat_sections(section, level=0):
    combined_text = f"{section.title}\n{section.text}\n"
    for sub in section.sections:
        combined_text += extract_flat_sections(sub, level + 1)["combined_text"]
    
    return {
        "title": section.title,
        "text": section.text,
        "level": level,
        "combined_text": combined_text.strip()
    }

def get_flat_sections(page):
    return [extract_flat_sections(section) for section in page.sections]