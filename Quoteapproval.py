import re
import allure
from playwright.sync_api import sync_playwright, expect

@allure.feature("Quote Management")
@allure.story("Create, Submit and Approve Quote")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("This test logs into Pricefx, creates a new quote, adds items, applies discounts, submits the quote, and approves it.")
def test_work():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        # ------------------- LOGIN -------------------
        with allure.step("Navigate to Pricefx demo login page"):
            page.goto(
                "https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fqc%2Fquotes"
            )
            assert page.url.startswith("https://demo.pricefx.com")
            allure.attach(page.screenshot(), name="Login Page", attachment_type=allure.attachment_type.PNG)

        with allure.step("Validate login page elements"):
            expect(page.locator("div").filter(has_text="Login").nth(5)).to_be_visible()
            expect(page.locator("[data-test='login-username-field']")).to_contain_text("Username")
            allure.attach(page.screenshot(), name="Login Elements", attachment_type=allure.attachment_type.PNG)

        with allure.step("Enter username and password"):
            page.locator("[data-test='username-input']").fill("shreyas")
            page.locator("[data-test='password-input']").fill("Start123!")
            allure.attach(page.screenshot(), name="Credentials Entered", attachment_type=allure.attachment_type.PNG)

        with allure.step("Click login and validate dashboard"):
            page.locator("[data-test='login-loginbutton-button']").click()
            page.wait_for_timeout(5000)
            expect(page.get_by_text("demofx_experisQuotingQuotes")).to_be_visible()
            allure.attach(page.screenshot(), name="Dashboard Loaded", attachment_type=allure.attachment_type.PNG)

        # ------------------- CREATE QUOTE -------------------
        with allure.step("Create new quote"):
            page.locator("[data-test='priceshop-newquotename-button']").wait_for(state="visible", timeout=60000)
            page.locator("[data-test='priceshop-newquotename-button']").click()
            page.get_by_role("link", name="Automation_Quote").wait_for(state="visible", timeout=60000)
            page.get_by_role("link", name="Automation_Quote").click()
            expect(page.get_by_text("(New Quote)")).to_be_visible()
            allure.attach(page.screenshot(), name="New Quote Page", attachment_type=allure.attachment_type.PNG)

        with allure.step("Set Effective and Expiry Dates"):
            page.locator("[data-test='targetdate-input']").click()
            page.get_by_role("button", name="2026").click()
            page.get_by_text("2025").click()
            page.get_by_text("1").nth(2).click()
            page.locator("[data-test='expirydate-input']").click()
            page.get_by_text("Today").nth(1).click()
            allure.attach(page.screenshot(), name="Dates Set", attachment_type=allure.attachment_type.PNG)

        # ------------------- SELECT CUSTOMER -------------------
        with allure.step("Select Customer CH-0001"):
            page.locator("[data-test='customer-select-addon']").click()
            customer_input = page.locator("[data-test='quick-filter-Customer-Id-input']").get_by_role("textbox")
            customer_input.fill("CH-0001")
            customer_input.press("Enter")
            page.get_by_role("row", name="Press SHIFT+SPACE to select").get_by_label("", exact=True).wait_for(state="visible")
            page.get_by_role("row", name="Press SHIFT+SPACE to select").get_by_label("", exact=True).click()
            page.get_by_text("Select item").click()
            allure.attach(page.screenshot(), name="Customer Selected", attachment_type=allure.attachment_type.PNG)

        # ------------------- QUOTE DISCOUNT -------------------
        with allure.step("Set Quote Discount Percent"):
            page.locator("[id='Detail-:QuoteDiscountPercent']").wait_for(state="visible")
            page.locator("[id='Detail-:QuoteDiscountPercent']").click()
            page.get_by_text("Biggest").wait_for(state="visible")
            page.get_by_text("Biggest").click()
            allure.attach(page.screenshot(), name="Discount Set", attachment_type=allure.attachment_type.PNG)

        # ------------------- ADD ITEM & PRODUCT DISCOUNT -------------------
        with allure.step("Add item and set product discount"):
            # Ensure Items tab is active
            page.locator("[data-test='Q-detail-tab--items']").click()
            # Wait for Add Items button
            page.locator("[data-test='sfdc-import-add-items-button']").wait_for(state="visible", timeout=60000)
            page.locator("[data-test='sfdc-import-add-items-button']").click()

            page.get_by_role("button", name="S1250 SEAL").wait_for(state="visible")
            page.get_by_role("button", name="S1250 SEAL").click()
            page.get_by_role("row", name="Press SHIFT+SPACE to select").get_by_label("", exact=True).wait_for(state="visible")
            page.get_by_role("row", name="Press SHIFT+SPACE to select").get_by_label("", exact=True).click()

            page.locator("[data-test='productdiscountpercent-input']").wait_for(state="visible")
            page.locator("[data-test='productdiscountpercent-input']").fill("10")

            page.locator("[data-test='priceshop-recalculate-button']").wait_for(state="visible")
            page.locator("[data-test='priceshop-recalculate-button']").click()
            expect(page.get_by_text("Quote calculated successfully")).to_be_visible()
            allure.attach(page.screenshot(), name="Item Added & Discount Applied", attachment_type=allure.attachment_type.PNG)

        # ------------------- FINISH & SUBMIT -------------------
        with allure.step("Finish quote creation and submit"):
            page.locator("[data-test='creationworkflow-finish-button']").wait_for(state="visible")
            page.locator("[data-test='creationworkflow-finish-button']").click()
            comment_box = page.get_by_role("textbox", name="Your comment (optional)")
            comment_box.wait_for(state="visible")
            comment_box.fill("Test")
            page.locator("[data-test='common-submit-button']").click()
            expect(page.get_by_text("Quote submitted successfully")).to_be_visible()
            expect(page.get_by_text("Draft - Submitted")).to_be_visible()
            allure.attach(page.screenshot(), name="Quote Submitted", attachment_type=allure.attachment_type.PNG)

        # ------------------- APPROVE QUOTE -------------------
        with allure.step("Approve quote workflow"):
            page.locator("[data-test='Q-detail-tab--workflow']").click()
            approve_button = page.locator(".ucButton--iconOnlyColor-green > .ucButton__inner")
            approve_button.wait_for(state="visible")
            approve_button.click()

            reason_box = page.get_by_role("textbox", name="Reason for your decision")
            reason_box.wait_for(state="visible")
            reason_box.fill("Test")

            page.locator("[data-test='common-approve-button']").click()
            expect(page.get_by_text("Quote has been approved")).to_be_visible()
            expect(page.get_by_role("button", name="Deal - Approved")).to_be_visible()
            allure.attach(page.screenshot(), name="Quote Approved", attachment_type=allure.attachment_type.PNG)

        # Close browser
        browser.close()
