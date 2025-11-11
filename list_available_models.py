"""
Script to list all available Gemini models for your API key
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit(1)

print("🔍 Checking available Gemini models...\n")

try:
    genai.configure(api_key=api_key)
    
    print("Available models that support generateContent:\n")
    print("-" * 60)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print(f"   Input Limit: {model.input_token_limit} tokens")
            print(f"   Output Limit: {model.output_token_limit} tokens")
            print("-" * 60)
    
    print("\n💡 Recommended models:")
    print("  • gemini-pro - Best for text (MOST STABLE)")
    print("  • gemini-1.5-pro - Latest, more capable")
    print("  • gemini-1.5-flash - Faster, good for most tasks")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Possible issues:")
    print("  - Invalid API key")
    print("  - Network connectivity")
    print("  - API not enabled for your account")