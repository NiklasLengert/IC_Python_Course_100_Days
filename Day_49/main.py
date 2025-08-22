from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

USER_EMAIL = os.getenv("ACCOUNT_EMAIL")
USER_PASS = os.getenv("ACCOUNT_PASSWORD")
SITE_URL = os.getenv("GYM_URL")

browser_options = webdriver.ChromeOptions()
browser_options.add_experimental_option("detach", True)
profile_path = os.path.join(os.getcwd(), "chrome_profile")
browser_options.add_argument(f"--user-data-dir={profile_path}")
browser = webdriver.Chrome(options=browser_options)
browser.get(SITE_URL)

waiter = WebDriverWait(browser, 2)

browser.get(SITE_URL)

def attempt_action(action, max_attempts=7, action_name=None):
    for attempt in range(max_attempts):
        print(f"Trying {action_name}. Attempt: {attempt + 1}")
        try:
            return action()
        except TimeoutException:
            if attempt == max_attempts - 1:
                raise
            time.sleep(1)

def authenticate():
    signin_btn = waiter.until(ec.element_to_be_clickable((By.ID, "login-button")))
    signin_btn.click()

    email_field = waiter.until(ec.presence_of_element_located((By.ID, "email-input")))
    email_field.clear()
    email_field.send_keys(USER_EMAIL)

    pass_field = browser.find_element(By.ID, "password-input")
    pass_field.clear()
    pass_field.send_keys(USER_PASS)

    signin_submit = browser.find_element(By.ID, "submit-button")
    signin_submit.click()

    waiter.until(ec.presence_of_element_located((By.ID, "schedule-page")))

def reserve_class(reserve_btn):
    reserve_btn.click()
    waiter.until(lambda d: reserve_btn.text == "Booked")

attempt_action(authenticate, action_name="login")

workout_cards = browser.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
new_bookings = 0
new_waitlists = 0
existing_bookings = 0
class_list = []

for workout in workout_cards:
    parent_group = workout.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    weekday = parent_group.find_element(By.TAG_NAME, "h2").text

    is_target_day = "Tue" in weekday or "Thu" in weekday
    if is_target_day:
        session_time = workout.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        is_evening_class = "6:00 PM" in session_time
        if is_evening_class:
            workout_name = workout.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            action_btn = workout.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            session_details = f"{workout_name} on {weekday}"

            btn_state = action_btn.text
            if btn_state == "Booked":
                print(f"✓ Already booked: {session_details}")
                existing_bookings += 1
                class_list.append(f"[Booked] {session_details}")
            elif btn_state == "Waitlisted":
                print(f"✓ Already on waitlist: {session_details}")
                existing_bookings += 1
                class_list.append(f"[Waitlisted] {session_details}")
            elif btn_state == "Book Class":
                attempt_action(lambda: reserve_class(action_btn), action_name="Booking")
                print(f"✓ Successfully booked: {session_details}")
                new_bookings += 1
                class_list.append(f"[New Booking] {session_details}")
                time.sleep(0.5)
            elif btn_state == "Join Waitlist":
                attempt_action(lambda: reserve_class(action_btn), action_name="Waitlisting")
                print(f"✓ Joined waitlist for: {session_details}")
                new_waitlists += 1
                class_list.append(f"[New Waitlist] {session_details}")
                time.sleep(0.5)

total_sessions = existing_bookings + new_bookings + new_waitlists
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_sessions} ---")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

def fetch_booking_cards():
    bookings_nav = waiter.until(ec.element_to_be_clickable((By.ID, "my-bookings-link")))
    bookings_nav.click()
    waiter.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

    booking_cards = browser.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

    if len(booking_cards) == 0:
        raise TimeoutException("No booking cards found - page may not have loaded")
    return booking_cards

booking_elements = attempt_action(fetch_booking_cards, action_name="Get my bookings")

confirmed_sessions = 0

for booking_card in booking_elements:
    try:
        time_info = booking_card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
        schedule_text = time_info.text

        matches_criteria = ("Tue" in schedule_text or "Thu" in schedule_text) and "6:00 PM" in schedule_text
        if matches_criteria:
            session_title = booking_card.find_element(By.TAG_NAME, "h3").text
            print(f"  ✓ Verified: {session_title}")
            confirmed_sessions += 1
    except NoSuchElementException:
        pass

print(f"\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_sessions} bookings")
print(f"Found: {confirmed_sessions} bookings")

success_condition = total_sessions == confirmed_sessions
if success_condition:
    print("SUCCESS: All bookings verified!")
else:
    print(f"MISMATCH: Missing {total_sessions - confirmed_sessions} bookings")