"""
TicketMaster - Main Application
Production-grade Streamlit frontend with modern UI/UX
"""
import streamlit as st
import os
from datetime import datetime

from utils.styles import apply_custom_styles

# Page configuration
st.set_page_config(
    page_title="TicketMaster",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for theme
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply custom styling with theme
apply_custom_styles(st.session_state.dark_mode)

# Theme toggle in top-right corner
col1, col2 = st.columns([6, 1])
with col2:
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    if st.button(theme_icon, key="theme_toggle", help="Toggle dark/light mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Sidebar
with st.sidebar:
    # Project name at top
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h1 style='font-size: 2rem; font-weight: 800; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                🎫 TicketMaster
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Navigation menu - styled as buttons
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    if st.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_page == "Home" else "secondary"):
        st.session_state.current_page = "Home"
        st.rerun()
    
    if st.button("📤 Upload Employee Data", use_container_width=True, type="primary" if st.session_state.current_page == "Upload" else "secondary"):
        st.session_state.current_page = "Upload"
        st.rerun()
    
    if st.button("✍️ Create Ticket", use_container_width=True, type="primary" if st.session_state.current_page == "Create" else "secondary"):
        st.session_state.current_page = "Create"
        st.rerun()
    
    # Copyright at bottom
    st.markdown("<div style='flex-grow: 1;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    current_year = datetime.now().year
    st.markdown(
        f"""
        <div style='text-align: center; color: #666; font-size: 0.85rem;'>
            <p style='margin: 0;'>© {current_year} TicketMaster</p>
            <p style='font-size: 0.75rem; margin-top: 0.25rem;'>All rights reserved</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main content area based on current page
if st.session_state.current_page == "Home":
    st.markdown(
        """
        <div class='hero-section'>
            <h1 style='font-size: 3rem; font-weight: 700; margin-bottom: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                Welcome to TicketMaster
            </h1>
            <p style='font-size: 1.25rem; color: var(--text-secondary); margin-bottom: 2rem;'>
                Intelligent ticket assignment powered by machine learning
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Feature cards
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>📤</div>
                <h3>Upload Employee Data</h3>
                <p>Upload CSV files with employee information for batch processing. The system will automatically process and assign tickets based on employee expertise.</p>
                <ul class='feature-list'>
                    <li>CSV format support</li>
                    <li>Automatic processing</li>
                    <li>Bulk employee onboarding</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class='feature-card'>
                <div class='feature-icon'>✍️</div>
                <h3>Single Ticket</h3>
                <p>Create individual tickets with detailed descriptions. Get instant department assignment based on content.</p>
                <ul class='feature-list'>
                    <li>Real-time analysis</li>
                    <li>Smart routing</li>
                    <li>Status tracking</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    # Statistics or additional info
    st.markdown("### 📊 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class='step-card'>
                <div class='step-number'>1</div>
                <h4>Submit</h4>
                <p>Upload tickets via CSV or create individually</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class='step-card'>
                <div class='step-number'>2</div>
                <h4>Process</h4>
                <p>AI analyzes content and assigns departments</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class='step-card'>
                <div class='step-number'>3</div>
                <h4>Track</h4>
                <p>Receive email updates on ticket status</p>
            </div>
            """,
            unsafe_allow_html=True
        )

elif st.session_state.current_page == "Upload":
    from pages.upload import show_upload_page
    show_upload_page()

elif st.session_state.current_page == "Create":
    from pages.tickets import show_ticket_page
    show_ticket_page()
