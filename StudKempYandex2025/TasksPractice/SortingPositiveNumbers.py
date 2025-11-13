import sys
import json
import requests

def main():
    input_lines = sys.stdin.read().splitlines()

    if len(input_lines) < 4:
        with open('input.txt', 'r', encoding='utf-8') as f:
            input_lines = [line.strip() for line in f.readlines()]

    url = input_lines[0].strip().rstrip('/')
    port = input_lines[1].strip()
    a = input_lines[2].strip()
    b = input_lines[3].strip()

    full_url = f"{url}:{port}?a={a}&b={b}"

    response = requests.get(full_url)
    numbers = json.loads(response.text)

    result = sorted([x for x in numbers if x > 0], reverse=True)

    output_text = '\n'.join(map(str, result))

    try:
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(output_text + '\n')
    except:
        pass

    print(output_text)

if __name__ == "__main__":
    main()
