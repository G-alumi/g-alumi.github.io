from view import BaseView, SimutransAddons, Index
from jinja2 import Environment, FileSystemLoader
from classes import customFilter as filter
import inspect
from classes.Repo import Repo
import json
import os
import datetime

if __name__ == "__main__":

	repos: list[Repo] = []
	repos_json = "./data/repositories.json"
	with open(repos_json, encoding="utf8") as f:
		repos = Repo.generate(json.load(f))

		releases_dir = "./data/releases"
		if os.path.isdir(releases_dir):
			for release_name in os.listdir(releases_dir):
				json_path = os.path.join(releases_dir, release_name)
				with open(os.path.join(releases_dir, release_name), encoding="utf8") as f2:
					release = Repo(json.load(f2))
					for i, repo in enumerate(repos):
						if repo.name == release.name:
							for j, update in enumerate(repo.updates):
								if update.tag != release.updates[0].tag and update.date + datetime.timedelta(days=365) >= datetime.date.today():
									release.updates.append(update)
							repos[i] = release
						else:
							for j, update in enumerate(repo.updates):
								if j != 0 and update.date + datetime.timedelta(days=365) < datetime.date.today():
									del repo.updates[j]

							repo.updates.sort(key=lambda x:x.date, reverse=True)
				os.remove(json_path)
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