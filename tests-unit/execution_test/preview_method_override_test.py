"""
Unit tests for Queue-specific Preview Method Override feature.

Tests the preview method override functionality:
- LatentPreviewMethod.from_string() method
- set_preview_method() function in latent_preview.py
- default_preview_method variable
- Integration with args.preview_method
"""
import pytest
from comfy.cli_args import args, LatentPreviewMethod
from latent_preview import set_preview_method, default_preview_method


class TestLatentPreviewMethodFromString:
    """Test LatentPreviewMethod.from_string() classmethod."""

    @pytest.mark.parametrize("value,expected", [
        ("auto", LatentPreviewMethod.Auto),
        ("latent2rgb", LatentPreviewMethod.Latent2RGB),
        ("taesd", LatentPreviewMethod.TAESD),
        ("none", LatentPreviewMethod.NoPreviews),
    ])
    def test_valid_values_return_enum(self, value, expected):
        """Valid string values should return corresponding enum."""
        assert LatentPreviewMethod.from_string(value) == expected

    @pytest.mark.parametrize("invalid", [
        "invalid",
        "TAESD",      # Case sensitive
        "AUTO",       # Case sensitive
        "Latent2RGB", # Case sensitive
        "latent",
        "",
        "default",    # default is special, not a method
    ])
    def test_invalid_values_return_none(self, invalid):
        """Invalid string values should return None."""
        assert LatentPreviewMethod.from_string(invalid) is None


class TestSetPreviewMethod:
    """Test set_preview_method() function from latent_preview.py."""

    def setup_method(self):
        """Store original value before each test."""
        self.original = args.preview_method

    def teardown_method(self):
        """Restore original value after each test."""
        args.preview_method = self.original

    def test_override_with_taesd(self):
        """'taesd' should set args.preview_method to TAESD."""
        set_preview_method("taesd")
        assert args.preview_method == LatentPreviewMethod.TAESD

    def test_override_with_latent2rgb(self):
        """'latent2rgb' should set args.preview_method to Latent2RGB."""
        set_preview_method("latent2rgb")
        assert args.preview_method == LatentPreviewMethod.Latent2RGB

    def test_override_with_auto(self):
        """'auto' should set args.preview_method to Auto."""
        set_preview_method("auto")
        assert args.preview_method == LatentPreviewMethod.Auto

    def test_override_with_none_value(self):
        """'none' should set args.preview_method to NoPreviews."""
        set_preview_method("none")
        assert args.preview_method == LatentPreviewMethod.NoPreviews

    def test_default_restores_original(self):
        """'default' should restore to default_preview_method."""
        # First override to something else
        set_preview_method("taesd")
        assert args.preview_method == LatentPreviewMethod.TAESD

        # Then use 'default' to restore
        set_preview_method("default")
        assert args.preview_method == default_preview_method

    def test_none_param_restores_original(self):
        """None parameter should restore to default_preview_method."""
        # First override to something else
        set_preview_method("taesd")
        assert args.preview_method == LatentPreviewMethod.TAESD

        # Then use None to restore
        set_preview_method(None)
        assert args.preview_method == default_preview_method

    def test_empty_string_restores_original(self):
        """Empty string should restore to default_preview_method."""
        set_preview_method("taesd")
        set_preview_method("")
        assert args.preview_method == default_preview_method

    def test_invalid_value_restores_original(self):
        """Invalid value should restore to default_preview_method."""
        set_preview_method("taesd")
        set_preview_method("invalid_method")
        assert args.preview_method == default_preview_method

    def test_case_sensitive_invalid_restores(self):
        """Case-mismatched values should restore to default."""
        set_preview_method("taesd")
        set_preview_method("TAESD")  # Wrong case
        assert args.preview_method == default_preview_method


class TestExecutionFlow:
    """Test the execution flow pattern used in execution.py."""

    def setup_method(self):
        """Store original value before each test."""
        self.original = args.preview_method

    def teardown_method(self):
        """Restore original value after each test."""
        args.preview_method = self.original

    def test_sequential_executions_with_different_methods(self):
        """Simulate multiple queue executions with different preview methods."""
        # Execution 1: taesd
        set_preview_method("taesd")
        assert args.preview_method == LatentPreviewMethod.TAESD

        # Execution 2: none
        set_preview_method("none")
        assert args.preview_method == LatentPreviewMethod.NoPreviews

        # Execution 3: default (restore)
        set_preview_method("default")
        assert args.preview_method == default_preview_method

        # Execution 4: auto
        set_preview_method("auto")
        assert args.preview_method == LatentPreviewMethod.Auto

        # Execution 5: no override (None)
        set_preview_method(None)
        assert args.preview_method == default_preview_method
