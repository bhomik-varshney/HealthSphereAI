import argparse
import os
import sys
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd


@dataclass
class Business:
    """Holds hospital data"""
    name: str
    phone_number: str
    website: str
    address: str


@dataclass
class BusinessList:
    """Holds list of Business objects, saves to Excel and CSV"""
    business_list: list = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        return pd.DataFrame([asdict(business) for business in self.business_list])

    def save_to_excel(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"output/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str, default="hospitals in India", help="Search term for Google Maps.")
    parser.add_argument("-t", "--total", type=int, help="Total number of results to scrape (default is 100).")
    args = parser.parse_args()

    search_list = [args.search] if args.search else ["hospitals in India"]
    total = args.total if args.total else 100

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(2000)

        for search_for in search_list:
            print(f"Scraping: {search_for}")
            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

            previously_counted = 0
            while True:
                page.mouse.wheel(0, 5000)
                page.wait_for_timeout(2000)
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                if len(listings) >= total or len(listings) == previously_counted:
                    break
                previously_counted = len(listings)

            business_list = BusinessList()
            for listing in listings[:total]:
                try:
                    listing.click()
                    page.wait_for_timeout(2000)

                    business = Business(
                        name=listing.get_attribute('aria-label') or "",
                        phone_number=page.locator(
                            '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]').inner_text() if page.locator(
                            '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]').count() > 0 else "",
                        website=page.locator(
                            '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]').inner_text() if page.locator(
                            '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]').count() > 0 else "",
                        address=page.locator(
                            '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]').inner_text() if page.locator(
                            '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]').count() > 0 else ""
                    )
                    business_list.business_list.append(business)
                except Exception as e:
                    print(f'Error occurred: {e}')

            business_list.save_to_excel(f"hospitals_data_{search_for}".replace(' ', '_'))
            business_list.save_to_csv(f"hospitals_data_{search_for}".replace(' ', '_'))

        browser.close()


if __name__ == "__main__":
    main()
