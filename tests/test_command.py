import sys
import os

sys.path.append('.')


def test_load_branches():
    from fungit.commands.commands import run_with_git, load_branches
    resp = load_branches()
    print(len(resp))
    for branch in resp:
        print(branch.name, branch.pushables,
              branch.pullables, branch.upstream_name, branch.is_head)


def test_load_commits():
    from fungit.commands.commands import current_head, load_commits
    head = current_head()
    resp = load_commits(head)
    print(len(resp))
    for commit in resp:
        print(commit.sha, commit.msg, commit.author,
              commit.unix_timestamp, commit.status, commit.extra_info, commit.tag, commit.action)


def test_load_files():
    from fungit.commands.commands import run_with_git, load_files
    resp = load_files()
    for file in resp:
        # print(file.name, file.display_str, file.short_status, file.has_staged_change,
        #       file.has_unstaged_change, file.tracked, file.deleted, file.added,
        #       file.has_merged_conflicts, file.has_inline_merged_conflicts)
        print(file.name,  file.has_staged_change, file.has_unstaged_change,)


if __name__ == '__main__':
    test_load_files()
    pass