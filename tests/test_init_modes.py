"""Tests for hca init --backup and --merge modes."""

import json
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from cli.core.config import CLAUDE_DIR, METADATA_DIR, METADATA_FILE
from cli.core.deployer import DeployMode, Deployer


class TestDeployerMergeMode:
    """Test the Deployer class merge functionality."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary source and target directories."""
        source_dir = tempfile.mkdtemp(prefix="hca_source_")
        target_dir = tempfile.mkdtemp(prefix="hca_target_")

        yield {"source": Path(source_dir), "target": Path(target_dir)}

        # Cleanup
        shutil.rmtree(source_dir, ignore_errors=True)
        shutil.rmtree(target_dir, ignore_errors=True)

    @pytest.fixture
    def setup_source(self, temp_dirs):
        """Set up source .claude directory structure."""
        source_claude = temp_dirs["source"] / CLAUDE_DIR
        source_claude.mkdir(parents=True)

        # Create agents
        agents_dir = source_claude / "agents"
        agents_dir.mkdir()
        (agents_dir / "agent1.md").write_text("# Agent 1 from source")
        (agents_dir / "agent2.md").write_text("# Agent 2 from source")

        # Create commands
        commands_dir = source_claude / "commands"
        commands_dir.mkdir()
        (commands_dir / "cmd1.md").write_text("# Command 1 from source")

        # Create skills
        skills_dir = source_claude / "skills"
        skills_dir.mkdir()
        skill1_dir = skills_dir / "skill1"
        skill1_dir.mkdir()
        (skill1_dir / "SKILL.md").write_text("# Skill 1 from source")

        return temp_dirs

    @pytest.fixture
    def setup_existing_target(self, setup_source):
        """Set up existing .claude directory in target."""
        temp_dirs = setup_source
        target_claude = temp_dirs["target"] / CLAUDE_DIR
        target_claude.mkdir(parents=True)

        # Create agents (some overlap, some unique)
        agents_dir = target_claude / "agents"
        agents_dir.mkdir()
        (agents_dir / "agent1.md").write_text("# Agent 1 - USER MODIFIED")
        (agents_dir / "my-custom-agent.md").write_text("# My Custom Agent")

        # Create commands (some overlap, some unique)
        commands_dir = target_claude / "commands"
        commands_dir.mkdir()
        (commands_dir / "cmd1.md").write_text("# Command 1 - USER MODIFIED")
        (commands_dir / "my-custom-cmd.md").write_text("# My Custom Command")

        # Create skills (some overlap, some unique)
        skills_dir = target_claude / "skills"
        skills_dir.mkdir()
        skill1_dir = skills_dir / "skill1"
        skill1_dir.mkdir()
        (skill1_dir / "SKILL.md").write_text("# Skill 1 - USER MODIFIED")
        custom_skill_dir = skills_dir / "my-custom-skill"
        custom_skill_dir.mkdir()
        (custom_skill_dir / "SKILL.md").write_text("# My Custom Skill")

        return temp_dirs


