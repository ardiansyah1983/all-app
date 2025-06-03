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
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for mobile optimization with pure HTML buttons
def load_css():
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-top: 2rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
        
        .main-header h1 {
            font-size: 1.8rem !important;
            line-height: 1.2 !important;
        }
        
        .main-header p {
            font-size: 1rem !important;
        }
        
        .streamlit-badge {
            font-size: 0.8rem !important;
            padding: 0.3rem 0.8rem !important;
            margin: 0.2rem !important;
        }
        
        .app-card {
            padding: 1rem !important;
            margin-bottom: 1.5rem !important;
        }
        
        .app-icon {
            width: 40px !important;
            height: 40px !important;
            font-size: 18px !important;
            margin-right: 0.8rem !important;
        }
        
        .stats-container {
            flex-direction: column !important;
            gap: 0.5rem !important;
        }
        
        .stat-item {
            padding: 1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stat-value {
            font-size: 1.5rem !important;
        }
        
        .action-buttons-row {
            gap: 0.3rem !important;
        }
        
        .action-btn {
            padding: 0.4rem 0.6rem !important;
            font-size: 0.75rem !important;
        }
        
        .primary-btn {
            padding: 0.6rem !important;
            font-size: 0.8rem !important;
        }
    }
    
    /* Base styles */
    .main-header {
        text-align: center;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 50%, #4ECDC4 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .streamlit-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.3rem;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    
    .app-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .app-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.15);
    }
    
    .app-header {
        display: flex;
        align-items: flex-start;
        margin-bottom: 1rem;
        gap: 1rem;
    }
    
    .app-icon {
        width: 50px;
        height: 50px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        flex-shrink: 0;
    }
    
    .app-info {
        flex: 1;
        min-width: 0;
    }
    
    .app-title {
        margin: 0 0 0.3rem 0;
        color: #333;
        font-size: 1.3rem;
        font-weight: 600;
        line-height: 1.2;
    }
    
    .app-category {
        background: #f0f0f0;
        padding: 0.25rem 0.7rem;
        border-radius: 12px;
        font-size: 0.75rem;
        color: #666;
        font-weight: 600;
        display: inline-block;
    }
    
    .app-description {
        color: #555;
        line-height: 1.5;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .action-buttons-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        align-items: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
    }
    
    .action-btn {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
        color: #495057;
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        font-weight: 500;
        min-width: fit-content;
        outline: none;
        font-family: inherit;
    }
    
    .action-btn:hover {
        background: #e9ecef;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .edit-btn {
        background: linear-gradient(135deg, #17a2b8, #138496);
        color: white !important;
        border: none;
    }
    
    .edit-btn:hover {
        background: linear-gradient(135deg, #138496, #117a8b);
        color: white !important;
    }
    
    .delete-btn {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white !important;
        border: none;
    }
    
    .delete-btn:hover {
        background: linear-gradient(135deg, #c82333, #a71e2a);
        color: white !important;
    }
    
    .copy-btn {
        background: linear-gradient(135deg, #6c757d, #5a6268);
        color: white !important;
        border: none;
    }
    
    .copy-btn:hover {
        background: linear-gradient(135deg, #5a6268, #495057);
        color: white !important;
    }
    
    .primary-btn {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white !important;
        border: none;
        flex: 1;
        min-width: 120px;
        justify-content: center;
        font-weight: 600;
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
    }
    
    .primary-btn:hover {
        background: linear-gradient(135deg, #20c997, #17a2b8);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        color: white !important;
    }
    
    .primary-btn:disabled {
        background: #6c757d !important;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
        color: #999 !important;
    }
    
    .confirm-btn {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: #212529 !important;
        border: none;
        font-weight: 600;
    }
    
    .confirm-btn:hover {
        background: linear-gradient(135deg, #fd7e14, #dc3545);
        color: white !important;
    }
    
    /* Color classes */
    .streamlit { background: linear-gradient(135deg, #FF4B4B, #FF6B6B); }
    .machine-learning { background: linear-gradient(135deg, #4ECDC4, #44A08D); }
    .data-science { background: linear-gradient(135deg, #667eea, #764ba2); }
    .analytics { background: linear-gradient(135deg, #ffa726, #fb8c00); }
    .visualization { background: linear-gradient(135deg, #fa709a, #fee140); }
    .dashboard { background: linear-gradient(135deg, #a8edea, #fed6e3); }
    .python { background: linear-gradient(135deg, #3776ab, #ffd43b); }
    .web-app { background: linear-gradient(135deg, #61dafb, #21c7f7); }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1.5rem 0;
        gap: 0.8rem;
    }
    
    .stat-item {
        text-align: center;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        flex: 1;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        min-width: 80px;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .stat-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    .mobile-search-container {
        margin-bottom: 1rem;
    }
    
    .mobile-floating-add {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 32px rgba(255, 75, 75, 0.4);
        z-index: 1000;
        cursor: pointer;
        color: white;
        font-size: 24px;
        font-weight: bold;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .mobile-floating-add:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 40px rgba(255, 75, 75, 0.5);
    }
    
    /* Notification styles */
    .notification {
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 4px solid;
        font-size: 0.9rem;
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
    
    /* Form improvements */
    .stForm {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    
    /* Mobile table improvements */
    .dataframe {
        font-size: 0.8rem;
        overflow-x: auto;
    }
    
    /* Hide scrollbar for cleaner look */
    .main::-webkit-scrollbar {
        width: 4px;
    }
    
    .main::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    .main::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 2px;
    }
    
    /* Loading spinner improvements */
    .stSpinner {
        text-align: center;
    }
    
    /* Confirmation dialog styles */
    .confirm-delete {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        color: #856404;
    }
    
    /* URL display styles */
    .url-display {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-family: monospace;
        font-size: 0.8rem;
        word-break: break-all;
        color: #495057;
    }
    </style>
    
    <script>
    function editApp(appId) {
        // Trigger Streamlit rerun with edit action
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'edit', appId: appId}
        }, '*');
    }
    
    function deleteApp(appId) {
        // Trigger Streamlit rerun with delete action
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'delete', appId: appId}
        }, '*');
    }
    
    function confirmDelete(appId) {
        // Trigger Streamlit rerun with confirm delete action
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'confirm_delete', appId: appId}
        }, '*');
    }
    
    function copyUrl(url) {
        // Copy URL to clipboard and show notification
        navigator.clipboard.writeText(url).then(function() {
            // Show temporary notification
            const notification = document.createElement('div');
            notification.className = 'notification info';
            notification.innerHTML = '✅ URL copied to clipboard!';
            document.body.appendChild(notification);
            
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 3000);
        }).catch(function() {
            // Fallback: show URL in a text area for manual copy
            const urlDisplay = document.createElement('div');
            urlDisplay.className = 'url-display';
            urlDisplay.innerHTML = `URL: ${url}`;
            event.target.parentNode.appendChild(urlDisplay);
            
            setTimeout(() => {
                if (urlDisplay.parentNode) {
                    urlDisplay.parentNode.removeChild(urlDisplay);
                }
            }, 5000);
        });
    }
    </script>
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
    
    if 'confirm_delete' not in st.session_state:
        st.session_state.confirm_delete = None
    
    if 'action_clicked' not in st.session_state:
        st.session_state.action_clicked = None

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

# Pure HTML app card with integrated buttons
def render_app_card_pure_html(app: Dict[str, Any]):
    """Render app card with pure HTML integrated action buttons"""
    
    # Handle delete confirmation state
    confirm_delete_display = ""
    if st.session_state.confirm_delete == app['id']:
        confirm_delete_display = f"""
        <div class="confirm-delete">
            ⚠️ Are you sure you want to delete "<strong>{app['name']}</strong>"? 
        </div>
        """
    
    # Determine button states
    delete_button_content = "⚠️ Confirm" if st.session_state.confirm_delete == app['id'] else "🗑️ Delete"
    delete_button_class = "confirm-btn" if st.session_state.confirm_delete == app['id'] else "delete-btn"
    delete_onclick = f"confirmDelete({app['id']})" if st.session_state.confirm_delete == app['id'] else f"deleteApp({app['id']})"
    
    # Main action button
    if app['url'] != '#' and app['url'].strip():
        main_button = f'<a href="{app["url"]}" target="_blank" class="action-btn primary-btn">🚀 Buka App</a>'
    else:
        main_button = '<button class="action-btn primary-btn" disabled>🚀 Buka App</button>'
    
    # Complete app card HTML
    app_card_html = f"""
    <div class="app-card">
        <div class="app-header">
            <div class="app-icon {app['color']}">{app['icon']}</div>
            <div class="app-info">
                <h3 class="app-title">{app['name']}</h3>
                <span class="app-category">{app['category']}</span>
            </div>
        </div>
        <p class="app-description">{app['description']}</p>
        
        {confirm_delete_display}
        
        <div class="action-buttons-row">
            <button class="action-btn edit-btn" onclick="editApp({app['id']})">
                ✏️ Edit
            </button>
            <button class="action-btn {delete_button_class}" onclick="{delete_onclick}">
                {delete_button_content}
            </button>
            <button class="action-btn copy-btn" onclick="copyUrl('{app['url']}')">
                📋 Copy
            </button>
            {main_button}
        </div>
    </div>
    """
    
    st.markdown(app_card_html, unsafe_allow_html=True)

# Handle button clicks
def handle_button_clicks():
    """Handle button clicks from JavaScript"""
    # Check for query parameters or other mechanisms to detect button clicks
    query_params = st.experimental_get_query_params()
    
    if 'action' in query_params and 'appId' in query_params:
        action = query_params['action'][0]
        app_id = int(query_params['appId'][0])
        
        if action == 'edit':
            # Find and set app for editing
            app_to_edit = next((app for app in st.session_state.apps_data if app['id'] == app_id), None)
            if app_to_edit:
                st.session_state.editing_app = app_to_edit
                st.experimental_set_query_params()  # Clear query params
                st.rerun()
        
        elif action == 'delete':
            st.session_state.confirm_delete = app_id
            st.experimental_set_query_params()  # Clear query params
            st.rerun()
        
        elif action == 'confirm_delete':
            # Delete the app
            st.session_state.apps_data = [a for a in st.session_state.apps_data if a['id'] != app_id]
            st.session_state.confirm_delete = None
            
            # Find app name for notification
            app_name = f"App ID {app_id}"
            show_notification(f"App '{app_name}' deleted successfully", "success")
            st.experimental_set_query_params()  # Clear query params
            st.rerun()

# Mobile sidebar content
def render_mobile_sidebar():
    """Render mobile-optimized sidebar"""
    with st.sidebar:
        st.markdown("### 🛠️ Control Panel")
        
        # Auto CSV Loader Section
        st.markdown("#### 📁 Auto CSV Loader")
        
        if st.button("🔍 Scan Data Folder", use_container_width=True):
            with st.spinner("Scanning..."):
                st.session_state.detected_csv_files = scan_data_folder()
                if st.session_state.detected_csv_files:
                    show_notification(f"Found {len(st.session_state.detected_csv_files)} CSV files", "success")
                else:
                    show_notification("No CSV files found", "info")
                st.rerun()
        
        # Display detected CSV files in compact format
        if st.session_state.detected_csv_files:
            st.markdown("**Found CSV Files:**")
            for i, csv_file in enumerate(st.session_state.detected_csv_files):
                with st.expander(f"📄 {csv_file['name'][:20]}{'...' if len(csv_file['name']) > 20 else ''}", expanded=False):
                    st.markdown(f"**Size:** {csv_file['size']}")
                    st.markdown(f"**Modified:** {csv_file['last_modified']}")
                    
                    if st.button(f"📤 Load", key=f"load_{i}", use_container_width=True):
                        with st.spinner("Loading..."):
                            new_apps = load_csv_file(csv_file['path'])
                            if new_apps:
                                st.session_state.apps_data.extend(new_apps)
                                show_notification(f"Loaded {len(new_apps)} apps", "success")
                                st.rerun()
        
        st.divider()
        
        # Manual CSV Upload
        st.markdown("#### 📤 Manual Upload")
        uploaded_file = st.file_uploader("Choose CSV file", type="csv", label_visibility="collapsed")
        
        if uploaded_file is not None:
            with st.spinner("Processing..."):
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
                    show_notification(f"Loaded {len(new_apps)} apps", "success")
                    st.rerun()
        
        st.divider()
        
        # Export/Import Controls
        st.markdown("#### 💾 Data Management")
        
        if st.button("📥 Export CSV", use_container_width=True):
            df = pd.DataFrame(st.session_state.apps_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"apps_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        if st.button("🔄 Reset to Default", use_container_width=True):
            if st.button("⚠️ Confirm Reset", key="confirm_reset", use_container_width=True):
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
                show_notification("Reset to default", "success")
                st.rerun()

# Alternative approach using Streamlit buttons with unique keys
def render_app_card_with_streamlit_buttons(app: Dict[str, Any]):
    """Render app card with Streamlit buttons but custom styling"""
    
    # App card HTML structure
    st.markdown(f"""
    <div class="app-card">
        <div class="app-header">
            <div class="app-icon {app['color']}">{app['icon']}</div>
            <div class="app-info">
                <h3 class="app-title">{app['name']}</h3>
                <span class="app-category">{app['category']}</span>
            </div>
        </div>
        <p class="app-description">{app['description']}</p>
    """, unsafe_allow_html=True)
    
    # Show delete confirmation message if needed
    if st.session_state.confirm_delete == app['id']:
        st.markdown(f"""
        <div class="confirm-delete">
            ⚠️ Are you sure you want to delete "<strong>{app['name']}</strong>"? 
            Click "Confirm Delete" below to proceed.
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons using Streamlit but with custom container
    st.markdown('<div class="action-buttons-row">', unsafe_allow_html=True)
    
    # Create columns for better button layout
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    # Edit button
    with col1:
        if st.button("✏️ Edit", key=f"edit_btn_{app['id']}", 
                    help="Edit this application", use_container_width=True):
            st.session_state.editing_app = app
            # Clear any delete confirmations
            if 'confirm_delete' in st.session_state:
                st.session_state.confirm_delete = None
            st.rerun()
    
    # Delete button with confirmation
    with col2:
        if st.session_state.confirm_delete == app['id']:
            if st.button("⚠️ Confirm", key=f"confirm_delete_btn_{app['id']}", 
                        help="Confirm deletion", use_container_width=True, type="primary"):
                # Remove app from data
                st.session_state.apps_data = [a for a in st.session_state.apps_data if a['id'] != app['id']]
                st.session_state.confirm_delete = None
                show_notification(f"App '{app['name']}' deleted successfully", "success")
                st.rerun()
        else:
            if st.button("🗑️ Delete", key=f"delete_btn_{app['id']}", 
                        help="Delete this application", use_container_width=True):
                st.session_state.confirm_delete = app['id']
                st.rerun()
    
    # Copy URL button
    with col3:
        if st.button("📋 Copy", key=f"copy_btn_{app['id']}", 
                    help="Show URL for copying", use_container_width=True):
            st.code(app['url'], language=None)
            show_notification("URL displayed above for copying", "info")
    
    # Main action button - Open App
    with col4:
        if app['url'] != '#' and app['url'].strip():
            st.link_button("🚀 Buka App", app['url'], use_container_width=True)
        else:
            st.button("🚀 Buka App", disabled=True, use_container_width=True, 
                     help="URL not available")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# Main app
def main():
    load_css()
    init_session_state()
    
    # Mobile-optimized header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Dashboard Streamlit 2025</h1>
        <div>
            <div class="streamlit-badge">Auto CSV Loader</div>
            <div class="streamlit-badge">ML Apps</div>
        </div>
        <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">Platform Terpadu dengan Auto-Upload CSV</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Render notifications
    render_notification()
    
    # Mobile sidebar
    render_mobile_sidebar()
    
    # Main content area
    # Mobile search and add button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search applications...", 
                                   placeholder="Cari nama app, kategori...", 
                                   label_visibility="collapsed")
    
    with col2:
        if st.button("➕ Add App", use_container_width=True):
            st.session_state.show_add_form = True
            # Clear any delete confirmations
            if 'confirm_delete' in st.session_state:
                st.session_state.confirm_delete = None
            st.rerun()
    
    # Statistics - mobile optimized
    categories = list(set(app['category'] for app in st.session_state.apps_data))
    active_apps = sum(1 for app in st.session_state.apps_data if app['url'] != '#')
    
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-item">
            <span class="stat-value">{len(st.session_state.apps_data)}</span>
            <span class="stat-label">Total Apps</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{len(categories)}</span>
            <span class="stat-label">Categories</span>
        </div>
        <div class="stat-item">
            <span class="stat-value">{active_apps}</span>
            <span class="stat-label">Active</span>
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
    
    # Display apps with integrated action buttons
    if filtered_apps:
        for app in filtered_apps:
            render_app_card_with_streamlit_buttons(app)
    else:
        st.info("🔍 No applications found matching your search.")
    
    # Add/Edit form - mobile optimized
    if st.session_state.get('show_add_form', False) or st.session_state.get('editing_app', None):
        st.divider()
        
        editing_app = st.session_state.get('editing_app', None)
        title = "Edit Application" if editing_app else "Add New Application"
        
        with st.expander(f"📝 {title}", expanded=True):
            with st.form("app_form"):
                # Mobile-friendly form layout
                name = st.text_input("App Name", 
                                   value=editing_app['name'] if editing_app else "",
                                   placeholder="e.g., QOE Dashboard")
                
                category = st.selectbox("Category", 
                                      options=["Machine Learning", "Data Science", "Analytics", 
                                             "Visualization", "Dashboard", "Web App", "Python"],
                                      index=["Machine Learning", "Data Science", "Analytics", 
                                           "Visualization", "Dashboard", "Web App", "Python"].index(editing_app['category']) if editing_app else 0)
                
                url = st.text_input("Streamlit URL", 
                                  value=editing_app['url'] if editing_app else "",
                                  placeholder="https://your-app.streamlit.app/")
                
                col1, col2 = st.columns(2)
                with col1:
                    icon = st.text_input("Icon (1 char)", 
                                       value=editing_app['icon'] if editing_app else "",
                                       max_chars=1,
                                       placeholder="Q")
                
                with col2:
                    color = st.selectbox("Color Theme",
                                       options=["streamlit", "machine-learning", "data-science", 
                                              "analytics", "visualization", "dashboard", 
                                              "python", "web-app"],
                                       index=["streamlit", "machine-learning", "data-science", 
                                            "analytics", "visualization", "dashboard", 
                                            "python", "web-app"].index(editing_app['color']) if editing_app else 0)
                
                description = st.text_area("Description", 
                                         value=editing_app['description'] if editing_app else "",
                                         placeholder="App description...",
                                         height=100)
                
                # Mobile-friendly form buttons
                col1, col2 = st.columns(2)
                
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
                                if 'editing_app' in st.session_state:
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
                            
                            # Clear any delete confirmations
                            if 'confirm_delete' in st.session_state:
                                st.session_state.confirm_delete = None
                            st.rerun()
                        else:
                            st.error("Please fill in all required fields (Name, Category, Description, Icon)")
                
                with col2:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        if editing_app:
                            if 'editing_app' in st.session_state:
                                del st.session_state.editing_app
                        else:
                            st.session_state.show_add_form = False
                        
                        # Clear any delete confirmations
                        if 'confirm_delete' in st.session_state:
                            st.session_state.confirm_delete = None
                        st.rerun()
    
    # Mobile floating action button for quick access
    if not st.session_state.get('show_add_form', False) and not st.session_state.get('editing_app', None):
        st.markdown("""
        <style>
        .floating-sidebar-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 32px rgba(255, 75, 75, 0.4);
            z-index: 1000;
            cursor: pointer;
            color: white;
            font-size: 24px;
            font-weight: bold;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        .floating-sidebar-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 40px rgba(255, 75, 75, 0.5);
        }
        </style>
        
        <div class="floating-sidebar-btn" title="Open Control Panel">
            ⚙️
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem; font-size: 0.9rem;">
        <div style="margin-bottom: 0.5rem;">
            <strong>Streamlit Auto-Loader v4.0 Mobile</strong>
        </div>
        <div style="font-size: 0.8rem; opacity: 0.8;">
            2025 Edition | Optimized for Mobile
        </div>
        <div style="margin-top: 0.5rem; font-size: 0.8rem;">
            📱 Integrated Actions | 🚀 Touch Friendly
        </div>
        <div style="margin-top: 0.3rem; font-size: 0.7rem; opacity: 0.6;">
            Edit, Delete, Copy & Launch - All in one card
        </div>
        <div style="margin-top: 0.3rem; font-size: 0.7rem; color: #28a745;">
            ✅ Ready to Use | 🎯 Fully Functional
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()