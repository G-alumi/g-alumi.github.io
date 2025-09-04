from view.BaseView import BaseView
import os
from classes.Repo import Repo
import datetime

class Index(BaseView):

	def execute(self):
		header_img = os.listdir("src/img/header/")

		updates = []
		addon :Repo
		for addon in self.params["addons"]:
			for update in addon.updates:
				if update.date + datetime.timedelta(days=365) >= datetime.date.today():
					updates.append({
						"date":		update.date,
						"name":		addon.name,
						"repo":		addon.getRelease(),
						"version":	update.tag,
					})
		updates.sort(key=lambda x:x["date"], reverse=True)
		
		self.tpl_assign("updates", updates)
		self.tpl_assign("header_img", header_img)
