from typing import Dict, List
import wikipediaapi

def get_article(page_title: str, lang: str = 'en') -> List[Dict[str, str]]:
    wiki = wikipediaapi.Wikipedia(language='en', user_agent="MyApp/1.0 (https://mywebsite.com; contact@myemail.com)")
    page = wiki.page(page_title)

    if not page.exists():
        raise ValueError(f"Page '{page_title}' not found.")

    results = []

    def recurse_sections(sections, prefix=""):
        for section in sections:
            current_title = f"{prefix} -> {section.title}" if prefix else section.title
        
            results.append({
                "title": current_title,
                "text": section.text.strip()
            })
        
            recurse_sections(section.sections, current_title)

    recurse_sections(page.sections)
    return results
