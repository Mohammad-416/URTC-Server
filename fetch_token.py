from playwright.sync_api import sync_playwright

EMAIL = "m9971359949@gmail.com"

def fetch_next_action_token():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Intercept requests
        next_action_token = []

        def handle_request(request):
            nonlocal next_action_token
            if request.method == "POST" and "login" in request.url:
                headers = request.headers
                if "next-action" in headers:
                    next_action_token.append(headers["next-action"])

        page.on("request", handle_request)

        # Go to the login page
        page.goto("https://login.unity.com/en/sign-in")
        page.wait_for_timeout(3000)

        # Fill email and click Continue
        page.fill("#email", EMAIL)  # updated selector
        page.click("button[type='submit']")


        # Wait for requests to be made
        page.wait_for_timeout(5000)

        browser.close()

        if not next_action_token:
            raise Exception("Next-Action token not found.")

        return next_action_token[-2]

# Run it
def fetch_token():
    token = fetch_next_action_token()
    print("Next-Action Token:", token)
    return token