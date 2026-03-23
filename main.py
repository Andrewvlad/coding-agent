import argparse
import sys
import os
from dotenv import load_dotenv
from config import MODEL, MAX_ITERATIONS, WORKING_DIRECTORY, SYSTEM_PROMPT

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


def parse_args():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--info", action="store_true", help="Enable info data output")
    args = parser.parse_args()
    return args.user_prompt, args.info


def process_function_calls(response, messages, verbose):
    function_responses = []

    if response.candidates:
        for candidate in response.candidates:
            if candidate is None or candidate.content is None:
                continue
            messages.append(candidate.content)

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)

            if not function_call_result.parts:
                raise Exception('Function call results missing parts.')

            if not function_call_result.parts[0].function_response:
                raise Exception('Function call results missing function response.')

            if not function_call_result.parts[0].function_response.response:
                raise Exception('Function call results missing function result.')

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            function_responses.append(function_call_result.parts[0])

        messages.append(types.Content(role="user", parts=function_responses))
        return True
    else:
        # Final agent response
        print('Response: ')
        print(response.text)
        return False


def run_agent(prompt, verbose):
    load_dotenv()
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ],
    )
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=SYSTEM_PROMPT,
    )

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    for _ in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=messages,
                config=config,
            )
        except ClientError as e:
            print(f'Error: Ran out of API tokens {e}')
            sys.exit(1)
        except Exception as e:
            print(f'Error: calling model {e}')
            sys.exit(1)

        if response is None or response.usage_metadata is None:
            print('Response error:')
            print(response)
            return

        if verbose:
            print('Prompt tokens: ', response.usage_metadata.prompt_token_count)
            print('Response tokens: ', response.usage_metadata.candidates_token_count)

        if not process_function_calls(response, messages, verbose):
            return

    print(f'Error: Exceeded max iterations ({MAX_ITERATIONS})')
    sys.exit(1)


def main():
    print('Running coding agent...')
    prompt, verbose = parse_args()

    if verbose:
        print('Prompt: ', prompt)

    run_agent(prompt, verbose)


if __name__ == "__main__":
    main()
