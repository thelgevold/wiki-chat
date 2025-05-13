import re

def capture_chapters(book_content):
   pattern = re.compile(
      r'Chapter\s+([IVXLCDM]+)\.\s*\n+'       # Chapter line with Roman numeral
      r'([^\n]+)\n+'                          # Title line
      r'([\s\S]+?)(?=\nChapter\s+[IVXLCDM]+\.|\Z)',  # Capture text until next chapter or end
      re.IGNORECASE)
   
   results = []

   for match in pattern.finditer(book_content):
      chapter, title, body_text = match.groups()
      results.append({
        'chapter': chapter.strip(),
        'title': title.strip(),
        'text': body_text.strip()
    })
      
   return results  

def trim_appendix(last_chapter):
   appendix_marker = "APPENDIX."
   if appendix_marker in last_chapter:
      print("Trimming appendix")
      return last_chapter.split(appendix_marker)[0].strip()
   
   return last_chapter

def get_book():
   with open(f"book.txt", "r", encoding="utf-8") as file:
      article_content = file.read()

      results = capture_chapters(article_content)      

      print(f"Number of chapters{len(results)}\n\n")  
      
      results[-1]["text"] = trim_appendix(results[-1]["text"])

      for item in results:
         print(f"{item["chapter"]} - {item["title"]} - {len(item["text"])}")

      return results
    

    
