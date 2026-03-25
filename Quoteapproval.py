import re
import allure
from playwright.sync_api import sync_playwright, expect

@allure.feature("Quote Management")
@allure.story("Create, Submit and Approve Quote")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description(
    "This test logs into Pricefx, creates a new quote, adds items, applies discounts, submits the quote, and approves it. Every validation is a separate step with screenshots. Waits are added to prevent timeout errors.")
def test_quoteapproval():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        # ------------------- Step 1: Navigate to Login -------------------
        with allure.step("Open Pricefx demo login page and validate URL"):
            page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fqc%2Fquotes")
            assert page.url.startswith("https://demo.pricefx.com")
            allure.attach(page.screenshot(), name="Login Page", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 2: Validate Login Elements -------------------
        with allure.step("Validate Login header and username field"):
            page.locator("div").filter(has_text="Login").nth(5).wait_for(state="visible")
            expect(page.locator("div").filter(has_text="Login").nth(5)).to_be_visible()

            page.locator("[data-test='login-username-field']").wait_for(state="visible")
            expect(page.locator("[data-test='login-username-field']")).to_contain_text("Username")
            allure.attach(page.screenshot(), name="Login Elements", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 3: Enter Credentials -------------------
        with allure.step("Fill in Username and Password"):
            page.locator("[data-test='username-input']").wait_for(state="visible")
            page.locator("[data-test='username-input']").fill("shreyas")
            page.locator("[data-test='password-input']").wait_for(state="visible")
            page.locator("[data-test='password-input']").fill("Start123!")
            allure.attach(page.screenshot(), name="Credentials Entered", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 4: Click Login and Validate Dashboard -------------------
        with allure.step("Click Login and validate dashboard is loaded"):
            page.locator("[data-test='login-loginbutton-button']").wait_for(state="visible")
            page.locator("[data-test='login-loginbutton-button']").click()
            page.get_by_text("demofx_experisQuotingQuotes").wait_for(state="visible")
            expect(page.get_by_text("demofx_experisQuotingQuotes")).to_be_visible()
            allure.attach(page.screenshot(), name="Dashboard Loaded", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 5: Create New Quote -------------------
        with allure.step("Create a new quote named 'Automation_Quote'"):
            page.locator("[data-test='priceshop-newquotename-button']").wait_for(state="visible")
            page.locator("[data-test='priceshop-newquotename-button']").click()
            page.get_by_role("link", name="Automation_Quote").wait_for(state="visible")
            page.get_by_role("link", name="Automation_Quote").click()
            page.get_by_text("(New Quote)").wait_for(state="visible")
            expect(page.get_by_text("(New Quote)")).to_be_visible()
            allure.attach(page.screenshot(), name="New Quote Page", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 6: Set Effective and Expiry Dates -------------------
        with allure.step("Set Effective Date and Expiry Date"):
            page.locator("[data-test='targetdate-input']").wait_for(state="visible")
            page.locator("[data-test='targetdate-input']").click()
            page.get_by_role("button", name="2026").wait_for(state="visible")
            page.get_by_role("button", name="2026").click()
            page.get_by_text("2025").click()
            page.get_by_text("1").nth(2).click()
            page.locator("[data-test='expirydate-input']").wait_for(state="visible")
            page.locator("[data-test='expirydate-input']").click()
            page.get_by_text("Today").nth(1).click()
            allure.attach(page.screenshot(), name="Dates Set", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 7: Select Customer -------------------
        with allure.step("Select customer CH-0001"):
            page.locator("[data-test='customer-select-addon']").wait_for(state="visible")
            page.locator("[data-test='customer-select-addon']").click()
            page.locator("[data-test='quick-filter-Customer-Id-input']").get_by_role("textbox").wait_for(
                state="visible")
            page.locator("[data-test='quick-filter-Customer-Id-input']").get_by_role("textbox").fill("CH-0001")
            page.locator("[data-test='quick-filter-Customer-Id-input']").get_by_role("textbox").press("Enter")
            page.get_by_role("row", name="Press SHIFT+SPACE to select").wait_for(state="visible")
            page.get_by_role("row", name="Press SHIFT+SPACE to select").get_by_label("", exact=True).click()
            page.get_by_text("Select item").wait_for(state="visible")
            page.get_by_text("Select item").click()
            allure.attach(page.screenshot(), name="Customer Selected", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 8: Set Quote Discount -------------------
        with allure.step("Set Quote Discount Percent to 'Biggest'"):
            page.locator("[id='Detail-:QuoteDiscountPercent']").wait_for(state="visible")
            page.locator("[id='Detail-:QuoteDiscountPercent']").click()
            page.get_by_text("Biggest").wait_for(state="visible")
            page.get_by_text("Biggest").click()
            allure.attach(page.screenshot(), name="Discount Set", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 9: Add Item and Set Product Discount -------------------
        with allure.step("Add product S1250 SEAL and set 10% discount"):
            page.locator("[data-test='Q-detail-tab--items']").wait_for(state="visible")
            page.locator("[data-test='Q-detail-tab--items']").click()
            page.get_by_text("Start by adding an item").wait_for(state="visible")
            page.locator("[data-test='sfdc-import-add-items-button']").wait_for(state="visible")
            page.locator("[data-test='sfdc-import-add-items-button']").click()
            page.get_by_role("button", name="S1250 SEAL").wait_for(state="visible")
            page.get_by_role("button", name="S1250 SEAL").click()
            page.get_by_text("\"00000509 S1250 SEAL\" has").wait_for(state="visible")
            page.get_by_role("row", name="Press SHIFT+SPACE to select").get_by_label("", exact=True).click()
            page.locator("[data-test='productdiscountpercent-input']").wait_for(state="visible")
            page.locator("[data-test='productdiscountpercent-input']").fill("10")
            page.locator("div").filter(has_text=re.compile(r"^QuantityProduct Discount Percent %$")).nth(2).click()
            allure.attach(page.screenshot(), name="Item Added and Discount Set",
                          attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 10: Recalculate Quote -------------------
        with allure.step("Click Recalculate and validate success"):
            page.locator("[data-test='priceshop-recalculate-button']").wait_for(state="visible")
            page.locator("[data-test='priceshop-recalculate-button']").click()
            page.get_by_text("Quote calculated successfully").wait_for(state="visible")
            expect(page.get_by_text("Quote calculated successfully")).to_be_visible()
            allure.attach(page.screenshot(), name="Quote Recalculated", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 11: Finish and Submit Quote -------------------
        with allure.step("Finish quote and submit"):
            page.locator("[data-test='creationworkflow-finish-button']").wait_for(state="visible")
            page.locator("[data-test='creationworkflow-finish-button']").click()
            page.get_by_text("Submit confirmation").wait_for(state="visible")
            page.get_by_role("textbox", name="Your comment (optional)").fill("Test")
            page.locator("[data-test='common-submit-button']").wait_for(state="visible")
            page.locator("[data-test='common-submit-button']").click()
            page.get_by_text("Quote submitted successfully").wait_for(state="visible")
            expect(page.get_by_text("Quote submitted successfully")).to_be_visible()
            expect(page.get_by_text("Draft - Submitted")).to_be_visible()
            allure.attach(page.screenshot(), name="Quote Submitted", attachment_type=allure.attachment_type.PNG)

        # ------------------- Step 12: Workflow Tab and Approve -------------------
        with allure.step("Open workflow tab and approve quote"):
            page.locator("[data-test='Q-detail-tab--workflow']").wait_for(state="visible")
            page.locator("[data-test='Q-detail-tab--workflow']").click()
            page.get_by_text("Workflow Submitted by shreyas").wait_for(state="visible")
            expect(page.get_by_text("Workflow Submitted by shreyas")).to_be_visible()
            page.locator(
                ".ucButton.ucButton--hasIcon.ucButton--iconOnly.ucButton--iconOnlyColor-green > .ucButton__inner").wait_for(
                state="visible")
            page.locator(
                ".ucButton.ucButton--hasIcon.ucButton--iconOnly.ucButton--iconOnlyColor-green > .ucButton__inner").click()
            page.get_by_text("Add Approval Reason").wait_for(state="visible")
            page.get_by_role("textbox", name="Reason for your decision").fill("Test")
            page.locator("[data-test='common-approve-button']").wait_for(state="visible")
            page.locator("[data-test='common-approve-button']").click()
            page.get_by_text("Quote has been approved").wait_for(state="visible")
            expect(page.get_by_text("Quote has been approved")).to_be_visible()
            expect(page.get_by_role("button", name="Deal - Approved")).to_be_visible()
            allure.attach(page.screenshot(), name="Quote Approved", attachment_type=allure.attachment_type.PNG)

        browser.close()
