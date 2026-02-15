from browser.driver_factory import get_local_driver
from scraping.elpais_scraper import get_opinion_article_links, scrape_article
from translation.translator import translate_to_english
from utils.image_downloader import download_image
from analysis.text_analyzer import find_repeated_words_raw, find_repeated_words_semantic
from utils.output_writer import save_json

def run_pipeline(driver):
    links = get_opinion_article_links(driver)
    print(f"Found {len(links)} articles")

    results = []
    translated_titles = []

    for idx, link in enumerate(links):
        print(f"\nProcessing article {idx + 1}")

        data = scrape_article(driver, link)

        title = data["title"] or "No title found"
        content = data["content"] or "No content found"
        
        print("Spanish Title:", title)
        print("Content Preview:", content[:300] if len(content) > 300 else content, "...")
        
        translated = ""
        if data["title"]:
            translated = translate_to_english(data["title"])
        print("Translated Title:", translated if translated else "N/A")

        if data["image_url"]:
            download_image(data["image_url"], idx)

        results.append({
            "spanish_title": title,
            "english_title": translated,
            "content": content,
            "image_url": data["image_url"],
        })

        if translated:
            translated_titles.append(translated)

    raw_result = find_repeated_words_raw(translated_titles)
    semantic_result = find_repeated_words_semantic(translated_titles)

    print("\nRAW REPEATED WORDS (>2 times):")
    if raw_result:
        for word, count in raw_result.items():
            print(f"{word} → {count}")
    else:
        print("No words repeated more than twice.")

    print("\nSEMANTIC REPEATED WORDS (>2 times, stopwords removed):")
    if semantic_result:
        for word, count in semantic_result.items():
            print(f"{word} → {count}")
    else:
        print("No words repeated more than twice.")

    save_json(results)

if __name__ == "__main__":
    driver = get_local_driver()
    try:
        run_pipeline(driver)
    finally:
        driver.quit()
