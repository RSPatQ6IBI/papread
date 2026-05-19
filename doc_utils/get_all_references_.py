import re
def get_reference_list_from_paper(doc):
    print("\n🏁  >>>-------->>>>--------- GET_ALL_REFERENCES_.PY  --- <<< ----------<<<<  \n")
    ref_detail_json_arr_ = []
    print(f"📖 Starting extraction! Processing document with {len(doc)} pages... 🚀")
    reference_content_ = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b['type'] == 0:  # Text block
                for line in b["lines"]:
                    for span in line["spans"]:
                        if span["size"] > 10:
                            if span['text'] == 'References':
                                print(f"📄 Scanning Page Number: {page.number + 1}...") 
                                print(f"🎯 Found the exact 'References' section header! (Font Size: {span['size']})")
                                found=True
                            else:
                                found=False
                        if found:
                            # print(f"📌 Extracting reference text span: '{span['text']}'")
                            reference_content_.append(span['text'])

    print(f"\n📥 Text collection complete! Gathered {len(reference_content_)} target text fragments.")
    print("🧪 Beginning Regex parsing and reference grouping... 🔍")
    
    references_arr_ = []
    for content in reference_content_:
        matches = re.findall(r"\[(.*?)\]", content)
        if matches:
            # print(f"🔢 Match found! Detected reference index identifier: {matches[0]}")
            new_ref_ = ''
            references_ = {}
            references_['ref_no_'] = matches[0]
            references_arr_.append(references_)
        else:
            if len(references_arr_) > 0:
                # print(f"🧱 Appending continuing text to active reference: '{content[:30]}...'")
                new_ref_+= content
                references_arr_[-1]['ref_val_'] = new_ref_


                # references_arr_[-1]['ref_txt_']+= content

    # print(f"\n✨ Parsing completed successfully! Found {len(references_arr_)} distinct references.\n")
    for ref_ in references_arr_:
        # print('\n',10*'-->>','\n',ref_['ref_val_'])
        ref_json_ = {
            "ref_num" : ref_['ref_no_'],
            "ref_val" : ref_['ref_val_']
        }
        ref_detail_json_arr_.append(ref_json_)
    return ref_detail_json_arr_



if __name__ == "__main__":
    import sys, os
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    import get_information_from_pyproject as load_toml
    the_source_pdfs_ = os.listdir(load_toml.source_pdf_path)
    print('The pdf is --->>>>  ', the_source_pdfs_[0])  
    import fitz
    path_pdf_ = os.path.join(load_toml.source_pdf_path, the_source_pdfs_[0])
    doc = fitz.open(path_pdf_)
    print('Title of the document --- >> ',doc.metadata["title"])
    all_refs_json_ = get_reference_list_from_paper(doc=doc)
    print(all_refs_json_)