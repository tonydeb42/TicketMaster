"""
Upload Page - Employee Data CSV Upload
"""
import streamlit as st
from utils.api_client import api_client


def show_upload_page():
    """Display the CSV upload page"""
    
    # Page header
    st.markdown(
        """
        <div style='margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--text-primary);'>
                📤 Upload Employee Data
            </h1>
            <p style='font-size: 1.1rem; color: var(--text-secondary);'>
                Upload a CSV file containing employee information for batch processing
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Instructions card
    with st.container():
        st.markdown(
            """
            <div class='card' style='background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-left: 4px solid #667eea;'>
                <h3 style='margin-top: 0; color: #667eea;'>📋 CSV Format Requirements</h3>
                <p style='margin-bottom: 0.75rem; color: var(--text-secondary);'>Your CSV file should include the following columns:</p>
                <ul style='margin: 0; padding-left: 1.5rem; color: var(--text-secondary);'>
                    <li style='margin-bottom: 0.5rem;'><strong>Employee ID</strong> - Unique identifier for each employee</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Email</strong> - Employee email address</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Name</strong> - Full name of the employee</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Department</strong> - Department name</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Role/Title</strong> - Job role or title</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Primary Skills</strong> - Core competencies</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Secondary Skills</strong> - Additional skills</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Experience Years</strong> - Years of experience</li>
                    <li style='margin-bottom: 0.5rem;'><strong>Problem Domains Handled</strong> - Areas of expertise</li>
                </ul>
                <p style='margin-top: 1rem; margin-bottom: 0; font-size: 0.9rem; color: var(--text-secondary);'>
                    💡 <em>The system will use this data to intelligently assign tickets based on employee expertise and availability.</em>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Upload section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(
            """
            <div class='card'>
                <h3 style='margin-top: 0; color: var(--text-primary);'>Upload Your File</h3>
            """,
            unsafe_allow_html=True
        )
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with ticket information",
            label_visibility="collapsed",
            accept_multiple_files=False
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(
            """
            <div class='card' style='background: var(--hover-bg);'>
                <h4 style='margin-top: 0; font-size: 1.1rem; color: var(--text-primary);'>📊 Processing Info</h4>
                <p style='font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.75rem;'>
                    Upload time depends on file size
                </p>
                <div style='background: var(--card-bg); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.75rem; border: 1px solid var(--border-color);'>
                    <p style='margin: 0; font-size: 0.85rem; color: var(--text-secondary);'>
                        <strong>Small files:</strong> < 1 min
                    </p>
                </div>
                <div style='background: var(--card-bg); padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.75rem; border: 1px solid var(--border-color);'>
                    <p style='margin: 0; font-size: 0.85rem; color: var(--text-secondary);'>
                        <strong>Large files:</strong> 2-5 mins
                    </p>
                </div>
                <p style='font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0;'>
                    ✉️ Email notification on completion
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Upload button and processing
    if uploaded_file is not None:
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # File info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        
        with st.expander("📁 File Details", expanded=False):
            for key, value in file_details.items():
                st.markdown(f"**{key}:** {value}")
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process Upload", use_container_width=True, type="primary"):
                process_upload(uploaded_file)


def process_upload(uploaded_file):
    """Handle the file upload process"""
    
    # Validate file extension
    if not uploaded_file.name.lower().endswith('.csv'):
        st.error("❌ Invalid file format. Please upload a CSV file.")
        return
    
    # Show loading spinner
    with st.spinner("🔄 Uploading and processing your file..."):
        # Read file content
        file_content = uploaded_file.getvalue()
        
        # Make API request
        success, response_data, error_message = api_client.upload_csv(
            file_content,
            uploaded_file.name
        )
        
        if success:
            st.success(
                "✅ Upload successful! Processing started. You will receive an email once completed.",
                icon="✅"
            )
            
            if response_data:
                with st.expander("📊 Response Details", expanded=False):
                    st.json(response_data)
            
            st.balloons()
            
        else:
            st.error(f"❌ Upload failed: {error_message}", icon="❌")
            
            with st.expander("🔧 Troubleshooting Tips", expanded=True):
                st.markdown(
                    """
                    **Common issues:**
                    - Ensure the backend server is running
                    - Check that the CSV file format is correct
                    - Verify the file size is within limits
                    - Make sure the backend URL is correctly configured
                    
                    **Need help?** Contact support or check the documentation.
                    """
                )
