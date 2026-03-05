import time
import page
from playwright.sync_api import sync_playwright, expect

def test_logo_visible():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome",headless=False)

        page = browser.new_page()
        page.goto("https://training.pricefx.eu/app/#/login?redirect_url=%2F") # passing url

        myurl = page.url
        print("Url of the application:", myurl)

        expect(page).to_have_url("https://training.pricefx.eu/app/#/login?redirect_url=%2F") # expected url

        #page.getByAltText(): to locate an element, usually image, by its text alternative.

        logo = page.get_by_alt_text("Pricefx logo")
        expect(logo).to_be_visible()

        page.locator('#LoginForm\\:partition').wait_for(state="visible")
        page.locator('#LoginForm\\:partition').fill("ce-exam-0222")
        page.get_by_placeholder("Enter your username").fill("admin")
        page.get_by_placeholder("Enter your password").fill("#_4Kyr0_g0")
        page.locator('[data-test="login-loginbutton-button"]').click()
        page.locator("span:has-text('New Quote')").click()
        page.locator("a:has-text('SampleQuote')").click()
        time.sleep(3)
        date_field = page.locator("div[data-test='effective-date-field'] input")
        date_field.evaluate("""
            el => {
                el.removeAttribute('readonly');
                el.value = '01/01/2026';
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)
        expect(date_field).to_have_value("01/01/2026")
        page.locator("[data-test='customer-select-addon']").click()
        ##time.sleep(3)
        customer_search = page.locator("[data-test='quick-filter-Customer-Name-input'] input.ant-input")
        customer_search.wait_for(state="visible")
        customer_search.fill("Alpina Food")
        customer_search.press("Enter")
        page.locator(".ucRadio__input").first.click()
        page.get_by_text("Select item").click()
        page.locator("#Detail-\:QuoteDiscountPercent:visible").click()
        ##time.sleep(1)
        page.locator("text=Biggest").first.click()
        ##time.sleep(1)
        page.locator("span:has-text('Items')").click()
        page.locator("button[aria-label='Add Items'] span[role='img'] svg").click()
        ##time.sleep(1)
        page.locator("input[placeholder='Search']").fill("Meatball BM")
        time.sleep(1)
        page.locator("span.ucMenuItemContent__anchor").click()
        time.sleep(15)
        browser.close()  # Explicit cleanup
