import sublime, sublime_plugin
import os.path

class OpenFileListCommand(sublime_plugin.WindowCommand):
    def run(self):
        views = self.window.views_in_group(self.window.active_group())
        names = []
        for view in views:
            name = view.file_name() or view.name() or 'untitled'
            names.append([os.path.basename(name), name])

        def on_done(index):
            if index >= 0:
                self.window.focus_view(views[index])

        self.window.show_quick_panel(names, on_done)
