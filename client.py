import argparse
from openai import OpenAI

def main():
    # Setup command line argument parsing
    parser = argparse.ArgumentParser(description="Send a request to the OpenAI API.")
    parser.add_argument("content", type=str, help="The content to send to the OpenAI API.")
    args = parser.parse_args()

    # Gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI(base_url="http://0.0.0.0:5000")

    # Non-streaming request
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": args.content,
            },
        ],
    )
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main()
