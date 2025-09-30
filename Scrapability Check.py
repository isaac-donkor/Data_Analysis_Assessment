# check_scrapability.py
import requests
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

def check_robots(base_url, user_agent="MyBot"):
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
    rp.parse(r.text.splitlines())

    # Test a few typical paths (customize as needed)
    test_paths = ["/", "/shop/", "/products/", "/cart/"]
    for path in test_paths:
        full_url = urljoin(base_url, path)
        allowed = rp.can_fetch(user_agent, full_url)
        print(f"Can '{user_agent}' fetch {full_url}? -> {allowed}")

if __name__ == "__main__":
    # Replace with the site you want to check
    check_robots("https://terrywhitechemmart.com.au/shop/products/skin-care", user_agent="MyBot")
