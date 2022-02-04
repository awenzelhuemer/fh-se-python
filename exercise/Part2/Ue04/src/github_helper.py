import re

import requests
from bs4 import BeautifulSoup

github_base_url = "https://github.com"


def get_github_members(url: str):
    url = f"{url.replace('github.com', 'github.com/orgs')}/people"
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc.select('a[id*="member-"]')


def get_github_repositories(url: str):
    page = 0
    all_repositories = []
    url = f"{url.replace(github_base_url, github_base_url + '/orgs')}/repositories"
    while True:
        page = page + 1
        paged_url = f"{url}?page={page}"
        response = requests.get(paged_url)
        doc = BeautifulSoup(response.text, 'html.parser')
        repository_tags = doc.find("div", {"id": "org-repositories"}).find_all("li")
        repository_count = len(repository_tags)
        if repository_count == 0:
            break
        for repo in repository_tags:
            repository = f'{github_base_url}{repo.find("a")["href"]}'
            all_repositories.append(repository)

    return all_repositories


def get_github_title_and_languages(url: str):
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    page_content = doc.find('main')
    title = doc.find('a', {'class': 'Header-link'}).text
    all_language_tags = page_content.find('h4', text="Top languages").parent.find_all('span', {'itemprop': 'programmingLanguage'})
    languages = [tag.text for tag in all_language_tags]
    return title, languages


def extract_github_data(url: str):
    title, all_languages = get_github_title_and_languages(url)
    members = get_github_members(url)
    repositories = get_github_repositories(url)

    repository_data = []

    for repo in repositories:
        response = requests.get(f"{github_base_url}{repo}")
        content = BeautifulSoup(response.text, 'html.parser')

        repository_name = repo.removeprefix('/')

        aboutbox = content.find("h2", text='About').findParent()
        description_info = aboutbox.find('p', {'class': 'f4'})
        if description_info is not None:
            description = description_info.text.strip()
        else:
            description = None

        # Values from infobox
        infobox_numbers = aboutbox.findAll('strong')
        stars = infobox_numbers[0].text.strip()
        watchers = infobox_numbers[1].text.strip()
        forks = infobox_numbers[2].text.strip()

        branches_and_tags = content.find('span', {'class': 'color-fg-muted'}, text=re.compile("branch(es)?")).parent.parent.findAll(
            "strong")
        branches = branches_and_tags[0].text
        tags = branches_and_tags[1].text

        languages_title_tag = content.find("h2", {"class": "h4"}, text="Languages")
        languages = []
        if languages_title_tag is not None:
            for language_item in languages_title_tag.parent.findAll("li"):
                language_spans = language_item.findAll('span')
                language = f"{language_spans[0].text}: {language_spans[1].text}"
                languages.append(language)

        last_updated_tag = content.find("relative-time")
        if last_updated_tag is not None:
            last_updated = last_updated_tag.text
        else:
            last_updated = None

        topics = []
        for topic_tag in content.findAll('a', {'class': 'topic-tag-link'}):
            topics.append(topic_tag.text.strip())

        repository_data.append({
            "name": repository_name,
            "description": description,
            "topics": topics,
            "languages": languages,
            "last_updated": last_updated,
            "watchers": watchers,
            "forks": forks,
            "stars": stars,
            "branches": branches,
            "tags": tags
        })

    return {
        "title": title,
        "member_count": len(members),
        "languages": all_languages,
        "repositories": repository_data
    }


def is_valid_github_url(url):
    try:
        if not re.match(f'^{github_base_url}/*', url):
            raise ValueError('Url is invalid.')

        response = requests.get(url)

        if not response.ok:
            raise ValueError('Invalid response')

        return True
    except Exception as ex:
        print(f"Exception: {ex}")
        return False
