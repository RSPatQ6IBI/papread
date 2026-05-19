import re
def get_citation_num_per_page_(page):
    # for page_index in range(len(doc)):
    #     page = doc[page_index]
    the_page_content_ = page.get_text()
    pattern = r'\[\s*\d+(?:\s*[-,\s]\s*\d+)*\s*\]'
    citations = re.findall(pattern, the_page_content_)
    the_citation_number_json_ = {
        "citation_number_details" : citations
    }
    return the_citation_number_json_
