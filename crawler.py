import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque

def crawl_website(start_url):
    visited = set()
    queue = deque([start_url])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    

    print("Comenzando el crawling...")

    while queue:
        url = queue.popleft()
        if url in visited:
            continue

        visited.add(url)
        print(f"Visitando: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                if full_url.startswith(start_url) and full_url not in visited:
                    queue.append(full_url)
        except requests.RequestException as e:
            print(f"Error al acceder a {url}: {e}")

    print("\nCrawling completado. Total de páginas visitadas:", len(visited))
    return visited

if __name__ == "__main__":
    start_url = input("Introduce el URL inicial (ej. https://example.com): ")
    pages = crawl_website(start_url)

    with open("pages.txt", "w") as f:
        for page in pages:
            f.write(page + "\n")
    print("Resultados guardados en 'pages.txt'.")
