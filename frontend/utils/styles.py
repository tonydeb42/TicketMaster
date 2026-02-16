"""
Custom CSS styling for modern, polished UI with dark/light mode support
"""
import streamlit as st


def apply_custom_styles(dark_mode=False):
    """Apply custom CSS styles to the Streamlit app with theme support"""
    
    # Define color schemes
    if dark_mode:
        colors = {
            'primary': '#667eea',
            'primary_dark': '#5568d3',
            'secondary': '#764ba2',
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'background': '#1a1a1a',
            'card_bg': '#2d2d2d',
            'text_primary': '#e0e0e0',
            'text_secondary': '#a0a0a0',
            'border_color': '#404040',
            'sidebar_bg': 'linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%)',
            'hover_bg': '#3a3a3a',
            'input_bg': '#252525',
        }
    else:
        colors = {
            'primary': '#667eea',
            'primary_dark': '#5568d3',
            'secondary': '#764ba2',
            'success': '#10b981',
            'error': '#ef4444',
            'warning': '#f59e0b',
            'background': '#f8f9fa',
            'card_bg': '#ffffff',
            'text_primary': '#1a202c',
            'text_secondary': '#4a5568',
            'border_color': '#e2e8f0',
            'sidebar_bg': 'linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%)',
            'hover_bg': '#f8f9fa',
            'input_bg': '#ffffff',
        }
    
    st.markdown(
        f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        /* Global Styles */
        :root {{
            --primary-color: {colors['primary']};
            --primary-dark: {colors['primary_dark']};
            --secondary-color: {colors['secondary']};
            --success-color: {colors['success']};
            --error-color: {colors['error']};
            --warning-color: {colors['warning']};
            --background: {colors['background']};
            --card-bg: {colors['card_bg']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --border-color: {colors['border_color']};
            --hover-bg: {colors['hover_bg']};
            --input-bg: {colors['input_bg']};
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.03);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04);
            --shadow-xl: 0 20px 25px rgba(0,0,0,0.1), 0 10px 10px rgba(0,0,0,0.04);
            --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        /* Main container */
        .main {{
            background-color: var(--background);
            padding: 2rem 3rem;
        }}
        
        /* Typography */
        html, body, [class*="css"] {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }}
        
        p {{
            line-height: 1.7;
            color: var(--text-secondary);
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: {colors['sidebar_bg']};
            border-right: 1px solid var(--border-color);
        }}
        
        /* Buttons */
        .stButton > button {{
            background: var(--gradient-primary);
            color: white;
            border: none;
            border-radius: 0.75rem;
            padding: 0.875rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-md);
            letter-spacing: 0.01em;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            background: linear-gradient(135deg, #5568d3 0%, #6639a0 100%);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
            box-shadow: var(--shadow-sm);
        }}
        
        /* Secondary buttons */
        .stButton > button[kind="secondary"] {{
            background: var(--card-bg);
            color: var(--text-primary);
            border: 2px solid var(--border-color);
        }}
        
        .stButton > button[kind="secondary"]:hover {{
            background: var(--hover-bg);
            border-color: var(--primary-color);
        }}
        
        /* File Uploader */
        [data-testid="stFileUploader"] {{
            background-color: var(--card-bg);
            border: 2px dashed var(--border-color);
            border-radius: 1rem;
            padding: 2rem;
            transition: all 0.3s ease;
        }}
        
        [data-testid="stFileUploader"]:hover {{
            border-color: var(--primary-color);
            background-color: var(--hover-bg);
        }}
        
        /* Text Input & Text Area */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {{
            border-radius: 0.75rem;
            border: 2px solid var(--border-color);
            padding: 0.875rem 1.25rem;
            font-size: 1rem;
            transition: all 0.2s ease;
            background-color: var(--input-bg);
            color: var(--text-primary);
        }}
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            outline: none;
        }}
        
        /* Select Box */
        .stSelectbox > div > div {{
            border-radius: 0.75rem;
            border: 2px solid var(--border-color);
            background-color: var(--input-bg);
            transition: all 0.2s ease;
        }}
        
        .stSelectbox > div > div:hover {{
            border-color: var(--primary-color);
        }}
        
        /* Feature Cards */
        .feature-card {{
            background: var(--card-bg);
            border-radius: 1.25rem;
            padding: 2rem;
            box-shadow: var(--shadow-md);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid var(--border-color);
            height: 100%;
        }}
        
        .feature-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
            border-color: rgba(102, 126, 234, 0.3);
        }}
        
        .feature-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            display: inline-block;
        }}
        
        .feature-card h3 {{
            color: var(--text-primary);
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }}
        
        .feature-card p {{
            color: var(--text-secondary);
            line-height: 1.7;
            margin-bottom: 1.25rem;
        }}
        
        .feature-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        
        .feature-list li {{
            padding: 0.5rem 0;
            color: var(--text-secondary);
            position: relative;
            padding-left: 1.75rem;
        }}
        
        .feature-list li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: var(--success-color);
            font-weight: 700;
        }}
        
        /* Step Cards */
        .step-card {{
            background: var(--card-bg);
            border-radius: 1rem;
            padding: 1.75rem;
            text-align: center;
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }}
        
        .step-card:hover {{
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }}
        
        .step-number {{
            width: 3.5rem;
            height: 3.5rem;
            background: var(--gradient-primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0 auto 1rem;
            box-shadow: var(--shadow-md);
        }}
        
        .step-card h4 {{
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }}
        
        .step-card p {{
            font-size: 0.95rem;
            color: var(--text-secondary);
            margin: 0;
        }}
        
        /* Hero Section */
        .hero-section {{
            text-align: center;
            padding: 3rem 0;
            margin-bottom: 3rem;
        }}
        
        /* Card Container */
        .card {{
            background: var(--card-bg);
            border-radius: 1rem;
            padding: 2rem;
            box-shadow: var(--shadow-md);
            border: 1px solid var(--border-color);
            margin-bottom: 1.5rem;
        }}
        
        /* Success/Error Messages */
        .stSuccess, .stError, .stWarning, .stInfo {{
            border-radius: 0.75rem;
            padding: 1rem 1.25rem;
            border-left: 4px solid;
            box-shadow: var(--shadow-sm);
        }}
        
        /* Remove default Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebarNav"] {{display: none;}}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .main {{
                padding: 1rem;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            .feature-card, .card {{
                padding: 1.5rem;
            }}
            
            .hero-section {{
                padding: 2rem 0;
            }}
        }}
        
        /* Smooth transitions */
        * {{
            transition-property: background-color, border-color, color, fill, stroke, opacity, box-shadow, transform;
            transition-duration: 200ms;
            transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* Column gap enhancement */
        [data-testid="column"] {{
            padding: 0 0.75rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
