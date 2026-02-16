"""
Ticket Creation Page - Single Ticket Submission
"""
import streamlit as st
from utils.api_client import api_client


def show_ticket_page():
    """Display the ticket creation page"""
    
    # Page header
    st.markdown(
        """
        <div style='margin-bottom: 2rem;'>
            <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--text-primary);'>
                ✍️ Create New Ticket
            </h1>
            <p style='font-size: 1.1rem; color: var(--text-secondary);'>
                Submit a single ticket with detailed description for intelligent routing
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Info banner
    st.markdown(
        """
        <div class='card' style='background: linear-gradient(135deg, #10b98115 0%, #34d39915 100%); border-left: 4px solid #10b981;'>
            <p style='margin: 0; color: #047857;'>
                <strong>💡 Pro Tip:</strong> Provide detailed descriptions for better department assignment accuracy.
                Our AI analyzes your ticket content to route it to the most appropriate team.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Main form
    with st.container():
        st.markdown(
            """
            <div class='card'>
                <h3 style='margin-top: 0; color: var(--text-primary);'>Ticket Information</h3>
            """,
            unsafe_allow_html=True
        )
        
        # Problem description
        st.markdown("#### 📝 Problem Description")
        query = st.text_area(
            "Describe your issue or query in detail",
            height=150,
            placeholder="Example: My laptop is overheating and shutting down randomly. It started yesterday after a Windows update. The CPU temperature reaches 95°C within minutes of startup...",
            help="Be as specific as possible. Include error messages, when the problem started, and what you've tried.",
            label_visibility="collapsed"
        )
        
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        
        # Department selection
        st.markdown("#### 🏢 Select Department")
        
        # Fetch departments from API
        departments = fetch_departments()
        
        if departments:
            selected_department = st.selectbox(
                "Choose the department for this ticket",
                options=departments,
                help="Select the most relevant department. Our AI can also help route this automatically.",
                label_visibility="collapsed"
            )
        else:
            st.warning("⚠️ Unable to load departments. Please try again or contact support.")
            selected_department = None
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_button = st.button(
            "🎫 Submit Ticket",
            use_container_width=True,
            type="primary",
            disabled=not query or not selected_department
        )
    
    # Handle form submission
    if submit_button:
        if not query or not query.strip():
            st.error("❌ Please provide a problem description.", icon="❌")
        elif not selected_department:
            st.error("❌ Please select a department.", icon="❌")
        else:
            submit_ticket(query.strip(), selected_department)
    
    # Validation hint
    if not query or not selected_department:
        st.markdown(
            """
            <div style='text-align: center; color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;'>
                <em>Fill in all required fields to submit your ticket</em>
            </div>
            """,
            unsafe_allow_html=True
        )


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_departments():
    """Fetch department list from API with caching"""
    
    with st.spinner("🔄 Loading departments..."):
        success, departments, error_message = api_client.get_departments()
        
        if success:
            return departments
        else:
            st.error(f"Failed to load departments: {error_message}", icon="❌")
            
            with st.expander("🔧 Troubleshooting", expanded=False):
                st.markdown(
                    f"""
                    **Error:** {error_message}
                    
                    **Possible solutions:**
                    - Check if the backend server is running
                    - Verify the backend URL: `{api_client.base_url}`
                    - Ensure the `/departments` endpoint is available
                    - Try refreshing the page
                    """
                )
            
            return None


def submit_ticket(query: str, department: str):
    """Submit ticket to backend API"""
    
    with st.spinner("🔄 Submitting your ticket..."):
        success, response_data, error_message = api_client.create_ticket(query, department)
        
        if success:
            st.success(
                "✅ Request raised successfully! You will receive an email with updates soon.",
                icon="✅"
            )
            
            if response_data:
                st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
                
                with st.expander("🎫 Ticket Details", expanded=True):
                    if isinstance(response_data, dict):
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'ticket_id' in response_data:
                                st.metric("Ticket ID", response_data['ticket_id'])
                            if 'status' in response_data:
                                st.metric("Status", response_data['status'])
                        with col2:
                            if 'department' in response_data:
                                st.metric("Department", response_data['department'])
                            if 'priority' in response_data:
                                st.metric("Priority", response_data['priority'])
                        
                        st.json(response_data)
                    else:
                        st.write(response_data)
            
            st.balloons()
            
            st.markdown(
                """
                <div style='text-align: center; margin-top: 2rem; padding: 1rem; background: var(--hover-bg); border-radius: 0.75rem; border: 1px solid var(--border-color);'>
                    <p style='margin: 0; color: var(--text-secondary);'>
                        Want to submit another ticket? Refresh the page or modify the form above.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        else:
            st.error(f"❌ Failed to create ticket: {error_message}", icon="❌")
            
            with st.expander("🔧 Troubleshooting", expanded=True):
                st.markdown(
                    f"""
                    **Error Details:** {error_message}
                    
                    **Common issues:**
                    - Backend server might be down
                    - Network connectivity issues
                    - Invalid request format
                    - Backend URL: `{api_client.base_url}/tickets`
                    
                    **What to try:**
                    1. Check your internet connection
                    2. Verify the backend is running
                    3. Try submitting again in a few moments
                    4. Contact support if the issue persists
                    
                    **Request Details:**
                    - Department: {department}
                    - Query length: {len(query)} characters
                    """
                )
