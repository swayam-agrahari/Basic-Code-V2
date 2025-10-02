import os
import requests
import argparse
import csv
from collections import Counter

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"

def fetch_github_data(user_or_org):
    url = f"{GITHUB_API_URL}/users/{user_or_org}/repos"
    repos = []
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            repos.extend(response.json())
           
            url = response.links.get('next', {}).get('url', None)
        else:
            print(f"Error fetching data: {response.status_code}")
            break
    return repos

def get_summary_stats(repos, min_stars, filter_language):
    total_stars = 0
    total_forks = 0
    languages = Counter()
    most_active_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)

  
    filtered_repos = []
    for repo in repos:
        if repo['stargazers_count'] >= min_stars:
            if filter_language is None or repo['language'] == filter_language:
                filtered_repos.append(repo)
                total_stars += repo['stargazers_count']
                total_forks += repo['forks_count']
                if repo['language']:
                    languages[repo['language']] += 1

    most_active_repos = filtered_repos[:5]

    return total_stars, total_forks, most_active_repos, languages

def display_results(total_stars, total_forks, most_active_repos, languages):
    print(f"Total Stars: {total_stars}")
    print(f"Total Forks: {total_forks}")
    print("\nTop 5 Most Active Repositories:")
    for repo in most_active_repos:
        print(f"- {repo['name']} ({repo['stargazers_count']} stars, {repo['forks_count']} forks)")

    print("\nLanguages Used Across Repositories:")
    for lang, count in languages.items():
        print(f"- {lang}: {count} repos")

def export_to_csv(filtered_repos, filename):
    fieldnames = ['Name', 'Stars', 'Forks', 'Language', 'URL']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for repo in filtered_repos:
            writer.writerow({
                'Name': repo['name'],
                'Stars': repo['stargazers_count'],
                'Forks': repo['forks_count'],
                'Language': repo['language'] or 'N/A',
                'URL': repo['html_url']
            })
    print(f"Data has been exported to {filename}")

def main():
    parser = argparse.ArgumentParser(description="GitHub Repo Analyzer")
    parser.add_argument('user_or_org', type=str, help="GitHub username or organization name")
    parser.add_argument('--min-stars', type=int, default=0, help="Filter repos by minimum stars")
    parser.add_argument('--language', type=str, help="Filter repos by programming language")
    parser.add_argument('--csv', type=str, help="Export filtered data to a CSV file")
    args = parser.parse_args()


    repos = fetch_github_data(args.user_or_org)


    total_stars, total_forks, most_active_repos, languages = get_summary_stats(
        repos, args.min_stars, args.language
    )

    display_results(total_stars, total_forks, most_active_repos, languages)

    if args.csv:
        export_to_csv(repos, args.csv)

if __name__ == '__main__':
    main()
