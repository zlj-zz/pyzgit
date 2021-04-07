import threading

from .box_option import initial_git_box as refresh_all
from .box.navigation_box import GitTypeBox
from .box.git_box import GIT_BOXS
from .box.func_box import DynamicPromptBox
from fungit.shared import GitType
import fungit.commands as git


class Manager:

    @staticmethod
    def switch_box_by_index(idx):
        GitTypeBox.set_current(GIT_BOXS[int(idx) - 1].genre)
        refresh_all()

    @staticmethod
    def prev_box():
        _current = GitTypeBox.current
        _index = index_of(_current, need_box=False)
        _len = len(GIT_BOXS)
        new_index = _len - 1 - (_len - _index) % _len
        GitTypeBox.set_current(GIT_BOXS[new_index].genre)
        refresh_all()

    @staticmethod
    def next_box():
        _current = GitTypeBox.current
        _index = index_of(_current, need_box=False)
        _len = len(GIT_BOXS)
        new_index = (_index + 1) % _len
        GitTypeBox.set_current(GIT_BOXS[new_index].genre)
        refresh_all()

    @staticmethod
    def prev_item():
        _current = GitTypeBox.current
        _, box = index_of(_current)

        if box.selected > 0:
            box.set_selected(box.selected - 1)

    @staticmethod
    def next_item():
        _current = GitTypeBox.current
        _, box = index_of(_current)

        _max_len = len(box.content_orignal) - 1

        if box.selected < _max_len:
            box.set_selected(box.selected + 1)

    @staticmethod
    def space_event():
        _current = GitTypeBox.current
        _, box = index_of(_current)

        if _current & GitType.STATUS:
            box.switch_status()
        else:
            # TODO:
            pass

    @staticmethod
    def a_event():
        _current = GitTypeBox.current
        _, box = index_of(_current)

        if _current & GitType.STATUS:
            box.switch_all()
        else:
            # TODO:
            pass

    @staticmethod
    def pull():
        def _pull_option():
            git.pull()
            DynamicPromptBox.close = True

        t = threading.Thread(target=_pull_option)
        t.setDaemon(True)
        t.start()

        DynamicPromptBox.main('', 'Pulling...')
        refresh_all()
        pass


def index_of(t, need_box: bool = True):
    for idx, sub in enumerate(GIT_BOXS):
        if sub.genre & t:
            if need_box:
                return idx, sub
            return idx