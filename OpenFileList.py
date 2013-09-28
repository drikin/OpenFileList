import sublime, sublime_plugin
import os.path

class OpenFileListCommand(sublime_plugin.WindowCommand):
    def run(self):
        views = self.window.views_in_group(self.window.active_group())
        (_, current) = self.window.get_view_index(self.window.active_view())
        names = []
        for view in views:
            name = view.file_name() or view.name() or 'untitled'
            names.append([os.path.basename(name),
                name.replace(sublime.active_window().folders()[0] + '/', '')])

        def on_done(index):
            if index >= 0:
                self.window.focus_view(views[index])
            else:
                self.window.focus_view(views[current])

        if int(sublime.version()) > 3000:
            self.window.show_quick_panel(names, on_done, sublime.MONOSPACE_FONT, current, on_done)
        else:
            self.window.show_quick_panel(names, on_done)