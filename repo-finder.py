import requests

def search_repos(stars, tolerance=0):
    if stars > 400000:
        query = "stars:>0"
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=1" #stupid pagination
    else:
        min_stars = stars - tolerance
        max_stars = stars + tolerance
        query = f"stars:{min_stars}..{max_stars}"
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['total_count'] == 0:
            return None
        return data['items']
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return None

def main():
    stars = int(input("Enter the number of stars: "))
    
    if stars > 400000:
        repos = search_repos(stars)
        repo = repos[0]
        print(f"That's too many! The closest repo is: Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}, Description: {repo['description']}")
    else:
        # First search for the exact number of stars
        repos = search_repos(stars)
        
        if repos:
            print(f"Found {len(repos)} repositories with {stars} stars:")
            for repo in repos:
                print(f"Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}, Description: {repo['description']}")
        else:
            print(f"No repositories found with {stars} stars.")
            expand_search = input("Would you like to expand the search by ±10 stars? (y/n): ").lower()
            if expand_search == 'y':
                repos = search_repos(stars, 10)
                if repos:
                    print(f"Found {len(repos)} repositories with {stars} ±10 stars:")
                    for repo in repos:
                        print(f"Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}, Description: {repo['description']}")
                else:
                    expand_search_more = input("No repositories found. Would you like to expand the search by ±100 stars? (y/n): ").lower()
                    if expand_search_more == 'y':
                        repos = search_repos(stars, 100)
                        if repos:
                            print(f"Found {len(repos)} repositories with {stars} ±100 stars:")
                            for repo in repos:
                                print(f"Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}, Description: {repo['description']}")
                        else:
                            expand_search_even_more = input("No repositories found. Would you like to expand the search by ±1,000 stars? (y/n): ").lower()
                            if expand_search_even_more == 'y':
                                repos = search_repos(stars, 1000)
                                if repos:
                                    print(f"Found {len(repos)} repositories with {stars} ±1,000 stars:")
                                    for repo in repos:
                                        print(f"Name: {repo['name']}, Stars: {repo['stargazers_count']}, URL: {repo['html_url']}, Description: {repo['description']}")
                                else:
                                    print("No repositories found with the expanded search criteria.")
                            else:
                                print("Search terminated.")
                    else:
                        print("Search terminated.")
            else:
                print("Search terminated.")

if __name__ == "__main__":
    main()
3579