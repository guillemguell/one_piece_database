# src/scraper/devil_fruits.py

import requests
from bs4 import BeautifulSoup
import re
import spacy
import os

nlp = spacy.load("en_core_web_sm")

BASE_URL = "https://onepiece.fandom.com"
PAGE = "https://onepiece.fandom.com/wiki/Devil_Fruit"
# HEADERS = {"User-Agent": "mozilla/5.0"}
HEADERS = {
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
  */*;q=0.8",
  "Accept-Language": "en-US,en;q=0.8",
  "Cache-Control": "no-cache",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/5\
  37.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}






def scrape_devil_fruits(limit = None):
    """
    Scrape and return a list of devil fruits with their details.
    """
    r = requests.get(PAGE, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")

    df_table = soup.find("table", attrs={"title": "Devil Fruits Navibox"})
    if not df_table:
        raise ValueError("Devil Fruits table not found")

    dfs = []

    dfs = scrape_logia_paramecia(df_table, 'Paramecia', dfs)
    dfs = scrape_zoan(df_table, 'Zoan', dfs)
    dfs = scrape_logia_paramecia(df_table, 'Logia', dfs)
    dfs = scrape_undetermined_class(df_table, 'Undetermined Class', dfs) 

    
    # # Paramecia devil fruits
    # df_category = 'Paramecia'

    # df_paramecia_table = df_table.find('a', attrs={'title': df_category}).find_parent('table')
    # df_paramecia_canon = df_paramecia_table.find(['span','th'], string='Canon:').find_parent('tr').find_all('li')
    # df_paramecia_non_canon = df_paramecia_table.find(['span','th'], string='Non-Canon:').find_parent('tr').find_all('li')



    # df_paramecia = [(item, True) for item in df_paramecia_canon] \
    #               + [(item, False) for item in df_paramecia_non_canon]

    # for item, is_canon in df_paramecia:
    #     dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': df_category, 'subcategory': None, 'is_canon': is_canon})


    # # Zoan devil fruits
    # df_category = 'Zoan'
    # df_zoan_table = df_table.find('a', attrs={'title': df_category}).find_parent('table')

    # df_zoan_standard = df_zoan_table.find(['span','th'], string=re.compile('Standard')).find_parent('tr').find_all('li')
    # df_zoan_ancient = df_zoan_table.find(['span','th'], string=re.compile('Ancient')).find_parent('tr').find_all('li')
    # df_zoan_mythical = df_zoan_table.find(['span','th'], string=re.compile('Mythical')).find_parent('tr').find_all('li')
    # df_zoan_artificial = df_zoan_table.find(['span','th'], string=re.compile('Artificial')).find_parent('tr').find_all('li')


    # non_canon_re = re.compile(r'non-canon', re.IGNORECASE)

    # df_zoan = [(item, 'Standard') for item in df_zoan_standard] \
    #               + [(item, 'Ancient') for item in df_zoan_ancient] \
    #               + [(item, 'Mythical') for item in df_zoan_mythical] \
    #               + [(item, 'Artificial') for item in df_zoan_artificial]

    # for item, subcategoria in df_zoan:
    #     is_canon = True
    #     sups = item.find_all('sup')
    #     if sups:
    #         is_canon = not any(non_canon_re.search(sup.get_text()) for sup in sups)
    #     dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': df_category, 'subcategory': subcategoria, 'is_canon': is_canon})
                

    # # Logia devil fruits
    # df_category = 'Logia'
    # df_logia_table = df_table.find('a', attrs={'title': df_category}).find_parent('table')


    # df_logia_canon = df_logia_table.find(['span','th'], string='Canon:').find_parent('tr').find_all('li')
    # df_logia_non_canon = df_logia_table.find(['span','th'], string='Non-Canon:').find_parent('tr').find_all('li')

    # df_logia = [(item, True) for item in df_logia_canon] \
    #               + [(item, False) for item in df_logia_non_canon]

    # for item, is_canon in df_logia:
    #     dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': 'Logia', 'subcategory': None, 'is_canon': is_canon})


    # # Undetermined Class devil fruits 
    # df_category = 'Undetermined Class'
    # df_undetermined_class_table = df_table.find(['span','th'], string=df_category).find_parent('table')

    # df_undetermined_class_canon = df_undetermined_class_table.find(['span','th'], string='Canon:').find_parent('tr').find_all('li')
    # df_undetermined_class_non_canon = df_undetermined_class_table.find(['span','th'], string='Non-Canon:').find_parent('tr').find_all('li')

    # df_undetermined_class = [(item, True) for item in df_undetermined_class_canon] \
    #               + [(item, False) for item in df_undetermined_class_non_canon]

    # for item, is_canon in df_undetermined_class:
    #     dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': df_category, 'subcategory': None, 'is_canon': is_canon})

    # fruits = []
    # for df in dfs:
    #     name = df['name']
    #     url = df['url']
    #     category = df['category']
    #     subcategory = df['subcategory'] 
    #     is_canon = df['is_canon']

    #     fruits.append(Fruit(
    #         name=name,
    #         url=url,
    #         category=category,
    #         subcategory=subcategory,
    #         is_canon=is_canon
    #     ))


    dfs_to_process = dfs if limit is None else dfs[:limit]
    with requests.Session() as session:
        for df in dfs_to_process:
            details = scrape_df_details(df['url'], session=session)
            df['habilities'] = details.get('habilities')
            for stat_key, stat_value in details.get('statistics', {}).items():
                nk = normalize_stat_key(stat_key)
                if nk:
                    df[nk] = stat_value


    return dfs


def scrape_zoan(df_table, df_category, dfs):
    df_zoan_table = df_table.find('a', attrs={'title': df_category}).find_parent('table')

    df_zoan_standard = df_zoan_table.find(['span','th'], string=re.compile('Standard')).find_parent('tr').find_all('li')
    df_zoan_ancient = df_zoan_table.find(['span','th'], string=re.compile('Ancient')).find_parent('tr').find_all('li')
    df_zoan_mythical = df_zoan_table.find(['span','th'], string=re.compile('Mythical')).find_parent('tr').find_all('li')
    df_zoan_artificial = df_zoan_table.find(['span','th'], string=re.compile('Artificial')).find_parent('tr').find_all('li')


    non_canon_re = re.compile(r'non-canon', re.IGNORECASE)

    df_zoan = [(item, 'Standard') for item in df_zoan_standard] \
                  + [(item, 'Ancient') for item in df_zoan_ancient] \
                  + [(item, 'Mythical') for item in df_zoan_mythical] \
                  + [(item, 'Artificial') for item in df_zoan_artificial]

    for item, subcategoria in df_zoan:
        is_canon = True
        sups = item.find_all('sup')
        if sups:
            is_canon = not any(non_canon_re.search(sup.get_text()) for sup in sups)
        dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': df_category, 'subcategory': subcategoria, 'is_canon': is_canon})

    return dfs

def scrape_logia_paramecia(df_table, df_category, dfs):

    df_paramecia_table = df_table.find('a', attrs={'title': df_category}).find_parent('table')
    df_paramecia_canon = df_paramecia_table.find(['span','th'], string='Canon:').find_parent('tr').find_all('li')
    df_paramecia_non_canon = df_paramecia_table.find(['span','th'], string='Non-Canon:').find_parent('tr').find_all('li')



    df_paramecia = [(item, True) for item in df_paramecia_canon] \
                  + [(item, False) for item in df_paramecia_non_canon]

    for item, is_canon in df_paramecia:
        dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': df_category, 'subcategory': None, 'is_canon': is_canon})

    return dfs

def scrape_undetermined_class(df_table, df_category, dfs):

  df_undetermined_class_table = df_table.find(['span','th'], string=df_category).find_parent('table')

  df_undetermined_class_canon = df_undetermined_class_table.find(['span','th'], string='Canon:').find_parent('tr').find_all('li')
  df_undetermined_class_non_canon = df_undetermined_class_table.find(['span','th'], string='Non-Canon:').find_parent('tr').find_all('li')

  df_undetermined_class = [(item, True) for item in df_undetermined_class_canon] \
                + [(item, False) for item in df_undetermined_class_non_canon]

  for item, is_canon in df_undetermined_class:
      dfs.append({'name': item.a.string, 'url': BASE_URL+item.a['href'], 'category': df_category, 'subcategory': None, 'is_canon': is_canon})

  return dfs

def scrape_df_details(url, session=None, timeout=15):
    try:
        r = session.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
    except Exception:
        return {'description': None}

    soup = BeautifulSoup(r.content, "html.parser")
    habilities = get_habilities(soup)
    statistics = get_statistics(soup)
    save_image(soup)

    return {'habilities': habilities, 'statistics': statistics}

def get_habilities(soup):
    p = soup.find('div', attrs={'id': 'mw-content-text'}).find('div', attrs={'class': 'mw-content-ltr mw-parser-output'}).p

    for tag in p.find_all(['sup']):
        tag.decompose()

    text = p.get_text(" ", strip=True)
    idx = text.find('.')
    if idx != -1:
        text = text[:idx+1]
    return extract_ability(" ".join(text.split())) or None


def extract_ability(text):
    text = text.replace("\n", " ")

    doc = nlp(text)

    ability_phrases = []

    for sent in doc.sents:
        sent_text = sent.text.strip()


        pattern = r"((?:allows|grants|enables the user to|which|that).*?)(?:\.|$)"
        matches = re.findall(pattern, sent_text, re.IGNORECASE)

        for match in matches:
            ability_clean = re.sub(r"\(.*?\)", "", match)  
            ability_clean = re.sub(r"\[\d+\]", "", ability_clean)  
            ability_clean = ability_clean.strip()

            ability_clean = re.sub(r"^(which|that)\s+", "", ability_clean, flags=re.IGNORECASE)

            if ability_clean:
                ability_phrases.append(ability_clean)

    ability_description = " ".join(ability_phrases).strip()
    if ability_description:
      ability_description = ability_description[0].upper() + ability_description[1:]
    
    return ability_description

def get_statistics(soup):
    stats_section = soup.find('h2', string='Statistics').find_parent('section')
    divs_stats_section = stats_section.find_all('div')

    stats = {}
    for div in divs_stats_section:
        if div.find('h3'):
            key = div.find('h3').get_text()
            value_div = div.find('div')
            if not value_div:
                continue
            value = value_div.get_text(" ", strip=True)
            value = re.sub(r"\[\s*[0-9a-zA-Z]+\s*\]", " ", value)
            value = re.sub(r"\s{2,}", " ", value).strip()
            stats[key] = value

    return stats


def save_image(soup):
    toc = soup.find('div', id='toc').find('span', string=re.compile('Appearance'))

    if not toc:
        return
    
    image_src = soup.find('a', class_='image image-thumbnail').img.get('src')
    
    return load_requests(image_src)

def load_requests(source_url):
    if ".png" in source_url:
        clean_url = source_url.split(".png")[0] + ".png"
    else:
        clean_url = source_url

    r = requests.get(clean_url, stream=True)
    if r.status_code == 200:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # src/scraper
        project_root = os.path.abspath(os.path.join(script_dir, "../../"))  # one_piece_database
        folder = os.path.join(project_root, "data/raw/devil_fruits_imgs")
        os.makedirs(folder, exist_ok=True)

        filename = clean_url.split('/')[-1].replace("_Infobox", "")
        invalid_chars = '<>:"/\\|?*'
        for c in invalid_chars:
            filename = filename.replace(c, "_")

        ruta = os.path.join(folder, filename)

        print("Guardando en:", ruta)
        with open(ruta, "wb") as output:
            for chunk in r.iter_content(1024):
                output.write(chunk)
            
def normalize_stat_key(key: str) -> str:
    """Quita ':' y cambia espacios por guiones bajos; devuelve en minúsculas."""
    if not key:
        return ""
    k = key.replace(":", "").strip().lower()
    k = re.sub(r"\s+", "_", k)
    return k

if __name__ == "__main__":
    devil_fruits = scrape_devil_fruits()
    for fruit in devil_fruits[:10]:
        print(fruit)