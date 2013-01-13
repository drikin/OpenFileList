import sublime, sublime_plugin
import os.path

class OpenFileListCommand(sublime_plugin.WindowCommand):
    def run(self):
        group_id = self.window.active_group()
        views = self.window.views_in_group(group_id)
        names = []
        for view in views:
            name = view.file_name()
            if not name:
                name = view.name()
            names.append([os.path.basename(name)])
        self.window.show_quick_panel(names, self.on_done)

    def on_done(self, index):
        if index >= 0:
            group_id = self.window.active_group()
            views = self.window.views_in_group(group_id)
            self.window.focus_view(views[index])

    def is_enabled(self):
        return self.window.active_view() != None
