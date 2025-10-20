import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://onepiece.fandom.com"

def _is_non_canon_from_li(li):
    if not li:
        return False
    text = li.get_text(" ", strip=True)
    if "non-canon" in text.lower() or "≠" in text:
        return True
    for sup in li.find_all(["sup", "span"]):
        if "non-canon" in (sup.get("title") or "").lower():
            return True
    return False

def scrape_devil_fruits(limit=None):
    """
    Scrape all Devil Fruits from One Piece Wiki.
    """
    url = "https://onepiece.fandom.com/wiki/Devil_Fruit"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")

    main_table = soup.find("table", attrs={"title": "Devil Fruits Navibox"})
    if not main_table:
        raise ValueError("Could not find Devil Fruits table")

    fruits, seen = [], set()
    for inner in main_table.find_all("table", class_="collapsible"):
        sec_th = inner.find("th", scope="col")
        section = sec_th.get_text(strip=True) if sec_th else "Unknown"

        if "related" in section.lower():
            continue

        for row in inner.find_all("tr"):
            th = row.find("th", scope="row") or row.find("th")
            row_label = th.get_text(strip=True).rstrip(":") if th else "Items"
            td = row.find("td")
            if not td:
                continue

            items = td.find_all("li") or td.find_all("a", href=True)
            for item in items:
                a = item if item.name == "a" else item.find("a", href=True)
                if not a or not a["href"].startswith("/wiki/"):
                    continue
                href = a["href"]
                if any(href.startswith(f"/wiki/{ns}:") for ns in ["Category", "File", "Template", "Help", "Special"]):
                    continue

                name = a.get("title") or a.get_text(strip=True)
                url_full = urljoin(BASE, href)
                if url_full in seen:
                    continue
                seen.add(url_full)

                # Canon check (Zoan special logic)
                if section.lower() == "zoan":
                    label = "Non-Canon" if _is_non_canon_from_li(item) else "Canon"
                    section = "Zoan"
                else:
                    label = row_label

                fruits.append({
                    "name": name,
                    "url": url_full,
                    "section": section,
                    "row_label": label
                })

                if limit and len(fruits) >= limit:
                    return fruits

    return fruits
