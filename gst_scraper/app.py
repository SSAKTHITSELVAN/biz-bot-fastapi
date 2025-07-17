from fastapi import FastAPI, Query
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/gst-details")
def get_gst_details(gstin: str = Query(..., min_length=15, max_length=15)):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://www.mastersindia.co/gst-number-search-and-gstin-verification/", timeout=60000)

            # Fill the GSTIN in the input
            page.fill('input[placeholder="XXXAAAYYYYZ01Z5"]', gstin)
            page.click('button:has-text("Search")')

            # Wait for GSTIN profile to appear
            page.wait_for_selector('.RRT__tabs', timeout=15000)

            def extract_text(selector):
                try:
                    return page.inner_text(selector).strip()
                except:
                    return ""

            data = {
                "GSTIN": extract_text('tr:has(th:has-text("GSTIN of the Tax Payer")) td'),
                "Legal Name": extract_text('tr:has(th:has-text("Legal Name of Business")) td'),
                "Principal Place of Business": extract_text('tr:has(th:has-text("Principal Place of Business")) td'),
                "State Jurisdiction": extract_text('tr:has(th:has-text("State Jurisdiction")) td'),
                "Centre Jurisdiction": extract_text('tr:has(th:has-text("Centre Jurisdiction")) td'),
                "Date of Registration": extract_text('tr:has(th:has-text("Date of Registration")) td'),
                "Constitution of Business": extract_text('tr:has(th:has-text("Constitution of Business")) td'),
                "Taxpayer Type": extract_text('tr:has(th:has-text("Taxpayer Type")) td'),
                "GSTIN Status": extract_text('tr:has(th:has-text("GSTIN Status")) td'),
            }

            # Switch to Return Status tab
            # page.click('#tab-1')
            # page.wait_for_selector('#panel-1 table', timeout=10000)

            # rows = page.query_selector_all('#panel-1 table tbody tr')
            # returns = []
            # for row in rows:
            #     cols = row.query_selector_all('td')
            #     if len(cols) >= 7:
            #         returns.append({
            #             "Valid": cols[0].inner_text().strip(),
            #             "Mode of Filing": cols[1].inner_text().strip(),
            #             "Date of Filing": cols[2].inner_text().strip(),
            #             "Return Type": cols[3].inner_text().strip(),
            #             "Return Period": cols[4].inner_text().strip(),
            #             "ARN": cols[5].inner_text().strip(),
            #             "Status": cols[6].inner_text().strip(),
            #         })

            # data["Return Filings"] = returns

            browser.close()
            return JSONResponse(content=data)

        except PlaywrightTimeout:
            browser.close()
            return JSONResponse(content={"error": "Page load or data extraction timed out"}, status_code=504)
        except Exception as e:
            browser.close()
            return JSONResponse(content={"error": str(e)}, status_code=500)
