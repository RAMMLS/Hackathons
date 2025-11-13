import requests

def solve():
    server = input()
    port = int(input())
    a = int(input())
    b = int(input())

    resp = requests.get(f"{server}:{port}", params={"a": a, "b": b})
    data = resp.json()
    result = data["result"]
    result.sort()
    print(*result)
    print(data["check"])

solve()