class TestBackupMode:
    """Test backup mode functionality."""

    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory."""
        project_dir = tempfile.mkdtemp(prefix="hca_project_")
        yield Path(project_dir)
        shutil.rmtree(project_dir, ignore_errors=True)

    def test_backup_creates_timestamped_directory(self, temp_project):
        """Test that backup creates a timestamped backup directory."""
        from datetime import datetime

        from cli.commands.init import _backup_and_remove

        # Create existing .claude directory
        claude_dir = temp_project / CLAUDE_DIR
        claude_dir.mkdir()
        (claude_dir / "test.md").write_text("test content")

        # Perform backup
        backup_path = _backup_and_remove(claude_dir)

        # Verify backup exists
        assert backup_path.exists()
        assert backup_path.name.startswith(".claude-backup-")
        assert not claude_dir.exists()

        # Verify content preserved
        assert (backup_path / "test.md").read_text() == "test content"


class TestMergeMode:
    """Test merge mode functionality."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        source_dir = tempfile.mkdtemp(prefix="hca_source_")
        target_dir = tempfile.mkdtemp(prefix="hca_target_")

        yield {"source": Path(source_dir), "target": Path(target_dir)}

        shutil.rmtree(source_dir, ignore_errors=True)
        shutil.rmtree(target_dir, ignore_errors=True)

    def test_merge_preserves_user_additions(self, temp_dirs):
        """Test that merge mode preserves user-added files."""
        source = temp_dirs["source"]
        target = temp_dirs["target"]

        # Setup source
        source_claude = source / CLAUDE_DIR
        source_agents = source_claude / "agents"
        source_agents.mkdir(parents=True)
        (source_agents / "agent1.md").write_text("# Agent 1 from source")

        # Setup target with user additions
        target_claude = target / CLAUDE_DIR
        target_agents = target_claude / "agents"
        target_agents.mkdir(parents=True)
        (target_agents / "agent1.md").write_text("# Agent 1 USER MODIFIED")
        (target_agents / "my-agent.md").write_text("# My Custom Agent")

        # Mock GitOps to avoid actual git operations
        with patch.object(Deployer, "_get_source_claude_dir") as mock_get_source:
            mock_get_source.return_value = source_claude
            with patch.object(Deployer, "_cleanup"):
                deployer = Deployer(str(source), "main")
                deployer._temp_dir = str(source)

                with patch("cli.core.deployer.GitOps") as mock_git:
                    mock_git.return_value.get_commit_hash.return_value = "abc123"
                    deployer.git_ops = mock_git.return_value

                    result = deployer.deploy(target, ["agents"], mode=DeployMode.MERGE)

        # Verify user addition is preserved
        assert (target_agents / "my-agent.md").exists()
        assert (target_agents / "my-agent.md").read_text() == "# My Custom Agent"

        # Verify source file updated
        assert (target_agents / "agent1.md").read_text() == "# Agent 1 from source"

        # Check merge stats
        assert "agents" in result["merge_stats"]
        assert "my-agent.md" in result["merge_stats"]["agents"]["preserved"]

    def test_merge_adds_new_source_files(self, temp_dirs):
        """Test that merge mode adds new files from source."""
        source = temp_dirs["source"]
        target = temp_dirs["target"]

        # Setup source with multiple agents
        source_claude = source / CLAUDE_DIR
        source_agents = source_claude / "agents"
        source_agents.mkdir(parents=True)
        (source_agents / "agent1.md").write_text("# Agent 1")
        (source_agents / "agent2.md").write_text("# Agent 2 NEW")

        # Setup target with only one agent
        target_claude = target / CLAUDE_DIR
        target_agents = target_claude / "agents"
        target_agents.mkdir(parents=True)
        (target_agents / "agent1.md").write_text("# Agent 1 old")

        with patch.object(Deployer, "_get_source_claude_dir") as mock_get_source:
            mock_get_source.return_value = source_claude
            with patch.object(Deployer, "_cleanup"):
                deployer = Deployer(str(source), "main")
                deployer._temp_dir = str(source)

                with patch("cli.core.deployer.GitOps") as mock_git:
                    mock_git.return_value.get_commit_hash.return_value = "abc123"
                    deployer.git_ops = mock_git.return_value

                    result = deployer.deploy(target, ["agents"], mode=DeployMode.MERGE)

        # Verify new file added
        assert (target_agents / "agent2.md").exists()
        assert (target_agents / "agent2.md").read_text() == "# Agent 2 NEW"

        # Check merge stats
        assert "agent2.md" in result["merge_stats"]["agents"]["added"]


class TestOverwriteMode:
    """Test overwrite mode functionality."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories."""
        source_dir = tempfile.mkdtemp(prefix="hca_source_")
        target_dir = tempfile.mkdtemp(prefix="hca_target_")

        yield {"source": Path(source_dir), "target": Path(target_dir)}

        shutil.rmtree(source_dir, ignore_errors=True)
        shutil.rmtree(target_dir, ignore_errors=True)

    def test_overwrite_removes_user_additions(self, temp_dirs):
        """Test that overwrite mode removes user-added files."""
        source = temp_dirs["source"]
        target = temp_dirs["target"]

        # Setup source
        source_claude = source / CLAUDE_DIR
        source_agents = source_claude / "agents"
        source_agents.mkdir(parents=True)
        (source_agents / "agent1.md").write_text("# Agent 1")

        # Setup target with user additions
        target_claude = target / CLAUDE_DIR
        target_agents = target_claude / "agents"
        target_agents.mkdir(parents=True)
        (target_agents / "my-agent.md").write_text("# My Custom Agent")

        with patch.object(Deployer, "_get_source_claude_dir") as mock_get_source:
            mock_get_source.return_value = source_claude
            with patch.object(Deployer, "_cleanup"):
                deployer = Deployer(str(source), "main")
                deployer._temp_dir = str(source)

                with patch("cli.core.deployer.GitOps") as mock_git:
                    mock_git.return_value.get_commit_hash.return_value = "abc123"
                    deployer.git_ops = mock_git.return_value

                    result = deployer.deploy(
                        target, ["agents"], mode=DeployMode.OVERWRITE
                    )

        # Verify user addition is removed
        assert not (target_agents / "my-agent.md").exists()

        # Verify only source files exist
        assert (target_agents / "agent1.md").exists()


