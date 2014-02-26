import re
import sublime
import sublime_plugin
class ConsolewrapCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        cursor = view.sel()[0]
        line_region = view.line(cursor)
        string = view.substr(line_region)
        match = re.search(r"(\s*)", string)
        if match:
            if cursor.empty():
                pos = cursor.begin()
                view.insert(edit, pos, "console.log();")
                view.sel().clear()
                view.sel().add(sublime.Region(pos + 12))
            else:
                var_text = view.substr(cursor)
                inserted_console_template = "\n%sconsole.log('%s ' , %s);"
                if 'source.coffee' in view.scope_name(0):
                  inserted_console_template = "\n%sconsole.log '%s', %s"
                view.insert(edit, line_region.end(), inserted_console_template % (match.group(1), var_text, var_text))
                end = view.line(line_region.end() + 1).end()
                view.sel().clear()
                view.sel().add(sublime.Region(end, end))

class ConsoleremoveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.get_selections();
        cursor = self.view.sel()[0];
        line_region = self.view.line(cursor);
        string = self.view.substr(line_region);
        newstring = re.sub(r"(?m)^((?!//|/\*).)*console\.log.*", '', string);
        self.view.replace(edit, line_region, newstring);
        self.view.sel().clear();

    def get_selections(self):
        selections = self.view.sel();
        has_selections = False;
        for sel in selections:
            if sel.empty() == False:
                has_selections = True;
        if not has_selections:
            full_region = sublime.Region(0, self.view.size());
            selections.add(full_region);
        return selections
