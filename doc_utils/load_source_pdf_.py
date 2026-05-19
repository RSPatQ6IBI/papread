import sys
import os
import fitz
# -------
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import get_information_from_pyproject as load_toml
from the_document_class_ import source_document_details_

from doc_utils.generate_now_key import generate_now_
from doc_utils.get_citation_numbers_ import get_citation_num_per_page_ as cite_num
from doc_utils.get_all_references_ import get_reference_list_from_paper

# ------- LOAD THE PDF IN SOURCE DIR

def get_source_attributes_for_doc(source_document_details_obj):
    print("\n🏁  >>>-------->>>>--------- LOAD_SOURCE_PDF_.PY  --- <<< ----------<<<<  \n")
    if source_document_details_obj.document_path is None:
        print(' ----- ... -----  GOING FOR THE DEFAULT DOC ----- ... ----- ')
        # source_pdf_path = load_toml.source_pdf_path
        the_source_pdfs_ = os.listdir(load_toml.source_pdf_path)
        source_document_details_obj.document_path = os.path.join(load_toml.source_pdf_path, the_source_pdfs_[0])
    paper_doc = fitz.open(source_document_details_obj.document_path)
    pdf_path_ = source_document_details_obj.document_path
    print('Path of the document --- >> ',pdf_path_)
    if paper_doc.metadata["title"]:
        print('Title of the document --- >> ',paper_doc.metadata["title"])
    all_refs_json_ = get_reference_list_from_paper(doc=paper_doc)
    link_info_arr_ = []
    the_info_json = {}
    for page in paper_doc:
        # print("\n\n",f" 📦 Page {page.number}","\n")
        links = page.get_links()
        link_count_ = 0
        for link in links:
            if link.get("uri"):
                pass
                # print(f"🔗 Link {link_count_}: {link.get('uri')}")
            else:
                link_count_ += 1
            # print(f" __ The page has {link_count_} references \n")
        citation_number_json_ = cite_num(page)
        the_info_json = {
            "page_no_" : page.number, 
            "link_count_" : link_count_, 
            "citation_number_" : citation_number_json_
        }
        link_info_arr_.append(the_info_json)
    the_time_index_ = generate_now_()
    
    source_document_details_obj.document_path=pdf_path_ 
    source_document_details_obj.document_pages=paper_doc.page_count 
    source_document_details_obj.document_references_ = all_refs_json_
    source_document_details_obj.link_info_per_page_ = link_info_arr_
    source_document_details_obj.document_key_ = the_time_index_
    

# if __name__ == "__main__":
#     print("\n🏁 THE_MAIN_FILE.PY  --- >>> \n")
#     print("\n🏁 Starting script execution via main entrypoint...")
#     third_auth_obj_ = source_document_details_(
#         document_path="", 
#         document_pages = "",
#         document_objects = "", 
#         document_references_ = "",
#         link_info_per_page_ = "",
#         document_key_ = ""
#     )
#     get_source_attributes_for_doc(third_auth_obj_)
#     print("🏁 Script execution finished successfully.")
#     print("\n🏁 THE_MAIN_FILE.PY  --- >>> \n")
    
