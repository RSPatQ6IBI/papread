# import os, sys
# current_dir = os.path.dirname(os.path.realpath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
# print(" >>>_-->>>> ", parent_dir)
# import get_information_from_pyproject as load_toml
# from the_document_class_ import source_document_details_
# from doc_utils.get_citation_numbers_ import get_citation_num_per_page_ as cite_num
# from doc_utils.get_all_references_ import get_reference_list_from_paper
# from doc_utils.generate_now_key import generate_now_


import llm_tasks_.search_scholar_serpapi_ as search_scholar

import doc_utils.load_source_pdf_ as load_pdf
def init_doc_class_():
    print("🚀 Initializing the document class sequence...")
    import sys
    import os
    print("📦 System modules 'sys' and 'os' imported locally.")
    
    print("🔍 Importing 'source_document_details_' from 'the_document_class_'...")
    from the_document_class_ import source_document_details_
    
    print("💾 Mapping imported class reference to 'the_research_paper_'...")
    the_research_paper_ = source_document_details_(
        document_path=None, 
        document_pages = None,
        document_objects = None, 
        document_references_ = None,
        link_info_per_page_ = None,
        document_key_ = None
    )
    print("✅ Document class initialization complete.")
    return the_research_paper_

def print_paper_attributes_(the_research_paper_):
    print("📦 DOCUMENT KEYS ::---::---::-->>>  ", the_research_paper_.document_key_)
    print("📦 DOCUMENT PATH ::---::---::-->>>  ", the_research_paper_.document_path)
    print("📦 NET PAGES ::---::---::-->>> ", the_research_paper_.document_pages)
    print("📦 NET REFERENCES ::---::---::-->>> ", len(the_research_paper_.document_references_))
    print("📦 NET LINKS ::---::---::-->>> ", len(the_research_paper_.link_info_per_page_), '\n\n\n')

import pickle   
if __name__ == "__main__":
    print("\n🏁  >>>-------->>>>--------- THE_MAIN_FILE.PY  --- <<< ----------<<<<  \n")
    # # print("\n🏁 Starting script execution via main entrypoint...")
    # third_auth_obj_ = init_doc_class_()
    # load_pdf.get_source_attributes_for_doc(third_auth_obj_)
    # # print_paper_attributes_(third_auth_obj_)
    # search_scholar.get_reference_list_from_paper(the_doc_ob_=third_auth_obj_)
    # with open('data_object_pickles_/default_doc_pickle_ref_links_.pkl', 'wb') as file:
    #     pickle.dump(third_auth_obj_, file=file)

    with open('data_object_pickles_/default_doc_pickle_ref_links_.pkl', 'rb') as file:
        third_auth_obj_ = pickle.load(file)
    
    import llm_tasks_.citation_search_scholar_gemini_ as citation_search
    citation_search.get_and_validate_reference_links(the_doc_ob_=third_auth_obj_)
    citation_search.display_citation_elements_and_pdf_url_(the_doc_ob_=third_auth_obj_)
    
    print("\n\n 🏁 Script execution finished successfully.")
    # for each_ref_ in third_auth_obj_.document_references_:
    #     print(each_ref_)
    # print("\n🏁 THE_MAIN_FILE.PY  --- >>> \n")
