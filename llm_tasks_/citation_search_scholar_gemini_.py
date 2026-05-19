#@title DESIGN GEN-AI CLIENT AND TEST THE RESPONSE

import os
import re
import sys
import json
import time
import pathlib
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
# from the_document_class_ import source_document_details_
load_dotenv()
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL         = 'gemini-3-flash-preview'
MAX_ITER      = 4
REQUEST_DELAY = 1.0        # seconds between HTTP retries

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/pdf,*/*",
}

def sanitize_filename(name: str) -> str:
    """Turn a title into a safe filename."""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:100]

def get_and_validate_reference_links(the_doc_ob_):
    an_entry_ = the_doc_ob_.document_references_[0]
    citation = an_entry_['ref_val']
    print(10*'--==>>','\n',citation,'\n',10*'--==>>')
    import llm_tasks_.the_prompt_vault_ as prompt_vault
    system_prompt_search_paper_scholar_arxiv_= prompt_vault.prompt_dict_["system_prompt_search_paper_scholar_arxiv_"]
    client = genai.Client(api_key=GOOGLE_API_KEY)
    messages = [{"role": "user", "content": f"Find the PDF for this citation:\n\n{citation}"}]
    tools = [{"type": "web_search_20250305", "name": "web_search"}]
    print(f"\n🔍  Starting agent  (model: {MODEL}, max_iter: {MAX_ITER})")
    print("─" * 60)
    response = client.models.generate_content(
        model=MODEL,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt_search_paper_scholar_arxiv_,
            # tools=[some_defined_function_],
            # automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True), ## calling by default is disabled
            temperature=0,
            top_p=0.95,
            top_k=20,
        ),
        contents=messages[0]['content']
    )
    # print(response.text)
    # for bl_ in  response.candidates[0].content.parts:
    #     print(bl_.function_call)
    #     print(bl_.text)

    #     import json
    result = json.loads(response.text)
    a_key_ = the_doc_ob_.document_key_
    an_entry_['title'] = result.get('title')
    an_entry_['authors'] = result.get('authors')
    an_entry_['year'] = result.get('year')
    an_entry_['pdf_url'] = result.get('pdf_url')
    an_entry_['source'] = result.get('source')
    an_entry_['confidence'] = result.get('confidence')
    
    download_pdf_vault_ = "reference_pdf_download_repo_/"
    if not os.path.exists(download_pdf_vault_):
        os.makedirs(download_pdf_vault_)
    import doc_utils.download_pdf_from_link_ as download_pdf
    pdf_filename_ = a_key_+"_"+an_entry_['title']+"_Ref_"+an_entry_['ref_num']+'.pdf'
    download_pdf.download_pdf(url=an_entry_['pdf_url'], save_path=download_pdf_vault_+ pdf_filename_)
        


def display_citation_elements_and_pdf_url_(the_doc_ob_):
    the_doc_ob_ = the_doc_ob_.document_references_[0]
    print("\n" + "─" * 60)
    print("📋  Agent result:")
    print(f"    Title      : ", the_doc_ob_['title'])
    print(f"    Authors      : ", the_doc_ob_['authors'])
    print(f"    Title      : ", the_doc_ob_['pdf_url'])
    print("─" * 60)
    