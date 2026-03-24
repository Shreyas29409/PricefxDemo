import allure
from playwright.sync_api import Playwright, sync_playwright, expect

@allure.severity(allure.severity_level.CRITICAL)
@allure.description("End-to-end AutomationDashboard test with full step tracking, Excel export, and screenshots")
def test_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        def screenshot_step(name: str):
            allure.attach(
                page.screenshot(full_page=True),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )

        # Step 1: Navigate to login page
        with allure.step("Navigate to login page"):
            page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fqc%2Fquotes")
            screenshot_step("Login page loaded")

        # Step 2: Enter username
        with allure.step("Fill in username"):
            username_input = page.locator("[data-test=\"username-input\"]")
            username_input.wait_for(state="visible", timeout=30000)
            username_input.fill("shreyas")
            screenshot_step("Username entered")

        # Step 3: Enter password
        with allure.step("Fill in password"):
            password_input = page.locator("[data-test=\"password-input\"]")
            password_input.wait_for(state="visible", timeout=30000)
            password_input.fill("Start123!")
            screenshot_step("Password entered")

        # Step 4: Click login
        with allure.step("Click the login button"):
            login_button = page.locator("[data-test=\"login-loginbutton-button\"]")
            login_button.wait_for(state="visible", timeout=30000)
            login_button.click()
            screenshot_step("Login clicked")

        # Step 5: Navigate to Quotes page
        with allure.step("Navigate to Quotes page"):
            page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/qc/quotes")
            screenshot_step("Quotes page loaded")

        # Step 6: Open dashboards
        with allure.step("Open Dashboards from header"):
            toggle_button = page.locator("[data-test=\"appheader-togglebutton\"]")
            toggle_button.wait_for(state="visible", timeout=30000)
            toggle_button.click()

            dashboards_link = page.get_by_role("link", name="Dashboards")
            dashboards_link.wait_for(state="visible", timeout=30000)
            dashboards_link.click()

            screenshot_step("Dashboards opened")

        # Step 7: Select AutomationDashboard
        with allure.step("Select AutomationDashboard"):
            selector = page.locator(".ant-select-selector")
            selector.wait_for(state="visible", timeout=30000)
            selector.click()

            dashboard_option = page.get_by_text("AutomationDashboard").nth(2)
            dashboard_option.wait_for(state="visible", timeout=30000)
            dashboard_option.click()

            screenshot_step("AutomationDashboard selected")

            with allure.step("Verify AutomationDashboard is visible"):
                dashboard_visible = page.get_by_text("AutomationDashboard").nth(3)
                dashboard_visible.wait_for(state="visible", timeout=30000)
                expect(dashboard_visible).to_be_visible()
                screenshot_step("AutomationDashboard visible")

        # Step 8: Set From Date
        with allure.step("Set From Date to 01-01-2020"):
            from_input = page.locator("[data-test=\"fromdate-input\"]")
            from_input.wait_for(state="visible", timeout=30000)
            from_input.click()

            page.get_by_role("button", name="2020").click()
            page.get_by_text("2020", exact=True).click()
            page.get_by_text("1", exact=True).first.click()

            screenshot_step("From Date set")

            with allure.step("Verify To Date label is visible"):
                to_date_label = page.get_by_text("To Date")
                to_date_label.wait_for(state="visible", timeout=30000)
                expect(to_date_label).to_be_visible()
                screenshot_step("To Date label visible")

        # Step 9: Set To Date
        with allure.step("Set To Date to 31-12-2025"):
            to_input = page.locator("[data-test=\"todate-input\"]")
            to_input.wait_for(state="visible", timeout=30000)
            to_input.click()

            page.get_by_role("button", name="2025").click()
            page.get_by_text("2025", exact=True).click()
            page.get_by_role("table").get_by_text("31", exact=True).click()

            screenshot_step("To Date set")

            with allure.step("Verify Customer label is visible"):
                customer_label = page.get_by_text("Customer", exact=True)
                customer_label.wait_for(state="visible", timeout=30000)
                expect(customer_label).to_be_visible()
                screenshot_step("Customer label visible")

        # ✅ FIXED Step 10
        with allure.step("Filter by Customer CID-00038"):
            cid = page.get_by_text("CID-")
            cid.wait_for(state="visible", timeout=30000)
            cid.click()

            customer_combo = page.locator("[data-test=\"customer-select\"]").get_by_role("combobox")
            customer_combo.wait_for(state="visible", timeout=30000)
            customer_combo.fill("CID-00038")

            cid_option = page.get_by_text("CID-").nth(2)
            cid_option.wait_for(state="visible", timeout=30000)
            cid_option.click()

            screenshot_step("Customer selected")

            with allure.step("Verify Product label is visible"):
                product_label = page.locator("[data-test=\"product-field\"]").get_by_text("Product")
                product_label.wait_for(state="visible", timeout=30000)
                expect(product_label).to_be_visible()
                screenshot_step("Product label visible")

        # ✅ FIXED Step 11
        with allure.step("Filter by Product MB-0060"):
            mb = page.get_by_text("MB-")
            mb.wait_for(state="visible", timeout=30000)
            mb.click()

            product_combo = page.locator("[data-test=\"product-select\"]").get_by_role("combobox")
            product_combo.wait_for(state="visible", timeout=30000)
            product_combo.fill("MB-0060")

            mb_option = page.get_by_text("MB-").nth(2)
            mb_option.wait_for(state="visible", timeout=30000)
            mb_option.click()

            apply_button = page.locator("[data-test=\"unity-dashboard-apply-settings-button\"]")
            apply_button.wait_for(state="visible", timeout=30000)

            screenshot_step("Product selected")

            with allure.step("Verify Apply button is visible"):
                expect(apply_button).to_be_visible()
                screenshot_step("Apply button visible")

        # Step 12: Apply settings
        with allure.step("Click Apply Settings"):
            apply_button.click()
            screenshot_step("Settings applied")

            with allure.step("Verify DashBoard label is visible"):
                dashboard_label = page.get_by_text("DashBoard", exact=True)
                dashboard_label.wait_for(state="visible", timeout=30000)
                expect(dashboard_label).to_be_visible()
                screenshot_step("Dashboard visible")

        # Step 13: Expand dashboard
        with allure.step("Expand dashboard"):
            expand_button = page.locator("[data-test=\"common-expand-button\"]")
            expand_button.wait_for(state="visible", timeout=30000)
            expand_button.click()
            screenshot_step("Dashboard expanded")

        # Step 14: Export to Excel
        with allure.step("Export to Excel"):
            more_button = page.locator("[data-test=\"dashboard-modal\"] [data-test=\"button-menu-more-button\"]")
            more_button.wait_for(state="visible", timeout=30000)
            more_button.click()

            export_button = page.get_by_role("button", name="Export to Excel").nth(1)
            export_button.wait_for(state="visible", timeout=30000)
            export_button.click()

            page.wait_for_timeout(10000)
            screenshot_step("Excel exported")

        # Step 15: Close browser
        with allure.step("Close browser"):
            browser.close()
