'''
    вакансии на hh.ru:
        адрес страницы: https://spb.hh.ru/search/vacancy?text=python&area=1&area=2

    вакансии на hh.ru в USD:
        адрес страницы: https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&currency_code=USD&text=python&enable_snippets=false

    список вакансий:
        тег для спиков вакансий: "div" id="a11y-main-content"

    вакансия:
        тег для вакансий: "div" class_="serp-item"

    заголовок и ссылка:
        заголовок вакансии: "h3" class_="bloko-header-section-3"
        текст заголовка вакансии: "span" class_="serp-item__title"
        ссылка на вакансию: "a" class_="bloko-link"

    зарплата:
        тег с текстом заплаты: "span" class_="bloko-header-section-2"
        текст зарплаты: "span" class_="bloko-header-section-2 bloko-header-section-2_lite"

    работадатель:
        инфо работадателя: "span" class_="vacancy-company-name"
        текст работадателя: "span" class_="bloko-header-section-2 bloko-header-section-2_lite"

    город вакансии:
        текст города: "div" class_="bloko-text"

'''



import requests
import fake_headers
from bs4 import BeautifulSoup
import json

def gen_headers() -> dict:
    headers_gen = fake_headers.Headers(os="win", browser="chrome")
    return headers_gen.generate()

url = "https://spb.hh.ru/search/vacancy?text=python%2C+Django%2C+flask&salary=&currency_code=USD&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line"

def requests_hh(gen_headers, url):
    response = requests.get(url, headers=gen_headers())
    response_text = response.text

    soup = BeautifulSoup(response_text, "lxml")

    vacancy_list = soup.find("div", id="a11y-main-content")
    return vacancy_list

vacancy_list = requests_hh(gen_headers, url)
vacancy_list_json = []

def main_hh(gen_headers, vacancy_list, vacancy_list_json):
    for vacancy_list_tag in vacancy_list.find_all("div", class_="serp-item"):
        h3_tag = vacancy_list_tag.find("span", attrs={"data-qa":"serp-item__title"})
        a_tag = vacancy_list_tag.find("a", class_="bloko-link")

        h3_tag_text = h3_tag.text.strip()
        link_a_tag_absolute = a_tag["href"]
    # print(h3_tag_text, link_a_tag_absolute)

        salary_tag = vacancy_list_tag.find("span", class_="bloko-header-section-2")
        if salary_tag is None:
            salary_tag_text = "зарплата не указана"
        else:
            salary_tag_text = salary_tag.text.strip()
    # print(salary_tag_text)

        company_tag = vacancy_list_tag.find("div", class_="vacancy-serp-item__meta-info-company")
        if company_tag is None:
            company_tag_text = "работадатель не указан"
        else:
            company_tag_text = company_tag.text.strip()
    # print(company_tag_text)

        city_tag = vacancy_list_tag.find(attrs={"data-qa": "vacancy-serp__vacancy-address"})
        city_tag_text = city_tag.text.strip()
    # print(city_tag.text.strip())


        vacancy_list_json.append(
        {
            "header": h3_tag_text,
            "link": link_a_tag_absolute,
            "salary": salary_tag_text,
            "company": company_tag_text,
            "city": city_tag_text
        }
    )
    # print(vacancy_list_json)
        with open("json/job.json", "w", encoding='utf-8') as f:
            json.dump(vacancy_list_json, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main_hh(gen_headers, vacancy_list, vacancy_list_json)