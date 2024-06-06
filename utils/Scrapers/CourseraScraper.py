import requests
from bs4 import BeautifulSoup


class CourseraScraper:
    def __init__(self):
        self.base_url = "https://www.coursera.org"
        self.search_url = f"{self.base_url}/search"

    def scrape(self, query, language, level, duration):
        params = {'query': query, 'sortBy': 'BEST_MATCH'}

        # Mapa de niveles a la URL de dificultad de Coursera
        level_map = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced'
        }

        # Mapa de duraciones a los parámetros de Coursera
        duration_map = {
            'hours': 'Less%20Than%202%20Hours',
            'days': '1-4%20Weeks',
            'weeks': '1-4%20Weeks',
            'months': '1-3%20Months%2C3-6%20Months%2C6-12%20Months%2C1-4%20Years'
        }

        if language:
            params['language'] = language.capitalize()

        if level:
            params['productDifficultyLevel'] = level_map.get(level, '')

        if duration:
            params['duration'] = duration_map.get(duration, '')

        response = requests.get(self.search_url, params=params)
        soup = BeautifulSoup(response.content, "html.parser")

        cards = soup.find_all("div", {"data-testid": "product-card-cds"})
        courses = []

        for card in cards:
            course_data = self.extract_course_data(card)
            courses.append(course_data)

        return courses

    @staticmethod
    def extract_course_data(card):
        image_element = card.find('img')
        image_url = image_element['src'] if image_element else 'No image found'
        title_element = card.find('a', class_='cds-CommonCard-titleLink')
        title = title_element.text.strip() if title_element else 'No title found'
        course_url = f"https://www.coursera.org{title_element['href']}" if title_element else ''

        body_content_element = card.find('div', class_='cds-CommonCard-bodyContent')
        description_element = body_content_element.find('p') if body_content_element else None
        description = description_element.text.strip() if description_element else ''

        skills_element = body_content_element.find('b', class_='css-14m26ju') if body_content_element else None
        skills = skills_element.next_sibling.strip() if skills_element else ''

        rating_element = card.find('div', class_='css-1vsx0as')
        rating = rating_element.text.strip() if rating_element else ''

        return {
            "Image": image_url,
            "Title": title,
            "Description": skills,
            "Score": rating,
            "CourseLink": course_url
        }
