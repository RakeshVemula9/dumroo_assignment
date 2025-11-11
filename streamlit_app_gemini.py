import streamlit as st
import pandas as pd
from ai_query_system_gemini import AdminQuerySystem
import os

# Page configuration
st.set_page_config(
    page_title="Dumroo AI Admin Panel - Gemini",
    page_icon="🎓",
    layout="wide"
)

# Title and description
st.title("🎓 Dumroo AI Admin Panel (Powered by Gemini)")
st.markdown("Ask questions about student data in plain English! 🚀 **FREE Gemini API**")

# Sidebar for admin configuration
st.sidebar.header("👤 Admin Access Control")

# API Key input with instructions
st.sidebar.markdown("### 🔑 Gemini API Key")
st.sidebar.info("Get your FREE API key at: https://aistudio.google.com/app/apikey")

api_key = st.sidebar.text_input(
    "Enter your Gemini API Key",
    type="password",
    value=os.getenv('GEMINI_API_KEY', ''),
    help="Free tier: 15 requests/min, 1500 requests/day"
)

# Grade and class selection
st.sidebar.markdown("### 🎯 Access Scope")
st.sidebar.info("Admins can only access data for their assigned grade and class.")

grade_options = ['All', 8, 9, 10]
selected_grade = st.sidebar.selectbox("Grade", grade_options)

class_options = ['All', 'A', 'B']
selected_class = st.sidebar.selectbox("Class Section", class_options)

# Convert 'All' to None for filtering
admin_grade = None if selected_grade == 'All' else selected_grade
admin_class = None if selected_class == 'All' else selected_class

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'system' not in st.session_state:
    st.session_state.system = None

# Initialize the system when API key is provided
if api_key:
    try:
        if st.session_state.system is None or \
           st.session_state.get('grade') != admin_grade or \
           st.session_state.get('class') != admin_class:
            
            with st.spinner("🔄 Initializing Gemini AI system..."):
                st.session_state.system = AdminQuerySystem(
                    api_key=api_key,
                    admin_grade=admin_grade,
                    admin_class=admin_class
                )
                st.session_state.grade = admin_grade
                st.session_state.class_ = admin_class
            
            # Show access info
            access_info = st.session_state.system.get_access_info()
            st.sidebar.success(f"✅ Connected to Gemini!\n\n"
                             f"📊 Access: Grade {access_info['grade']}, "
                             f"Class {access_info['class']}\n\n"
                             f"👥 Students: {access_info['total_students']}\n\n"
                             f"📄 Records: {access_info['total_records']}")
            
            # Show API info
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 💡 Gemini Free Tier")
            st.sidebar.markdown("""
            - ✅ 15 requests per minute
            - ✅ 1,500 requests per day
            - ✅ No credit card required
            - ✅ Completely FREE!
            """)
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")
        st.session_state.system = None
else:
    st.sidebar.warning("⚠️ Please enter your Gemini API key to continue")
    st.sidebar.markdown("""
    ### 📝 How to get API key:
    1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
    2. Sign in with Google
    3. Click "Get API Key"
    4. Copy and paste here
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Ask Questions")
    
    # Example queries as clickable suggestions
    with st.expander("📌 Click to see example queries", expanded=True):
        example_queries = [
            "Which students haven't submitted their homework yet?",
            "Show me students who scored below 70 in quizzes",
            "What's the average quiz score for my students?",
            "List all upcoming quizzes scheduled for next week",
            "Show me performance data from last week"
        ]
        
        for query in example_queries:
            if st.button(f"📌 {query}", key=query, use_container_width=True):
                if st.session_state.system:
                    st.session_state.messages.append({"role": "user", "content": query})
                    with st.spinner("🤔 Thinking..."):
                        response = st.session_state.system.query(query)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()

with col2:
    st.markdown("### 📊 Data Preview")
    if st.session_state.system:
        df = st.session_state.system.filtered_data
        st.dataframe(df.head(10), height=300)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Students", df['student_name'].nunique())
        with col_b:
            submitted = (df['submission_status'] == 'Submitted').sum()
            total = len(df)
            rate = (submitted/total*100) if total > 0 else 0
            st.metric("Submission Rate", f"{rate:.1f}%")

# Chat interface
st.markdown("---")

# Display chat messages
if st.session_state.messages:
    st.markdown("### 💭 Chat History")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Clear chat button
if st.session_state.messages and st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Chat input
if st.session_state.system:
    if prompt := st.chat_input("Type your question here... (e.g., 'Which students scored below 70?')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analyzing with Gemini..."):
                try:
                    response = st.session_state.system.query(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()
else:
    st.chat_input("Please configure your Gemini API key in the sidebar first...", disabled=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        🎓 Dumroo AI Admin Panel | Powered by Google Gemini Pro (FREE!) 🚀
    </div>
    """,
    unsafe_allow_html=True
)