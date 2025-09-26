from view import BaseView, SimutransAddons, Index
from jinja2 import Environment, FileSystemLoader
from classes import customFilter as filter
import inspect
from classes.Repo import Repo
import json
import os
import datetime
import re
import shutil

if __name__ == "__main__":

	repos: list[Repo] = []
	repos_json = "./data/repositories.json"
	with open(repos_json, encoding="utf8") as f:
		repos = Repo.generate(json.load(f))

	WORK_DIR = "./data/work"
	REPO_FILE = os.path.join(WORK_DIR, "repo.json")
	REPO2_FILE = os.path.join(WORK_DIR, "repo2.json")
	RELEASE_FILE = os.path.join(WORK_DIR, "release.json")
	if os.path.exists(REPO_FILE) and os.path.exists(RELEASE_FILE) and os.path.exists(REPO2_FILE):
		load_repo = None
		load_repo2 = None
		load_release = None
		with open(REPO_FILE, encoding="utf8") as f:
			load_repo:dict[str,str] = json.load(f)

		with open(REPO2_FILE, encoding="utf8") as f:
			load_repo2:dict[str,str] = json.load(f)
		
		with open(RELEASE_FILE, encoding="utf8") as f:
			load_release:dict[str,str] = json.load(f)
			
		shutil.rmtree(WORK_DIR)
		isExists = False
		for repo in repos:
			updates: list[Repo.Update] = []
			if repo.repo == load_repo["nameWithOwner"]:
				isExists = True
				release_description = ""
				release_description_lines = load_release["body"].strip().splitlines()
				for line in release_description_lines:
					if not ("詳しくは" in line and "readme" in line.lower()) :
						release_description += line
						release_description += "\n"

				updates.append(Repo.Update({
					"tag":  		load_release["tagName"],
					"date":  		datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d"),
					"description":  release_description,
				}))

				repo.name = re.sub('\(.*?\)$', '', load_repo["description"].strip()).strip()
				repo.description = load_repo2["description"].strip()
				
			for upd_i, update in enumerate(repo.updates):
				# !(更新のrepo & 更新のタグ) | 最新の更新 | 1年以内の更新
				if (
					not(repo.name == load_repo["nameWithOwner"]and update.tag == load_release["tagName"]) or
					upd_i == 0 or
					update.date + datetime.timedelta(days=365) >= datetime.date.today()
				):
					updates.append(update)

			updates.sort(key=lambda x:x.date, reverse=True)
			repo.updates = updates
		
		if not isExists:
			release_description = ""
			release_description_lines = load_release["body"].strip().splitlines()
			for line in release_description_lines:
				if not ("詳しくは" in line and "readme" in line.lower()) :
					release_description += line
					release_description += "\n"

			repo = Repo({
				"repo": load_repo["nameWithOwner"],
				"name": re.sub('\(.*?\)$', '', load_repo["description"].strip()).strip(),
				"description": load_repo2["description"],
				"thumbnails": load_repo2["thumbnails"],
				"updates": [{
					"tag":  		load_release["tagName"],
					"date":  		datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime("%Y-%m-%d"),
					"description":  release_description,
				}],
			})
			repos.append(repo)

		repos.sort(key=lambda x:x.updates[0].date, reverse=True)

	with open(repos_json, "w", encoding="utf8") as f:
		json.dump([r.getDict() for r in repos], f, indent=2, ensure_ascii=False)


	# 生成するページのリスト
	pages: list[tuple[BaseView.BaseView, str]] = [
		(SimutransAddons.SimutransAddons, "simutrans_addons.html"),
		(Index.Index, "index.html"),
	]

	# jinja2に自作関数を登録
	env = Environment(loader=FileSystemLoader("./templates", encoding="utf8"))
	for func in inspect.getmembers(filter, inspect.isfunction):
		env.filters[func[0]] = func[1]
	
	params = {}
	params["addons"] = repos

	for view, name in pages:
		page = view()
		page.set_param(params)
		with open(name, "w", encoding="utf8") as f:
			f.write(page.render(env))