import os 
import sys
from doc_utils.generate_now_key import generate_now_

class source_document_details_:
    def __init__(
        self, 
        document_path, 
        document_pages, 
        document_objects, 
        document_references_,
        link_info_per_page_,
        document_key_
    ):
        # Assigning attributes
        self.document_path = document_path
        self.document_pages = document_pages
        self.document_objects = document_objects
        self.document_references_ = document_references_
        self.link_info_per_page_ = link_info_per_page_
        self.document_key_ = document_key_
        

    def display_summary(self):
        """Prints a colorful summary of the document details."""
        print(f"\n📑 --- [Document Summary: {self.document_key_}] ---")
        print(f"📍 Location:  {self.document_path}")
        print(f"🔢 Page Count: {self.document_pages} pages")
        print(f"🎨 Elements:   {', '.join(self.document_objects) if self.document_objects else 'None'}")
        print(f"🔖 Refs:       {', '.join(self.document_references_) if self.document_references_ else 'None'}")
        print(f"🆔 Unique Key: {self.document_key_}")
        print("✅ End of Report\n")

