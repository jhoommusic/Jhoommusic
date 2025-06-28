import asyncio
import shlex
from typing import Tuple

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

import config


def install_req(cmd: str) -> Tuple[str, str, int, int]:
    async def install_requirements():
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    return asyncio.get_event_loop().run_until_complete(install_requirements())


def git():
    REPO_LINK = config.GITHUB_REPO
    if config.GIT_TOKEN:
        GIT_USERNAME = REPO_LINK.split("com/")[1].split("/")[0]
        TEMP_REPO = REPO_LINK.split("https://")[1]
        UPSTREAM_REPO = f"https://{config.GIT_TOKEN}@{TEMP_REPO}"
    else:
        UPSTREAM_REPO = REPO_LINK
    try:
        repo = Repo()
        LOGGER(__name__).info(f"Git Client Found")
    except GitCommandError:
        LOGGER(__name__).warning(f"Invalid Git Command")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "origin" in repo.remotes:
            origin = repo.remote("origin")
        else:
            origin = repo.create_remote("origin", UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(
            config.UPSTREAM_BRANCH,
            origin.refs[config.UPSTREAM_BRANCH],
        )
        repo.heads[config.UPSTREAM_BRANCH].set_tracking_branch(
            origin.refs[config.UPSTREAM_BRANCH]
        )
        repo.heads[config.UPSTREAM_BRANCH].checkout(True)
        try:
            repo.create_remote("origin", config.UPSTREAM_REPO)
        except BaseException:
            pass
        nrs = repo.remote("origin").refs
        if config.UPSTREAM_BRANCH in nrs:
            repo.remote("origin").refs[config.UPSTREAM_BRANCH].checkout()
        else:
            repo.git.checkout("-b", config.UPSTREAM_BRANCH)
        LOGGER(__name__).info(f"Initialized Git Repository")
    except NoSuchPathError:
        LOGGER(__name__).error(f"Directory {os.getcwd()} does not seems to be a git repository")