def run_integration_test():
    """Run a simple integration test for backup and merge modes."""
    print("=" * 60)
    print("Integration Test: Backup and Merge Modes")
    print("=" * 60)

    # Create test directories
    test_base = Path(tempfile.mkdtemp(prefix="hca_integration_"))
    source_dir = test_base / "source"
    project_dir = test_base / "project"

    try:
        # Setup source repository structure
        source_claude = source_dir / CLAUDE_DIR
        (source_claude / "agents").mkdir(parents=True)
        (source_claude / "agents" / "explore.md").write_text("# Explore Agent v2")
        (source_claude / "agents" / "plan.md").write_text("# Plan Agent v2")
        (source_claude / "commands").mkdir()
        (source_claude / "commands" / "feature.md").write_text("# Feature Command")
        (source_claude / "skills").mkdir()
        (source_claude / "skills" / "skill1").mkdir()
        (source_claude / "skills" / "skill1" / "SKILL.md").write_text("# Skill 1")

        # Setup existing project structure
        project_claude = project_dir / CLAUDE_DIR
        (project_claude / "agents").mkdir(parents=True)
        (project_claude / "agents" / "explore.md").write_text("# Explore Agent v1 USER")
        (project_claude / "agents" / "my-custom.md").write_text("# My Custom Agent")
        (project_claude / "commands").mkdir()
        (project_claude / "commands" / "my-cmd.md").write_text("# My Command")
        (project_claude / "skills").mkdir()
        (project_claude / "skills" / "my-skill").mkdir()
        (project_claude / "skills" / "my-skill" / "SKILL.md").write_text("# My Skill")

        print("\n1. Testing BACKUP mode...")
        print("-" * 40)

        # Test backup mode
        backup_project = test_base / "project_backup"
        shutil.copytree(project_dir, backup_project)
        backup_claude = backup_project / CLAUDE_DIR

        from cli.commands.init import _backup_and_remove

        backup_path = _backup_and_remove(backup_claude)

        print(f"   Backup created: {backup_path.name}")
        print(f"   Original .claude removed: {not backup_claude.exists()}")
        print(f"   Backup contains files: {list(backup_path.rglob('*.md'))[:3]}")

        assert backup_path.exists(), "Backup should exist"
        assert not backup_claude.exists(), "Original .claude should be removed"
        assert (backup_path / "agents" / "my-custom.md").exists(), "User files in backup"

        print("   [PASS] Backup mode works correctly!")

        print("\n2. Testing MERGE mode...")
        print("-" * 40)

        # Test merge mode
        merge_project = test_base / "project_merge"
        shutil.copytree(project_dir, merge_project)

        with patch.object(Deployer, "_get_source_claude_dir") as mock:
            mock.return_value = source_claude
            with patch.object(Deployer, "_cleanup"):
                deployer = Deployer(str(source_dir), "main")
                deployer._temp_dir = str(source_dir)

                with patch("cli.core.deployer.GitOps") as mock_git:
                    mock_git.return_value.get_commit_hash.return_value = "test123"
                    deployer.git_ops = mock_git.return_value

                    result = deployer.deploy(
                        merge_project, ["agents", "commands", "skills"],
                        mode=DeployMode.MERGE
                    )

        merge_claude = merge_project / CLAUDE_DIR

        # Verify merge results
        print(f"   Mode: {result['mode']}")
        print(f"   Merge stats: {json.dumps(result['merge_stats'], indent=4)}")

        # Check user files preserved
        assert (merge_claude / "agents" / "my-custom.md").exists(), \
            "User agent should be preserved"
        assert (merge_claude / "commands" / "my-cmd.md").exists(), \
            "User command should be preserved"
        assert (merge_claude / "skills" / "my-skill" / "SKILL.md").exists(), \
            "User skill should be preserved"

        # Check source files updated/added
        assert (merge_claude / "agents" / "explore.md").read_text() == "# Explore Agent v2", \
            "Source agent should be updated"
        assert (merge_claude / "agents" / "plan.md").exists(), \
            "New source agent should be added"

        print("   [PASS] User additions preserved!")
        print("   [PASS] Source files updated!")
        print("   [PASS] Merge mode works correctly!")

        print("\n3. Testing OVERWRITE mode...")
        print("-" * 40)

        # Test overwrite mode
        overwrite_project = test_base / "project_overwrite"
        shutil.copytree(project_dir, overwrite_project)

        with patch.object(Deployer, "_get_source_claude_dir") as mock:
            mock.return_value = source_claude
            with patch.object(Deployer, "_cleanup"):
                deployer = Deployer(str(source_dir), "main")
                deployer._temp_dir = str(source_dir)

                with patch("cli.core.deployer.GitOps") as mock_git:
                    mock_git.return_value.get_commit_hash.return_value = "test123"
                    deployer.git_ops = mock_git.return_value

                    result = deployer.deploy(
                        overwrite_project, ["agents", "commands", "skills"],
                        mode=DeployMode.OVERWRITE
                    )

        overwrite_claude = overwrite_project / CLAUDE_DIR

        # Check user files removed
        assert not (overwrite_claude / "agents" / "my-custom.md").exists(), \
            "User agent should be removed"
        assert not (overwrite_claude / "commands" / "my-cmd.md").exists(), \
            "User command should be removed"

        print("   [PASS] User additions removed!")
        print("   [PASS] Overwrite mode works correctly!")

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        shutil.rmtree(test_base, ignore_errors=True)


if __name__ == "__main__":
    success = run_integration_test()
    exit(0 if success else 1)
