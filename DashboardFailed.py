import allure
from playwright.sync_api import sync_playwright, expect

@allure.severity(allure.severity_level.CRITICAL)
@allure.description("Failure at Customer selection with stable execution")
def test_dashboardfailed():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        try:
            # Step 1: Login page
            with allure.step("Navigate to login page"):
                page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/login?redirect_url=%2Fqc%2Fquotes")

            # Step 2: Login
            with allure.step("Login"):
                page.locator("[data-test='username-input']").fill("shreyas")
                page.locator("[data-test='password-input']").fill("Start123!")
                page.locator("[data-test='login-loginbutton-button']").click()

            # Step 3: Quotes page
            with allure.step("Go to Quotes"):
                page.goto("https://demo.pricefx.com/app/?partition=demofx_experis#/qc/quotes")

            # Step 4: Open dashboards
            with allure.step("Open Dashboards"):
                page.locator("[data-test='appheader-togglebutton']").click()
                page.get_by_role("link", name="Dashboards").click()

            # Step 5: Select dashboard
            with allure.step("Select AutomationDashboard"):
                page.locator(".ant-select-selector").click()
                page.get_by_text("AutomationDashboard").nth(2).click()
                expect(page.get_by_text("AutomationDashboard").nth(3)).to_be_visible()

            # ✅ Step 6: BYPASS DATE PICKER (NO FAIL HERE)
            with allure.step("Set dates using JS (stable)"):
                page.evaluate("""
                    document.querySelector('[data-test="fromdate-input"]').value = '01/01/2020';
                    document.querySelector('[data-test="todate-input"]').value = '31/12/2025';
                """)

                expect(page.get_by_text("Customer", exact=True)).to_be_visible()

            # ❌ Step 7: INTENTIONAL FAILURE (NOW GUARANTEED)
            with allure.step("Fail at Customer selection"):
                cid = page.get_by_text("CID-")
                cid.wait_for(state="visible")
                cid.click()

                customer_combo = page.locator("[data-test='customer-select']").get_by_role("combobox")
                customer_combo.wait_for(state="visible")

                customer_combo.fill("CID-000")  # wrong value

                # 🔥 FORCE FAILURE HERE (no waiting for UI)
                assert customer_combo.input_value() == "CID-00038", "Customer selection failed!"

        except Exception as e:
            # 📸 Screenshot ONLY on failure
            allure.attach(
                page.screenshot(full_page=True),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise e

        finally:
            browser.close()
