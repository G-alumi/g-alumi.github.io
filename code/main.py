from classes.Repo import Repo
import datetime
import os
import sys
from classes.GithubCurl import GithubCurl

if __name__ == "__main__":
	args = sys.argv
	token = args[1]
	GithubCurl.setToken(token)

	dirname = os.path.dirname(__file__)

	base_html = ''
	with open(os.path.join(dirname, 'html', 'index_base.html'), 'r', encoding='UTF-8') as f:
		base_html = f.read()

	repos = Repo.getRepos()
	repos = sorted(repos, key=lambda x: (x.publish_at, x.update_at), reverse=True)
	repo_template = ''
	repos_html = ''

	with open(os.path.join(dirname, 'html', 'repo.html'), 'r', encoding='UTF-8') as f:
		repo_template = f.read()

	isFirst = True
	for repo in repos:
		if not(isFirst):
			repos_html += '	<hr class="addon_separate">\n'
		isFirst = False

		thumbnails = ''
		for thumbnail in repo.thumbnail:
			thumbnails += '\n				<img src="'+ thumbnail +'" alt="">'

		publish = ''
		if repo.publish_at + datetime.timedelta(days=7) > datetime.datetime.now(datetime.timezone.utc):
			publish = '<div class="new">'+ repo.publish_at.strftime('%Y/%m/%d') +' 公開</div>'
		else:
			publish = '<div>'+ repo.publish_at.strftime('%Y/%m/%d') +' 公開</div>'
		
		update = ''
		if repo.publish_at != repo.update_at:
			if repo.update_at + datetime.timedelta(days=7) > datetime.datetime.now(datetime.timezone.utc):
				update = '<div class="update">'+ repo.update_at.strftime('%Y/%m/%d') +' 更新</div>'
			else:
				update = '<div>'+ repo.update_at.strftime('%Y/%m/%d') +' 更新</div>'
		
		replace = {
			"title"			: repo.title,
			"fullName"		: repo.fullName,
			"thumbnail_0"	: repo.thumbnail[0] if repo.thumbnail else "",
			"thumbnails"	: thumbnails,
			"publish"		: publish,
			"update"		: update,
		}

		repos_html += repo_template.format(**replace)
	
	res_html = base_html.format(repos=repos_html)
	with open('index.html', 'w', encoding='UTF-8') as f:
		f.write(res_html)