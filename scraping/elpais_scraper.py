from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

OPINION_URL = "https://elpais.com/opinion/"

def accept_cookies(driver):
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button#didomi-notice-agree-button, button[aria-label='Aceptar']")
            )
        )
        btn.click()
        time.sleep(1)
    except:
        pass

def get_opinion_article_links(driver):
    driver.get(OPINION_URL)
    time.sleep(2)  
    accept_cookies(driver)
    
    wait = WebDriverWait(driver, 20)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
    )
    
    articles = driver.find_elements(By.CSS_SELECTOR, "article h2 a")

    links = []
    for a in articles:
        href = a.get_attribute("href")
        if href and "/opinion/" in href and href not in links:
            links.append(href)
        if len(links) == 5:
            break
    
    return links


def scrape_article(driver, url):
    driver.get(url)
    time.sleep(2)  
    
    wait = WebDriverWait(driver, 20)
    
    title = ""
    try:
        title_el = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.a_t, h1[class*='title'], article h1"))
        )
        title = title_el.text.strip()
    except:
        print("Title not found for this article")

    content = ""
    try:
        content_selectors = [
            "div[data-dtm-region='articulo_cuerpo']",
            "div.a_c",
            "article div.article-body",
            "div.article_body"
        ]
        
        for selector in content_selectors:
            try:
                content_container = driver.find_element(By.CSS_SELECTOR, selector)
                paragraphs = content_container.find_elements(By.TAG_NAME, "p")
                content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])
                if content:
                    break
            except:
                continue
                
        if not content:
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "article p")
            content = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])
            
    except Exception as e:
        print(f"Content not found for this article: {e}")

    if not content:
        print("Content not found for this article")

    image_url = None
    try:
        img = driver.find_element(By.CSS_SELECTOR, "figure img, article img")
        image_url = img.get_attribute("src")
    except:
        pass

    return {
        "title": title,
        "content": content,
        "image_url": image_url,
    }