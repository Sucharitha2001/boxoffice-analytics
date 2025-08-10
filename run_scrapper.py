# run_all_scrapers.py

from city_scraper import get_cities
from movie_scraper import get_movies_for_city
from seat_scraper import get_seat_data
from database import insert_collection

def run_scrape():
    cities = get_cities()
    print(f"Found {len(cities)} cities.")

    for city in cities:
        print(f"\n📍 Scraping movies for city: {city}")
        movies = get_movies_for_city(city)

        for movie in movies:
            print(f"🎬 Movie: {movie['name']} ({movie['language']})")

            seat_data_list = get_seat_data(city, movie['name'])

            for seat_data in seat_data_list:
                insert_collection(
                    city=city,
                    language=movie['language'],
                    movie_name=movie['name'],
                    theater=seat_data['theater'],
                    showtime=seat_data['showtime'],
                    seat_breakdown=seat_data['seat_breakdown'],
                    ticket_prices=seat_data['ticket_prices'],
                    estimated_collection=seat_data['estimated_collection']
                )
                print(f"✅ Inserted showtime: {seat_data['showtime']} at {seat_data['theater']}")
