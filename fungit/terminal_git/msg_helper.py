import logging

from fungit.commands.exec import run_cmd_with_resp
from .gitoptions import GIT_OPTIONS
from .shared import echo, warn, err, exit_, CommandColor, Fx


LOG = logging.getLogger()


def echo_one_help_msg(k: str):
    echo("    " + k, color=CommandColor.GREEN, nl=False)
    if GIT_OPTIONS[k]["help-msg"]:
        msg = GIT_OPTIONS[k]["help-msg"]
    else:
        msg = GIT_OPTIONS[k]["command"]
    echo((9 - len(k)) * " " + str(msg))


def echo_help_msg(keys: list):
    echo("Usage: g <option> [<args>]\n", style=Fx.b)
    # echo('')
    if keys:
        invalid_keys = []
        for k in keys:
            if GIT_OPTIONS.get(k):
                echo_one_help_msg(k)
            else:
                invalid_keys.append(k)
        if invalid_keys:
            echo("\nDon't support these options: ", nl=False)
            echo(" ".join(invalid_keys), color=CommandColor.RED)
    else:
        echo(
            """
-h / --help [<args>]  :get help mesage, default is all.
                       You can also follow the parameters to
                       get help information for specific commands.

--complete            :You can use this option to get shell auto completion.
                       Just support `bash`, `zsh`.
        """
        )
        echo("These are short commands that can replace git operations:")
        for k in GIT_OPTIONS.keys():
            echo_one_help_msg(k)


def give_tip(c: str):
    err(f"Don't support option: {c}")
    echo("\nMaybe what you want is:")
    c = c[0]
    for k in GIT_OPTIONS.keys():
        if k.startswith(c):
            echo_one_help_msg(k)


def echo_description():
    from .. import __version__

    has_git = False
    try:
        err, git_version = run_cmd_with_resp("git --version")
        if git_version:
            has_git = True
        else:
            exit_(1, err)
    except Exception:
        LOG.warning("Happen error when run command with get Git version")
        git_version = ""

    echo("[fungit] version: %s" % __version__, style=Fx.b)
    echo(git_version)
    echo("Description:", style=Fx.b)
    echo(
        "Fungit terminal tool, help you use git more simple. Support Linux and MacOS.\n",
        style=Fx.underline,
    )

    echo("Usage: g <option> [<args>]", style=Fx.b)
    echo("You can use ", nl=False)
    echo("-h", color=CommandColor.GREEN, nl=False)
    echo(" and ", nl=False)
    echo("--help", color=CommandColor.GREEN, nl=False)
    echo(" to get how to use command fungit.\n")

    if not has_git:
        warn("Don't found Git, maybe need install.")
