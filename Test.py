import time
import pytest

from playwright.sync_api import Page, expect, sync_playwright

def test_pricefx():
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
        page.locator("[data-test=\"targetdate-input\"]").click()
        page.get_by_role("button", name="2026").click()
        page.get_by_text("2025").click()
        page.get_by_text("1").first.click()
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
        page.locator("[data-test=\"Q-detail-tab--items\"]").click()
        page.locator("[data-test=\"sfdc-import-add-items-button\"]").click()
        page.get_by_role("button", name="Meatball Bl MB-").click()
        page.get_by_role("row", name="Press SHIFT+SPACE to select").locator("input[type='checkbox']").click()
        page.locator("[data-test=\"productdiscountpercent-input\"]").click()
        page.locator("[data-test=\"productdiscountpercent-input\"]").fill("15")
        page.locator("[data-test=\"priceshop-recalculate-button\"]").click()
        page.locator("[data-test=\"common-submit-button\"]").click()
        page.locator(
            "[data-test=\"unity-quote-submitconfirmation-modal\"] [data-test=\"common-submit-button\"]").click()
        page.locator("[data-test=\"Q-detail-tab--workflow\"]").click()
        page.locator(
            ".ucButton.ucButton--hasIcon.ucButton--iconOnly.ucButton--iconOnlyColor-green > .ucButton__inner").click()
        page.get_by_role("textbox", name="Reason for your decision").click()
        page.get_by_role("textbox", name="Reason for your decision").fill("Test")
        page.locator("[data-test=\"common-approve-button\"]").click()
        browser.close()
