import streamlit as st
import pandas as pd
import json
import os
import glob
from datetime import datetime
import io
import zipfile
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Dashboard Aplikasi Visualisasi 2025 - Auto CSV Loader",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 50%, #4ECDC4 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 3rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .streamlit-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    
    .app-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 35px 90px rgba(0, 0, 0, 0.2);
    }
    
    .app-icon {
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: bold;
        color: white;
        margin-right: 1rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .streamlit { background: linear-gradient(135deg, #FF4B4B, #FF6B6B); }
    .machine-learning { background: linear-gradient(135deg, #4ECDC4, #44A08D); }
    .data-science { background: linear-gradient(135deg, #667eea, #764ba2); }
    .analytics { background: linear-gradient(135deg, #ffa726, #fb8c00); }
    .visualization { background: linear-gradient(135deg, #fa709a, #fee140); }
    .dashboard { background: linear-gradient(135deg, #a8edea, #fed6e3); }
    .python { background: linear-gradient(135deg, #3776ab, #ffd43b); }
    .web-app { background: linear-gradient(135deg, #61dafb, #21c7f7); }
    
    .csv-file-item {
        background: rgba(78, 205, 196, 0.1);
        border: 1px solid rgba(78, 205, 196, 0.3);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        gap: 1rem;
    }
    
    .stat-item {
        text-align: center;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        flex: 1;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        display: block;
    }
    
    .notification {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    
    .notification.success {
        background-color: #d4edda;
        border-color: #28a745;
        color: #155724;
    }
    
    .notification.error {
        background-color: #f8d7da;
        border-color: #dc3545;
        color: #721c24;
    }
    
    .notification.info {
        background-color: #d1ecf1;
        border-color: #17a2b8;
        color: #0c5460;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'apps_data' not in st.session_state:
        st.session_state.apps_data = [
            {
                "id": 1,
                "name": "QOE",
                "category": "Machine Learning",
                "description": "QOE Visualisasi Data Pengukuran Kualitas Layanan 2025",
                "url": "https://qoe-app-kendari.streamlit.app/",
                "icon": "Q",
                "color": "streamlit"
            },
            {
                "id": 2,
                "name": "Prima Aksi",
                "category": "Machine Learning",
                "description": "Visualisasi Target Prima Aksi 2025",
                "url": "https://prima-aksi.streamlit.app/",
                "icon": "P",
                "color": "machine-learning"
            }
        ]
    
    if 'detected_csv_files' not in st.session_state:
        st.session_state.detected_csv_files = []
    
    if 'notification' not in st.session_state:
        st.session_state.notification = None

# Auto-scan for CSV files
def scan_data_folder():
    """Scan for CSV files in the current directory and subdirectories"""
    csv_files = []
    
    # Look for CSV files in common locations
    search_patterns = [
        "*.csv",
        "Data/*.csv",
        "data/*.csv",
        "datasets/*.csv",
        "csv_files/*.csv"
    ]
    
    for pattern in search_patterns:
        for file_path in glob.glob(pattern):
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                file_size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
                
                csv_files.append({
                    'name': os.path.basename(file_path),
                    'path': file_path,
                    'size': file_size_str,
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
                })
    
    # Remove duplicates based on file name
    seen_names = set()
    unique_files = []
    for file in csv_files:
        if file['name'] not in seen_names:
            unique_files.append(file)
            seen_names.add(file['name'])
    
    return unique_files

# Load CSV file and extract app data
def load_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Load and parse CSV file for app data"""
    try:
        df = pd.read_csv(file_path)
        
        # Clean column names
        df.columns = df.columns.str.lower().str.strip()
        
        # Required columns
        required_cols = ['name', 'category', 'description', 'url', 'icon', 'color']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Missing columns in CSV: {', '.join(missing_cols)}")
            return []
        
        # Process each row
        apps = []
        for _, row in df.iterrows():
            # Skip rows with missing required data
            if pd.isna(row['name']) or pd.isna(row['category']) or pd.isna(row['description']):
                continue
            
            # Generate new ID
            max_id = max([app['id'] for app in st.session_state.apps_data], default=0)
            new_id = max_id + len(apps) + 1
            
            app = {
                'id': new_id,
                'name': str(row['name']).strip(),
                'category': str(row['category']).strip(),
                'description': str(row['description']).strip(),
                'url': str(row['url']).strip() if pd.notna(row['url']) else '#',
                'icon': str(row['icon']).strip()[:1].upper() if pd.notna(row['icon']) else '?',
                'color': str(row['color']).lower().strip() if pd.notna(row['color']) else 'streamlit'
            }
            
            # Check for duplicates
            if not any(existing['name'].lower() == app['name'].lower() 
                      for existing in st.session_state.apps_data + apps):
                apps.append(app)
        
        return apps
        
    except Exception as e:
        st.error(f"❌ Error loading CSV file: {str(e)}")
        return []

# Show notification
def show_notification(message: str, type: str = "info"):
    """Display a notification message"""
    st.session_state.notification = {"message": message, "type": type}

# Render notification
def render_notification():
    """Render notification if exists"""
    if st.session_state.notification:
        notif = st.session_state.notification
        if notif["type"] == "success":
            st.success(f"✅ {notif['message']}")
        elif notif["type"] == "error":
            st.error(f"❌ {notif['message']}")
        else:
            st.info(f"ℹ️ {notif['message']}")
        
        # Clear notification after displaying
        st.session_state.notification = None

# Render app card
def render_app_card(app: Dict[str, Any], col):
    """Render a single app card"""
    with col:
        with st.container():
            st.markdown(f"""
            <div class="app-card">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div class="app-icon {app['color']}">{app['icon']}</div>
                    <div>
                        <h3 style="margin: 0; color: #333;">{app['name']}</h3>
                        <span style="background: #f0f0f0; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; color: #666; font-weight: 600;">
                            {app['category']}
                        </span>
                    </div>
                </div>
                <p style="color: #555; line-height: 1.6; margin-bottom: 1.5rem;">{app['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                if st.button("✏️", key=f"edit_{app['id']}", help="Edit"):
                    st.session_state.editing_app = app
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{app['id']}", help="Delete"):
                    st.session_state.apps_data = [a for a in st.session_state.apps_data if a['id'] != app['id']]
                    show_notification(f"App '{app['name']}' deleted successfully", "success")
                    st.rerun()
            
            with col3:
                if st.button("📋", key=f"copy_{app['id']}", help="Copy URL"):
                    st.code(app['url'])
                    show_notification("URL copied to clipboard area", "info")
            
            with col4:
                if app['url'] != '#':
                    st.link_button("🚀 Buka App", app['url'], use_container_width=True)
                else:
                    st.button("🚀 Buka App", disabled=True, use_container_width=True)

# Main app
def main():
    load_css()
    init_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Dashboard Streamlit 2025</h1>
        <div class="streamlit-badge">Auto CSV Loader</div>
        <div class="streamlit-badge">Machine Learning Apps</div>
        <p style="font-size: 1.2rem; margin-top: 1rem;">Platform Terpadu dengan Auto-Upload CSV dari Folder Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render notifications
    render_notification()
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Control Panel")
        
        # Auto CSV Loader Section
        st.subheader("📁 Auto CSV Loader")
        
        if st.button("🔍 Scan Folder Data", use_container_width=True):
            with st.spinner("Scanning for CSV files..."):
                st.session_state.detected_csv_files = scan_data_folder()
                if st.session_state.detected_csv_files:
                    show_notification(f"Found {len(st.session_state.detected_csv_files)} CSV files", "success")
                else:
                    show_notification("No CSV files found", "info")
                st.rerun()
        
        # Display detected CSV files
        if st.session_state.detected_csv_files:
            st.write("**Detected CSV Files:**")
            for csv_file in st.session_state.detected_csv_files:
                with st.expander(f"📄 {csv_file['name']}", expanded=False):
                    st.write(f"**Size:** {csv_file['size']}")
                    st.write(f"**Modified:** {csv_file['last_modified']}")
                    st.write(f"**Path:** {csv_file['path']}")
                    
                    if st.button(f"📤 Load {csv_file['name']}", key=f"load_{csv_file['name']}"):
                        with st.spinner(f"Loading {csv_file['name']}..."):
                            new_apps = load_csv_file(csv_file['path'])
                            if new_apps:
                                st.session_state.apps_data.extend(new_apps)
                                show_notification(f"Successfully loaded {len(new_apps)} apps from {csv_file['name']}", "success")
                                st.rerun()
        
        st.divider()
        
        # Manual CSV Upload
        st.subheader("📤 Manual CSV Upload")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            with st.spinner("Processing uploaded CSV..."):
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Load apps from uploaded file
                new_apps = load_csv_file(temp_path)
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                if new_apps:
                    st.session_state.apps_data.extend(new_apps)
                    show_notification(f"Successfully loaded {len(new_apps)} apps from uploaded file", "success")
                    st.rerun()
        
        st.divider()
        
        # Export/Import Controls
        st.subheader("💾 Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export CSV", use_container_width=True):
                df = pd.DataFrame(st.session_state.apps_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download",
                    data=csv,
                    file_name=f"streamlit_apps_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.button("🔄 Reset Default", use_container_width=True):
                if st.button("⚠️ Confirm Reset", key="confirm_reset"):
                    st.session_state.apps_data = [
                        {
                            "id": 1,
                            "name": "QOE",
                            "category": "Machine Learning",
                            "description": "QOE Visualisasi Data Pengukuran Kualitas Layanan 2025",
                            "url": "https://qoe-app-kendari.streamlit.app/",
                            "icon": "Q",
                            "color": "streamlit"
                        },
                        {
                            "id": 2,
                            "name": "Prima Aksi",
                            "category": "Machine Learning",
                            "description": "Visualisasi Target Prima Aksi 2025",
                            "url": "https://prima-aksi.streamlit.app/",
                            "icon": "P",
                            "color": "machine-learning"
                        }
                    ]
                    show_notification("Dashboard reset to default", "success")
                    st.rerun()
    
    # Main content area
    # Search and filter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search applications...", placeholder="Enter app name, category, or description")
    
    with col2:
        if st.button("➕ Add New App", use_container_width=True):
            st.session_state.show_add_form = True
            st.rerun()
    
    # Statistics
    categories = list(set(app['category'] for app in st.session_state.apps_data))
    active_apps = sum(1 for app in st.session_state.apps_data if app['url'] != '#')
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-value">{len(st.session_state.apps_data)}</span>
            <span>Total Apps</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{len(categories)}</span>
            <span>Categories</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{active_apps}</span>
            <span>Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter apps based on search
    filtered_apps = st.session_state.apps_data
    if search_term:
        filtered_apps = [
            app for app in st.session_state.apps_data
            if search_term.lower() in app['name'].lower() or
               search_term.lower() in app['category'].lower() or
               search_term.lower() in app['description'].lower()
        ]
    
    # Display apps in grid
    if filtered_apps:
        # Create columns for grid layout
        cols_per_row = 2
        for i in range(0, len(filtered_apps), cols_per_row):
            cols = st.columns(cols_per_row)
            for j in range(cols_per_row):
                if i + j < len(filtered_apps):
                    render_app_card(filtered_apps[i + j], cols[j])
    else:
        st.info("🔍 No applications found matching your search criteria.")
    
    # Add/Edit form modal (using expander as modal alternative)
    if st.session_state.get('show_add_form', False) or st.session_state.get('editing_app', None):
        st.divider()
        
        editing_app = st.session_state.get('editing_app', None)
        title = "Edit Application" if editing_app else "Add New Application"
        
        with st.expander(f"📝 {title}", expanded=True):
            with st.form("app_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("App Name", 
                                       value=editing_app['name'] if editing_app else "",
                                       placeholder="e.g., QOE Dashboard")
                    
                    category = st.selectbox("Category", 
                                          options=["Machine Learning", "Data Science", "Analytics", 
                                                 "Visualization", "Dashboard", "Web App", "Python"],
                                          index=["Machine Learning", "Data Science", "Analytics", 
                                               "Visualization", "Dashboard", "Web App", "Python"].index(editing_app['category']) if editing_app else 0)
                    
                    icon = st.text_input("Icon (1 character)", 
                                       value=editing_app['icon'] if editing_app else "",
                                       max_chars=1,
                                       placeholder="Q")
                
                with col2:
                    url = st.text_input("Streamlit URL", 
                                      value=editing_app['url'] if editing_app else "",
                                      placeholder="https://your-app.streamlit.app/")
                    
                    color = st.selectbox("Color Theme",
                                       options=["streamlit", "machine-learning", "data-science", 
                                              "analytics", "visualization", "dashboard", 
                                              "python", "web-app"],
                                       index=["streamlit", "machine-learning", "data-science", 
                                            "analytics", "visualization", "dashboard", 
                                            "python", "web-app"].index(editing_app['color']) if editing_app else 0)
                
                description = st.text_area("Description", 
                                         value=editing_app['description'] if editing_app else "",
                                         placeholder="Detailed description of your Streamlit app...")
                
                col1, col2, col3 = st.columns([1, 1, 2])
                
                with col1:
                    if st.form_submit_button("💾 Save", use_container_width=True):
                        if name and category and description and icon:
                            if editing_app:
                                # Update existing app
                                for i, app in enumerate(st.session_state.apps_data):
                                    if app['id'] == editing_app['id']:
                                        st.session_state.apps_data[i].update({
                                            'name': name,
                                            'category': category,
                                            'description': description,
                                            'url': url or '#',
                                            'icon': icon.upper(),
                                            'color': color
                                        })
                                        break
                                show_notification(f"App '{name}' updated successfully", "success")
                                del st.session_state.editing_app
                            else:
                                # Add new app
                                max_id = max([app['id'] for app in st.session_state.apps_data], default=0)
                                new_app = {
                                    'id': max_id + 1,
                                    'name': name,
                                    'category': category,
                                    'description': description,
                                    'url': url or '#',
                                    'icon': icon.upper(),
                                    'color': color
                                }
                                st.session_state.apps_data.append(new_app)
                                show_notification(f"App '{name}' added successfully", "success")
                                st.session_state.show_add_form = False
                            
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields")
                
                with col2:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        if editing_app:
                            del st.session_state.editing_app
                        else:
                            st.session_state.show_add_form = False
                        st.rerun()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <small>Streamlit Auto-Loader v4.0 | 2025 Edition</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()