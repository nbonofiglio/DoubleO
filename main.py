def main():
    import os
    import argparse
    from dotenv import load_dotenv
    from google import genai
    from google.genai import types
    from prompt import system_prompt
    from call_function import available_functions, call_function

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if (api_key is None):
        raise RuntimeError("missing Gemini API key")
    
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Prompt Gemini")
    parser.add_argument("user_prompt", type=str, help="User prompt text being sent to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(20):
 
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )

        for candidate in response.candidates:
            messages.append(candidate.content)
    
        functions = response.function_calls

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

        if not prompt_tokens:
            raise RuntimeError("Invalid prompt token count")
        if not response_tokens:
            raise RuntimeError("Invalid response token count")

        if (functions == None):
            print(f"-> {response.text}")
            break

        results = []
   
        for function in functions:
            function_call_result = call_function(function, verbose=args.verbose)
            if (len(function_call_result.parts) == 0):
                raise Exception(f"Result of {function} is empty and should not be")
            if (function_call_result.parts[0].function_response is None):
                raise Exception(f"Response for {function} has no value")
            if (function_call_result.parts[0].function_response.response is None):
                raise Exception("Response attribute of Response object has not value")
            results.append(function_call_result.parts[0])
            if (args.verbose):
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=results))

    else:
        print("Iteration limit reached")
        exit(1)

if __name__ == "__main__":
    main()
