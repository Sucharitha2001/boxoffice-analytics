from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from database import init_db, insert_collection
from city_scraper import get_all_cities
from movie_scraper import get_movies_for_city
import time

init_db()

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

cities = get_all_cities()

for city in cities:
    print(f"\n📍 Scraping city: {city}")
    try:
        movies = get_movies_for_city(driver, city)
    except Exception as e:
        print(f"⚠️ Failed to get movies for {city}: {e}")
        continue

    for movie_name, language in movies:
        print(f"🎬 Movie: {movie_name}")
        try:
            movie = driver.find_element(By.XPATH, f"//h4[contains(text(), '{movie_name}')]")
            movie.click()
            time.sleep(5)

            showtimes = driver.find_elements(By.CLASS_NAME, "showtime-pill")
            for show in showtimes:
                try:
                    showtime = show.text
                    show.click()
                    time.sleep(5)

                    seats = driver.find_elements(By.CLASS_NAME, "seat")
                    filled_seats = {}
                    ticket_price = {}

                    for seat in seats:
                        seat_type = seat.get_attribute("data-seat-type")
                        price = int(seat.get_attribute("data-price"))
                        status = seat.get_attribute("class")

                        if seat_type not in filled_seats:
                            filled_seats[seat_type] = 0
                            ticket_price[seat_type] = price

                        if "booked" in status:
                            filled_seats[seat_type] += 1

                    estimated_collection = sum(
                        ticket_price[stype] * filled_seats[stype]
                        for stype in filled_seats
                    )

                    insert_collection(city, language, movie_name, "Unknown Theater", showtime, filled_seats, ticket_price, estimated_collection)
                    print(f"✅ {movie_name} @ {showtime}: ₹{estimated_collection:,}")

                    driver.back()
                    time.sleep(3)
                except Exception as e:
                    print(f"⚠️ Error scraping showtime: {e}")
                    continue

            driver.back()
            time.sleep(3)
        except Exception as e:
            print(f"⚠️ Error with movie {movie_name}: {e}")
            continue

driver.quit()
