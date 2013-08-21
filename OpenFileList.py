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

        # Get the views:
        views = getViews(self, list_mode)

        # Fallback: if current group has no views,
        # then list all views in current window
        if len(views) < 1 and self.settings.get('list_by_window_fallback') == True:
            views = getViews(self, "window")

        names = []
        current_index = False
        i = -1
        for view in views:
            i += 1
            view_path = view.file_name() or view.name() or 'untitled'
            view_name = os.path.basename(view_path)

            # If the view id = current view id,
            # then save the index of current view:
            if view.id() == self.window.active_view().id():
                current_index = i

            if view.is_dirty():
                view_name += " " + self.settings.get('mark_dirty_file_char')

            names.append([view_name, view_path])

        # Delete current view from arrays:
        if current_index is not False and self.settings.get('skip_current_file') == True:
            del views[current_index]
            del names[current_index]
        else:
            names[current_index][0] = self.settings.get('mark_current_file_char') + " " + names[current_index][0]
 
        def on_done(index):
            if index >= 0:
                self.window.focus_view(views[index])

        self.window.show_quick_panel(names, on_done)
