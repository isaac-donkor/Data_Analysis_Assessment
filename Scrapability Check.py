# check_scrapability.py
import requests
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
import os

def check_robots(base_url, user_agent="MyBot"):
    if not base_url.startswith("http"):
        base_url = "https://" + base_url
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    robots_url = urljoin(base_url, "/robots.txt")
    print(f"Fetching robots.txt from {robots_url} ...")

    try:
        r = requests.get(robots_url, timeout=10)
    except Exception as e:
        print("Error fetching robots.txt:", e)
        return

    if r.status_code != 200:
        print(f"No robots.txt found (status {r.status_code})")
        return

    # Parse rules
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.parse(r.text.splitlines())

    # Prepare output file path
    output_file = os.path.join(os.path.dirname(__file__), "robots_check_results.txt")

    # Open file in write mode
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Robots.txt checked from {robots_url}\n\n")

        test_paths = ["/", "/shop/", "/products/", "/cart/"]
        for path in test_paths:
            full_url = urljoin(base_url, path)
            allowed = rp.can_fetch(user_agent, path)
            result = f"Can '{user_agent}' fetch {full_url}? -> {allowed}"
            print(result)
            f.write(result + "\n")

    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    # Use the domain, not a deep URL
    check_robots("https://terrywhitechemmart.com.au", user_agent="MyBot")
