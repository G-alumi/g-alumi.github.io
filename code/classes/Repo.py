import urllib.request
import json
import re
import datetime
import base64
from classes.GithubCurl import GithubCurl

class Repo:
	def __init__(self, resJson, ghCurl) -> None:
		self.id			= resJson["id"]
		self.name		= resJson["name"]
		self.fullName	= resJson["full_name"]
		self.url		= resJson["html_url"]
		self.thumbnail	= []

		url = "https://api.github.com/repos/" + self.fullName + "/releases"
		with ghCurl.get(url) as res:
			releases = json.loads(res.read())
			self.publish_at = datetime.datetime.fromisoformat(releases[-1]["published_at"].replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=+9)))
			self.update_at = datetime.datetime.fromisoformat(releases[0]["published_at"].replace('Z', '+00:00')).astimezone(datetime.timezone(datetime.timedelta(hours=+9)))

		url = "https://api.github.com/repos/" + self.fullName + "/contents"
		with ghCurl.get(url) as res:
			files = json.loads(res.read())

			for file in files:
				if re.fullmatch(r"thumb.*.png", file["name"], re.IGNORECASE):
					self.thumbnail.append(file["download_url"])
				elif re.fullmatch(r"readme.md", file["name"], re.IGNORECASE):
					with ghCurl.get(file["git_url"]) as res:
						readMe = base64.b64decode(json.loads(res.read())["content"]).decode()
						self.title = re.search(r"^# (.+)$", readMe, re.MULTILINE).group(1)

			
	def getRepos() -> list:
		ghcurl = GithubCurl()
		repos = []
		url = "https://api.github.com/users/g-alumi/repos"
		with ghcurl.get(url) as res:
			body = json.loads(res.read())
			for repo in body:	
				if re.match(r"SimutransPak.+-.+-.+",repo["name"]):
					repos.append(Repo(repo, ghcurl))

		return repos

if __name__ == "__main__":
	repos = Repo.getRepos()
	for repo in repos:
		print(repo.name, repo.publish_at, repo.update_at, repo.thumbnail, repo.title)