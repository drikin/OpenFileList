import sublime, sublime_plugin
import os.path

# Get the views according to the 'list_mode' argument 
# on key bindings file (aka keyboard shorcuts)
def getViews(self, list_mode):
    if list_mode == "active_group":
        views = self.window.views_in_group(self.window.active_group())

    if list_mode == "window":
        views = self.window.views()

    return views

class OpenFileListCommand(sublime_plugin.WindowCommand):
    settings = None
    def run(self, list_mode):
        # Load settings.
        if self.settings == None:
            self.settings = sublime.load_settings("OpenFileList.sublime-settings")

        views = getViews(self, list_mode)

        # Fallback: if current group has no views,
        # then list all views in current window
        if len(views) < 1 and self.settings.get('list_by_window_fallback') == True:
            views = getViews(self, "window")

        names = []
        for view in views:
            name = view.file_name() or view.name() or 'untitled'
            names.append([os.path.basename(name), name])

        def on_done(index):
            if index >= 0:
                self.window.focus_view(views[index])

        self.window.show_quick_panel(names, on_done)
