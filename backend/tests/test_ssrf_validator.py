"""
Tests for SSRF validator module.
"""

import pytest
from django.core.exceptions import ValidationError

from utils.ssrf_validator import (
    SSRFValidator,
    validate_url,
    is_url_safe,
    is_private_ip,
    is_internal_network,
    get_allowed_domains,
)


class TestSSRFValidator:
    """Test cases for SSRFValidator class."""

    def test_valid_allowlisted_domain(self):
        """Test that allowlisted domains are accepted."""
        validator = SSRFValidator(allowed_domains=["example.com", "test.org"])
        # Should not raise
        validator.validate("https://example.com/page")
        validator.validate("https://subdomain.example.com/page")
        validator.validate("https://test.org/article")

    def test_invalid_domain_rejected(self):
        """Test that non-allowlisted domains are rejected."""
        validator = SSRFValidator(allowed_domains=["example.com"])
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("https://malicious.com/page")
        assert "malicious.com" in str(exc_info.value)

    def test_localhost_rejected(self):
        """Test that localhost is rejected."""
        validator = SSRFValidator()
        with pytest.raises(ValidationError):
            validator.validate("http://localhost/page")
        with pytest.raises(ValidationError):
            validator.validate("http://127.0.0.1/page")

    def test_private_ip_rejected(self):
        """Test that private IP addresses are rejected."""
        validator = SSRFValidator()
        # 192.168.x.x
        with pytest.raises(ValidationError):
            validator.validate("http://192.168.1.100/page")
        # 10.x.x.x
        with pytest.raises(ValidationError):
            validator.validate("http://10.0.0.50/page")
        # 172.16-31.x.x
        with pytest.raises(ValidationError):
            validator.validate("http://172.20.0.1/page")

    def test_internal_network_rejected(self):
        """Test that internal network addresses are rejected."""
        validator = SSRFValidator()
        with pytest.raises(ValidationError):
            validator.validate("http://server.internal/page")
        with pytest.raises(ValidationError):
            validator.validate("https://app.local/page")

    def test_invalid_url_format(self):
        """Test that invalid URL formats are rejected."""
        validator = SSRFValidator()
        with pytest.raises(ValidationError):
            validator.validate("not-a-url")
        with pytest.raises(ValidationError):
            validator.validate("ftp://example.com/page")

    def test_http_and_https_allowed(self):
        """Test that HTTP and HTTPS protocols are allowed."""
        validator = SSRFValidator(allowed_domains=["example.com"])
        # Should not raise
        validator.validate("http://example.com/page")
        validator.validate("https://example.com/page")

    def test_is_safe_method(self):
        """Test is_safe method returns boolean."""
        validator = SSRFValidator(allowed_domains=["example.com"])
        assert validator.is_safe("https://example.com/page") is True
        assert validator.is_safe("http://malicious.com/page") is False
        assert validator.is_safe("http://localhost/page") is False


class TestModuleFunctions:
    """Test module-level convenience functions."""

    def test_validate_url_function(self):
        """Test validate_url convenience function."""
        # Should not raise for valid URL
        validate_url("https://wikipedia.org/wiki/Python")

        # Should raise for invalid URL
        with pytest.raises(ValidationError):
            validate_url("http://localhost:8000/secret")

    def test_is_url_safe_function(self):
        """Test is_url_safe convenience function."""
        assert is_url_safe("https://github.com/user/repo") is True
        assert is_url_safe("http://192.168.1.1/admin") is False

    def test_is_private_ip_function(self):
        """Test is_private_ip function."""
        assert is_private_ip("127.0.0.1") is True
        assert is_private_ip("192.168.1.1") is True
        assert is_private_ip("10.0.0.1") is True
        assert is_private_ip("8.8.8.8") is False
        assert is_private_ip("example.com") is False

    def test_is_internal_network_function(self):
        """Test is_internal_network function."""
        assert is_internal_network("server.internal") is True
        assert is_internal_network("app.local") is True
        assert is_internal_network("example.com") is False

    def test_get_allowed_domains_default(self):
        """Test that default domains are returned when env var not set."""
        import os

        # Ensure env var is not set
        original = os.environ.get("ALLOWED_SCRAPE_DOMAINS")
        if original:
            del os.environ["ALLOWED_SCRAPE_DOMAINS"]

        try:
            domains = get_allowed_domains()
            assert isinstance(domains, list)
            assert len(domains) > 0
            assert "wikipedia.org" in domains
            assert "github.com" in domains
        finally:
            # Restore env var
            if original:
                os.environ["ALLOWED_SCRAPE_DOMAINS"] = original

    def test_get_allowed_domains_from_env(self):
        """Test that domains are read from environment variable."""
        import os

        original = os.environ.get("ALLOWED_SCRAPE_DOMAINS")
        os.environ["ALLOWED_SCRAPE_DOMAINS"] = "custom1.com,custom2.com"

        try:
            domains = get_allowed_domains()
            assert "custom1.com" in domains
            assert "custom2.com" in domains
            assert "wikipedia.org" not in domains
        finally:
            # Restore env var
            if original:
                os.environ["ALLOWED_SCRAPE_DOMAINS"] = original
            else:
                del os.environ["ALLOWED_SCRAPE_DOMAINS"]
