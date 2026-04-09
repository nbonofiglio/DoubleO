def main():
    import os
    import argparse
    from dotenv import load_dotenv
    from google import genai
    from google.genai import types
    from prompt import system_prompt

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if (api_key is None):
        raise RuntimeError("missing Gemini API key")
    
    client = client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Prompt Gemini")
    parser.add_argument("user_prompt", type=str, help="User prompt text being sent to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0),
        )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if not prompt_tokens:
        raise RuntimeError("Invalid prompt token count")
    if not response_tokens:
        raise RuntimeError("Invalid response token count")
    
    if args.verbose:
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}\nUser prompt: {args.user_prompt}\nResponse: {response.text}")
    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
