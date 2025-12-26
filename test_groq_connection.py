import os
import sys

def test_connection():
    print("=== Groq Connection Test ===\n")
    
    # 1. Check Library
    try:
        from groq import Groq
        print("✅ Library 'groq' is installed.")
    except ImportError:
        print("❌ Error: 'groq' library is not installed. Run 'pip install groq'.")
        return

    # 2. Check API Key
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY environment variable is not set.")
        print("   -> Please set it in your system environment variables.")
        print("   -> On Windows PowerShell: $env:GROQ_API_KEY='gsk_...'")
        return
    else:
        print(f"✅ API Key found: {api_key[:4]}...{api_key[-4:]}")

    # 3. Test Connection
    print("\nAttempting to connect to Groq API (llama3-70b-8192)...")
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a test assistant."},
                {"role": "user", "content": "Reply with 'Connection Successful!' if you receive this."}
            ],
            temperature=0,
            max_tokens=20
        )
        response_text = completion.choices[0].message.content
        print("\n✅ Success! AI Response:")
        print("-" * 30)
        print(response_text)
        print("-" * 30)
        
    except Exception as e:
        print(f"\n❌ Connection Failed: {str(e)}")

if __name__ == "__main__":
    test_connection()
