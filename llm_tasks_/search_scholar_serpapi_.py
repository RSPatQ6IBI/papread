
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import re
import json
load_dotenv()
THE_SERPAPI_KEY_ = os.getenv("SERPAPI_API_KEY")

def get_reference_list_from_paper(the_doc_ob_):
    print("\n🏁  >>>-------->>>>--------- SEARCH_SCHOLAR_SERPAPI_.PY  --- <<< ----------<<<<  \n")
    references_arr_ = the_doc_ob_.document_references_

    for ref_ in references_arr_:
        params = {
        "engine": "google_scholar",
        "q": ref_['ref_val'],
        "hl": "en",
        "api_key": THE_SERPAPI_KEY_
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        for paper in results.get("organic_results", []):
            print(f"Title: {paper['title']}")
            print(f"Link: {paper['link']}\n")
            ref_['paper_title_'] = paper['title']
            ref_['paper_link_serpapi_'] = paper['link']
    the_doc_ob_.document_references_ = references_arr_
# return references_arr_
