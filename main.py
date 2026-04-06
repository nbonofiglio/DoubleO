def main():
    import os
    import argparse
    from dotenv import load_dotenv
    from google import genai

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if (api_key is None):
        raise RuntimeError("missing Gemini API key")
    
    client = client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Prompt Gemini")
    parser.add_argument("user_prompt", type=str, help="User prompt text being sent to Gemini")
    args = parser.parse_args()

    response = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    if not prompt_tokens:
        raise RuntimeError("Invalid prompt token count")
    if not response_tokens:
        raise RuntimeError("Invalid response token count")
    
    print(f"Prompt tokens: ${prompt_tokens}\nResponse tokens: ${response_tokens}\nResponse: ${response.text}")

if __name__ == "__main__":
    main()
