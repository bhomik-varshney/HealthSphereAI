import os
import time
from playwright.sync_api import sync_playwright
import pandas as pd
from dataclasses import dataclass, asdict, field

@dataclass
class Business:
    """Holds hospital data"""
    name: str
    phone_number: str
    website: str
    address: str

@dataclass
class BusinessList:
    """Holds list of Business objects, saves to CSV"""
    business_list: list = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        return pd.DataFrame([asdict(business) for business in self.business_list])

    def save_to_csv(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        filepath = f"{self.save_at}/{filename}.csv"
        self.dataframe().to_csv(filepath, index=False)
        return filepath  # Return the saved file path

def scrape_hospitals(location: str, search_type="hospitals in or near"):
    """Scrapes hospital data and saves to CSV"""
    filename = f"hospitals_data_{search_type}_{location.replace(' ', '_')}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        time.sleep(2)

        print(f"Scraping: {location}")
        page.locator('//input[@id="searchboxinput"]').fill(f"{search_type} {location}")
        page.keyboard.press("Enter")
        time.sleep(5)

        listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
        
        business_list = BusinessList()
        for listing in listings[:10]:  # Scrape only first 10 results for speed
            try:
                listing.click()
                time.sleep(2)

                business = Business(
                    name=listing.get_attribute('aria-label') or "N/A",
                    phone_number=page.locator('//button[contains(@data-item-id, "phone:tel:")]//div').inner_text() if page.locator('//button[contains(@data-item-id, "phone:tel:")]//div').count() > 0 else "N/A",
                    website=page.locator('//a[@data-item-id="authority"]//div').inner_text() if page.locator('//a[@data-item-id="authority"]//div').count() > 0 else "N/A",
                    address=page.locator('//button[@data-item-id="address"]//div').inner_text() if page.locator('//button[@data-item-id="address"]//div').count() > 0 else "N/A"
                )
                business_list.business_list.append(business)
            except Exception as e:
                print(f'Error occurred: {e}')
        
        browser.close()
    
    return business_list.save_to_csv(filename)  # Return file path
