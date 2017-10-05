import json
import os
import subprocess
import sys
from pprint import pprint

from github import Github

from repoauth import _token

def main(repo_query):
    """Main function"""
    git = Github(_token)
    repo_search = git.search_repositories("org:WUSTLCSE132 {0}".format(repo_query))
    curr_page = 0
    repo_page = repo_search.get_page(curr_page)
    while repo_page:
        for repo in repo_page:
            if repo.name.find(repo_query) != -1:
                print(repo.name)
        curr_page += 1
        repo_page = repo_search.get_page(curr_page)
        # print(repo.name)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        REPO_QUERY = sys.argv[1]
        main(REPO_QUERY)
    else:
        print("invalid argument")

    # repo.edit(has_wiki=False)
# F = open("repos", "w")



# with open("repos") as data_file:
#     REPOS = json.load(data_file)

# for repo in REPOS:
#     owner = repo["owner"]
#     slug = repo["slug"]
#     print(owner + " " + slug)
#     url = "git@bitbucket.org:" + owner + "/" + slug + ".git"
#     if not os.path.exists(slug):
#         subprocess.call(["git", "clone", url])

# # Clear out media and document files
# subprocess.call("find . -type f -iname *.jpg -delete", shell=True)
# subprocess.call("find . -type f -iname *.png -delete", shell=True)
# subprocess.call("find . -type f -iname *.gif -delete", shell=True)
# subprocess.call("find . -type f -iname *.pdf -delete", shell=True)
# subprocess.call("find . -type f -iname *.mp3 -delete", shell=True)
# subprocess.call("find . -type f -iname *.mp4 -delete", shell=True)
# subprocess.call("find . -type f -iname *.docx -delete", shell=True)
# subprocess.call("find . -type f -iname *.doc -delete", shell=True)
# subprocess.call("find . -type f -iname *.exe -delete", shell=True)
# subprocess.call("find . -type f -iname *.pdb -delete", shell=True)
# subprocess.call("find . -type f -iname *.DS_Store -delete", shell=True)
# subprocess.call("find . -name 'node_modules' -exec rm -r '{}'", shell=True)
# subprocess.call("find . -name '.git' -exec rm -r '{}'", shell=True)
