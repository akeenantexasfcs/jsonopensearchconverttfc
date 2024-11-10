#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import json
import uuid

def create_bulk_index_entries(text_content, document_id, index_name="textract-documents"):
    # Split text into lines
    lines = text_content.strip().split('\n')
    bulk_entries = []
    
    for i, line in enumerate(lines, 1):
        if line.strip():  # Skip empty lines
            # Create index action
            action = {
                "index": {
                    "_index": index_name
                }
            }
            
            # Create document
            doc = {
                "DocumentId": document_id,
                "BlockType": "LINE",
                "Id": str(i),
                "Text": line.strip(),
                "Confidence": 99.8,
                "Page": 1
            }
            
            # Add both action and document
            bulk_entries.append(json.dumps(action))
            bulk_entries.append(json.dumps(doc))
    
    return "\n".join(bulk_entries)

st.title("Text to OpenSearch Bulk Index Converter")

# Text input area
document_content = st.text_area("Paste your document content here:", height=300)
document_id = st.text_input("Enter Document ID:", value=f"doc_{uuid.uuid4().hex[:8]}")
index_name = st.text_input("Enter Index Name:", value="textract-documents")

if st.button("Convert to Bulk Index Format"):
    if document_content:
        bulk_index_content = create_bulk_index_entries(document_content, document_id, index_name)
        
        # Display the output
        st.text_area("Bulk Index Format (Copy this to OpenSearch):", bulk_index_content, height=300)
        
        # Download button
        st.download_button(
            label="Download as JSON",
            data=bulk_index_content,
            file_name=f"{document_id}_bulk_index.json",
            mime="application/json"
        )
    else:
        st.warning("Please enter some document content")

st.markdown("""
### How to use:
1. Paste your document content in the text area
2. (Optional) Customize the Document ID and Index Name
3. Click 'Convert to Bulk Index Format'
4. Copy the output or download the file
5. Paste the content into OpenSearch Dev Tools console
""")

