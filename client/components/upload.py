import streamlit as st
import json
from utils.api import upload_pdfs_api

def render_uploader():
    st.sidebar.header("📄 Upload PDFs")
    uploaded_files = st.sidebar.file_uploader(
        "Upload multiple PDFs", 
        type="pdf", 
        accept_multiple_files=True,
        help="Select one or more PDF files to add to the knowledge base"
    )
    
    if uploaded_files:
        st.sidebar.info(f"📁 {len(uploaded_files)} file(s) selected")
        for file in uploaded_files:
            st.sidebar.write(f"• {file.name}")
    
    if st.sidebar.button("🚀 Upload to DB", disabled=not uploaded_files):
        if uploaded_files:
            with st.sidebar:
                # Show progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("📤 Uploading files...")
                    progress_bar.progress(25)
                    
                    response = upload_pdfs_api(uploaded_files)
                    progress_bar.progress(50)
                    
                    status_text.text("🔄 Processing documents...")
                    progress_bar.progress(75)
                    
                    if response.status_code == 200:
                        progress_bar.progress(100)
                        status_text.text("✅ Upload complete!")
                        
                        # Parse and display success message
                        try:
                            result = response.json()
                            st.success(f"✅ {result.get('message', 'Files uploaded successfully')}")
                            if 'files_processed' in result:
                                st.info(f"📋 Processed files: {', '.join(result['files_processed'])}")
                        except:
                            st.success("✅ Files uploaded and processed successfully!")
                    
                    elif response.status_code == 429:
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Handle rate limit errors specifically
                        try:
                            error_data = response.json()
                            st.error(f"⚠️ Rate Limit Exceeded")
                            st.warning(error_data.get('message', 'Rate limit exceeded'))
                            if 'suggestion' in error_data:
                                st.info(f"💡 Suggestion: {error_data['suggestion']}")
                        except:
                            st.error("⚠️ Rate limit exceeded. Please wait and try again.")
                    
                    elif response.status_code == 400:
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Handle validation errors
                        try:
                            error_data = response.json()
                            st.error(f"❌ Upload Error")
                            st.warning(error_data.get('error', 'Invalid files or request'))
                            if 'suggestion' in error_data:
                                st.info(f"💡 Suggestion: {error_data['suggestion']}")
                        except:
                            st.error("❌ Invalid files. Please check your PDFs and try again.")
                    
                    elif response.status_code == 401:
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Handle authentication errors
                        st.error("🔐 Authentication Error")
                        st.warning("There's an issue with the API configuration.")
                        st.info("💡 Please contact the administrator to check the API key setup.")
                    
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        
                        # Handle other errors
                        try:
                            error_data = response.json()
                            st.error(f"❌ Error: {error_data.get('error', 'Unknown error occurred')}")
                            if 'suggestion' in error_data:
                                st.info(f"💡 Suggestion: {error_data['suggestion']}")
                        except:
                            st.error(f"❌ Error: {response.text}")
                
                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Connection Error: {str(e)}")
                    st.info("💡 Please check if the server is running and try again.")
        else:
            st.sidebar.warning("⚠️ Please select files first")