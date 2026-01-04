"""Core deployment logic for HCA CLI."""

import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import CLAUDE_DIR, COMPONENTS, METADATA_DIR, METADATA_FILE
from .git_ops import GitOps


class DeployMode(Enum):
    """Deployment mode for handling existing files."""

    OVERWRITE = "overwrite"  # Remove existing and replace completely
    MERGE = "merge"  # Merge with existing, preserving user additions


class Deployer:
    """Handle deployment of .claude configurations."""

    def __init__(
        self, source: str, branch: str = "main", verbose: bool = False
    ) -> None:
        """Initialize deployer.

        Args:
            source: Source repository URL or local path
            branch: Branch to use for remote repositories
            verbose: Enable verbose output
        """
        self.source = source
        self.branch = branch
        self.verbose = verbose
        self.git_ops = GitOps()
        self._temp_dir: Optional[str] = None
        self._manifest: Optional[Dict] = None

    def get_manifest(self) -> Dict[str, List[str]]:
        """Get manifest of available components.

        Returns:
            Dictionary with component names and their files/directories
        """
        if self._manifest:
            return self._manifest

        source_claude = self._get_source_claude_dir()

        self._manifest = {
            "agents": self._list_files(source_claude / "agents"),
            "commands": self._list_files(source_claude / "commands"),
            "skills": self._list_dirs(source_claude / "skills"),
        }

        return self._manifest

    def deploy(
        self,
        target_dir: Path,
        components: List[str],
        mode: DeployMode = DeployMode.OVERWRITE,
    ) -> Dict:
        """Deploy selected components to target directory.

        Args:
            target_dir: Target project directory
            components: List of components to deploy
            mode: Deployment mode (OVERWRITE or MERGE)

        Returns:
            Deployment result dictionary
        """
        source_claude = self._get_source_claude_dir()
        target_claude = target_dir / CLAUDE_DIR

        # Create target directory
        target_claude.mkdir(parents=True, exist_ok=True)

        result = {
            "components": {},
            "version": self._get_version(),
            "commit": self.git_ops.get_commit_hash(self._temp_dir),
            "mode": mode.value,
            "merge_stats": {},
        }

        # Deploy each component
        for component in components:
            src = source_claude / component
            dst = target_claude / component

            if src.exists():
                if mode == DeployMode.MERGE and dst.exists():
                    merge_result = self._merge_component(src, dst, component)
                    result["components"][component] = {
                        "success": True,
                        "count": merge_result["total_files"],
                    }
                    result["merge_stats"][component] = merge_result
                else:
                    # Standard overwrite mode
                    if dst.exists():
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)

                    count = len([f for f in dst.rglob("*") if f.is_file()])
                    result["components"][component] = {"success": True, "count": count}
            else:
                result["components"][component] = {
                    "success": False,
                    "count": 0,
                    "error": "Source not found",
                }

        # Write metadata
        self._write_metadata(target_claude, result, components)

        # Cleanup
        self._cleanup()

        return result

    def _merge_component(
        self, src: Path, dst: Path, component: str
    ) -> Dict:
        """Merge source component with existing destination.

        This preserves user-added files/directories while updating
        files that exist in the source.

        Args:
            src: Source component directory
            dst: Destination component directory
            component: Component name (agents, commands, skills)

        Returns:
            Merge statistics dictionary
        """
        stats = {
            "updated": [],
            "added": [],
            "preserved": [],
            "total_files": 0,
        }

        # Get all items in source and destination
        src_items = set(item.name for item in src.iterdir())
        dst_items = set(item.name for item in dst.iterdir())

        # Items only in destination (user additions) - preserve them
        user_additions = dst_items - src_items
        stats["preserved"] = list(user_additions)

        # Items in both - update them
        common_items = src_items & dst_items
        for item_name in common_items:
            src_item = src / item_name
            dst_item = dst / item_name

            if src_item.is_dir():
                # For directories (like skills), recursively merge
                self._merge_directory(src_item, dst_item, stats)
            else:
                # For files, overwrite with source
                shutil.copy2(src_item, dst_item)
                stats["updated"].append(item_name)

        # Items only in source - add them
        new_items = src_items - dst_items
        for item_name in new_items:
            src_item = src / item_name
            dst_item = dst / item_name

            if src_item.is_dir():
                shutil.copytree(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)
            stats["added"].append(item_name)

        # Count total files
        stats["total_files"] = len([f for f in dst.rglob("*") if f.is_file()])

        return stats

    def _merge_directory(self, src: Path, dst: Path, stats: Dict) -> None:
        """Recursively merge source directory into destination.

        Args:
            src: Source directory
            dst: Destination directory
            stats: Statistics dictionary to update
        """
        src_items = set(item.name for item in src.iterdir())
        dst_items = set(item.name for item in dst.iterdir()) if dst.exists() else set()

        # Process common items
        for item_name in src_items & dst_items:
            src_item = src / item_name
            dst_item = dst / item_name

            if src_item.is_dir() and dst_item.is_dir():
                self._merge_directory(src_item, dst_item, stats)
            elif src_item.is_file():
                shutil.copy2(src_item, dst_item)

        # Add new items from source
        for item_name in src_items - dst_items:
            src_item = src / item_name
            dst_item = dst / item_name

            if src_item.is_dir():
                shutil.copytree(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)

    def _get_source_dir(self) -> Path:
        """Get path to source directory containing components.

        In official plugin format, components (agents/, commands/, skills/)
        are at the root level, not under .claude/.

        Returns:
            Path to the source directory (root of plugin)
        """
        if self._temp_dir:
            return Path(self._temp_dir)

        # Check if source is a local path
        if os.path.isdir(self.source):
            return Path(self.source)

        # Clone remote repository
        self._temp_dir = tempfile.mkdtemp(prefix="hca_")
        self.git_ops.clone(self.source, self._temp_dir, self.branch, depth=1)

        return Path(self._temp_dir)

    def _get_source_claude_dir(self) -> Path:
        """Get path to source directory (for backwards compatibility).

        Returns:
            Path to the source directory
        """
        return self._get_source_dir()

    def _write_metadata(
        self, claude_dir: Path, result: Dict, components: List[str]
    ) -> None:
        """Write deployment metadata.

        Args:
            claude_dir: Target .claude directory
            result: Deployment result
            components: List of deployed components
        """
        metadata_dir = claude_dir / METADATA_DIR
        metadata_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "version": result["version"],
            "source": self.source,
            "branch": self.branch,
            "commit": result["commit"],
            "installed_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "components": {},
            "checksums": {},
        }

        # Record component info and checksums
        for component in components:
            component_dir = claude_dir / component
            if component_dir.exists():
                files = [f for f in component_dir.rglob("*") if f.is_file()]
                metadata["components"][component] = {
                    "installed": True,
                    "files": [
                        str(f.relative_to(claude_dir)) for f in files
                    ],
                }

                # Compute checksums
                for f in files:
                    rel_path = str(f.relative_to(claude_dir))
                    metadata["checksums"][rel_path] = self._compute_checksum(f)

        metadata_file = metadata_dir / METADATA_FILE
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum of a file.

        Args:
            file_path: Path to the file

        Returns:
            Checksum string with sha256 prefix
        """
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return f"sha256:{sha256_hash.hexdigest()[:16]}"

    def _get_version(self) -> str:
        """Get version from CLI package.

        Returns:
            Version string
        """
        from cli import __version__

        return __version__

    def _list_files(self, directory: Path) -> List[str]:
        """List files in directory.

        Args:
            directory: Directory path

        Returns:
            List of file names
        """
        if not directory.exists():
            return []
        return [f.name for f in directory.iterdir() if f.is_file()]

    def _list_dirs(self, directory: Path) -> List[str]:
        """List directories in directory.

        Args:
            directory: Directory path

        Returns:
            List of directory names
        """
        if not directory.exists():
            return []
        return [d.name for d in directory.iterdir() if d.is_dir()]

    def _cleanup(self) -> None:
        """Clean up temporary directory."""
        if self._temp_dir and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir)
            self._temp_dir = None
