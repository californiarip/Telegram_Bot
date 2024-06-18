import requests
from bs4 import BeautifulSoup

# Dictionary with the links to filtered job searches on hh.kz
urls = {
    # IT JOBS
    'it_analytics': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20'
                    '&ored_clusters=true&professional_role=156&professional_role=10&professional_role=150'
                    '&professional_role=165&professional_role=164&professional_role=157&professional_role=148'
                    '&schedule=remote&search_period=7',

    'it_developer': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20'
                    '&ored_clusters=true&schedule=remote&search_period=7&search_field=name&search_field=company_name'
                    '&search_field=description&professional_role=160&professional_role=124&professional_role=36'
                    '&professional_role=96&professional_role=104&professional_role=112&professional_role=114'
                    '&professional_role=116&professional_role=125&professional_role=113&professional_role=107',

    # EDUCATION
    'education': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20&ored_clusters'
                 '=true&schedule=remote&search_period=7&search_field=name&search_field=company_name&search_field'
                 '=description&professional_role=17&professional_role=23&professional_role=168&professional_role=167'
                 '&professional_role=79&professional_role=101&professional_role=132',

    # MARKETING
    'marketing': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20&ored_clusters'
                 '=true&schedule=remote&search_period=7&search_field=name&search_field=company_name&search_field'
                 '=description&professional_role=140&professional_role=1&professional_role=2&professional_role=3'
                 '&professional_role=10&professional_role=12&professional_role=34&professional_role=37'
                 '&professional_role=55&professional_role=163&professional_role=68&professional_role=70'
                 '&professional_role=71&professional_role=99&professional_role=170',

    # MANAGEMENT
    'management': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20&ored_clusters'
                  '=true&schedule=remote&search_period=7&search_field=name&search_field=company_name&search_field'
                  '=description&professional_role=72&professional_role=74&professional_role=76&professional_role=140'
                  '&professional_role=71&professional_role=75&professional_role=67&professional_role=153'
                  '&professional_role=69&professional_role=158&professional_role=137&professional_role=68'
                  '&professional_role=3&professional_role=2&professional_role=88&professional_role=66'
                  '&professional_role=70&professional_role=73&professional_role=1',

    # FINANCES
    'finances': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20&ored_clusters'
                '=true&professional_role=16&professional_role=154&professional_role=18&professional_role=50'
                '&professional_role=158&professional_role=57&professional_role=155&professional_role=147'
                '&professional_role=134&professional_role=135&professional_role=136&professional_role=137'
                '&professional_role=142&schedule=remote&search_period=7',

    # SALES
    'sales': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20&ored_clusters=true'
             '&schedule=remote&search_period=7&search_field=name&search_field=company_name&search_field=description'
             '&professional_role=6&professional_role=10&professional_role=154&professional_role=51&professional_role'
             '=53&professional_role=54&professional_role=57&professional_role=70&professional_role=71'
             '&professional_role=97&professional_role=105&professional_role=106&professional_role=161'
             '&professional_role=151&professional_role=122&professional_role=129',

    # TECHSUPPORT
    'techsupport_callcenter': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20'
                              '&ored_clusters=true&schedule=remote&search_period=7&search_field=name&search_field'
                              '=company_name'
                              '&search_field=description&professional_role=83',

    'techsupport_': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20'
                    '&ored_clusters=true&professional_role=121&schedule=remote&search_period=7',

    # NO EXPERIENCE
    'no_experience': 'https://hh.kz/search/vacancy?area=40&area=159&enable_snippets=true&items_on_page=20'
                     '&ored_clusters=true&schedule=remote&search_period=7&search_field=name&search_field=company_name'
                     '&search_field=description&experience=noExperience',
}


# Function that collects jobs data and stores it in a list
def fetch_vacancies(category):
    url = urls.get(category)
    if not url:
        return []

    jobs = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f'Failed to fetch URL: {url}')
            break

        soup = BeautifulSoup(response.text, 'lxml')
        job_elements = soup.find_all('div',
                                     class_='serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS '
                                            'vacancy-card_simple--xFe6Vn6pgjyHcFozfcLy')

        for job_element in job_elements:
            job_name = job_element.find('h2')
            company_name = job_element.find('span', class_='company-info-text--vgvZouLtf8jwBmaD1xgp')
            experience = job_element.find('span',
                                          class_='label--rWRLMsbliNlu_OMkM_D3 label_light-gray--naceJW1Byb6XTGCkZtUM')
            more_info = job_element.h2.a['href']

            salary = job_element.find('span',
                                      class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni '
                                             'compensation-text--kTJ0_rp54B2vNeZ3CTt2 '
                                             'separate-line-on-xs--mtby5gO4J0ixtqzW38wh')

            job_info = {
                'job_name': job_name.text.strip() if job_name else 'Не указано',
                'company_name': company_name.text.strip() if company_name else 'Не указано',
                'experience': experience.text.strip() if experience else 'Не указано',
                'salary': salary.text.strip() if salary else 'Не указано',
                'more_info': more_info.strip() if more_info else 'Не указано',
            }
            jobs.append(job_info)

        # Break the loop if 100 jobs found
        if len(jobs) >= 100:
            break

        # Check for the next page link
        next_page = soup.find('a', attrs={'data-qa': 'pager-next'})
        if next_page:
            url = 'https://hh.kz' + next_page['href']
        else:
            break
    return jobs
