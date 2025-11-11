"""
Test script to verify Gemini API setup
"""

import os
from dotenv import load_dotenv

def test_imports():
    """Test if required packages are installed"""
    print("🔍 Testing package imports...")
    
    packages = {
        'pandas': 'pandas',
        'google.generativeai': 'google-generativeai',
        'streamlit': 'streamlit',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All packages installed!")
    return True

def test_env():
    """Test environment configuration"""
    print("\n🔍 Testing environment setup...")
    
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("  ❌ GEMINI_API_KEY not found in .env file")
        print("\n📝 Create a .env file with:")
        print("GEMINI_API_KEY=your_api_key_here")
        print("\n🔗 Get your key at: https://aistudio.google.com/app/apikey")
        return False
    
    if api_key == 'your_gemini_api_key_here':
        print("  ❌ Please replace placeholder with actual API key")
        return False
    
    if not api_key.startswith('AIza'):
        print("  ⚠️ Gemini keys usually start with 'AIza'")
        print("  Your key might be invalid")
    
    print(f"  ✅ API key found (starts with: {api_key[:8]}...)")
    return True

def test_data_files():
    """Test if data files exist"""
    print("\n🔍 Testing data files...")
    
    if not os.path.exists('student_data.csv'):
        print("  ❌ student_data.csv not found")
        print("  Run: python create_sample_data.py")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv('student_data.csv')
        print(f"  ✅ student_data.csv loaded ({len(df)} records)")
        print(f"  ✅ {df['student_name'].nunique()} unique students")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_gemini_api():
    """Test Gemini API connection"""
    print("\n🔍 Testing Gemini API connection...")
    
    try:
        import google.generativeai as genai
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("  ⚠️ No API key found, skipping test")
            return True
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Say 'Hello from Gemini!'")
        
        print("  ✅ Gemini API connected successfully!")
        print(f"  ✅ Response: {response.text[:50]}...")
        return True
        
    except Exception as e:
        print(f"  ❌ API Error: {str(e)}")
        print("\n💡 Common issues:")
        print("  - Invalid API key")
        print("  - API not enabled")
        print("  - Network connectivity")
        return False

def main():
    print("=" * 60)
    print("🧪 GEMINI API SETUP VERIFICATION")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_env,
        test_data_files,
        test_gemini_api
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if all(results):
        print("\n🎉 All tests passed! You're ready to go!")
        print("\n📋 Next steps:")
        print("  1. Run: python ai_query_system_gemini.py (CLI version)")
        print("  2. Run: streamlit run streamlit_app_gemini.py (Web version)")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
    
    print("\n💡 Need help?")
    print("  - Gemini API Docs: https://ai.google.dev/")
    print("  - Get API Key: https://aistudio.google.com/app/apikey")
    print("=" * 60)

if __name__ == "__main__":
    main()