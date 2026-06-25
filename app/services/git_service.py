from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from git import Repo


@dataclass(slots=True)
class GitCloneResult:
    work_dir: Path
    commit_hash: str
    default_branch: str | None
    repo_name: str | None
    repo_owner: str | None


class GitService:
    def clone_repository(self, url: str, branch: str | None = None, shallow: bool = True) -> GitCloneResult:
        temp_dir = Path(tempfile.mkdtemp(prefix="repo-ingest-"))
        clone_kwargs = {"to_path": temp_dir.as_posix(), "depth": 1} if shallow else {"to_path": temp_dir.as_posix()}
        if branch:
            clone_kwargs["branch"] = branch
        try:
            repo = Repo.clone_from(url, **clone_kwargs)
            commit_hash = repo.head.commit.hexsha
            try:
                default_branch = repo.active_branch.name
            except Exception:
                default_branch = branch
            repo_owner = None
            repo_name = None
            if "/" in url:
                parts = url.rstrip("/").split("/")
                repo_name = parts[-1].removesuffix(".git")
                repo_owner = parts[-2] if len(parts) >= 2 else None
            return GitCloneResult(temp_dir, commit_hash, default_branch, repo_name, repo_owner)
        except Exception:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise

    def cleanup(self, work_dir: Path) -> None:
        shutil.rmtree(work_dir, ignore_errors=True)