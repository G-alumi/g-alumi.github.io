from view.BaseView import BaseView


class SimutransAddons(BaseView):
	
	def execute(self):
		self.tpl_assign("title", "simutrans addons")
		self.tpl_assign("addons", self.params["addons"])