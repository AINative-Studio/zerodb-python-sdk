"""Tests for the x402 WWW-Authenticate header parser."""

import pytest

from zerodb_mcp.x402 import (
    parse_x402_payment_header,
    parse_x402_payment_header_or_raise,
)


def test_parses_real_header_format_emitted_by_backend():
    # Exact shape from app/api/v1/endpoints/x402_subscriptions.py::subscribe_via_x402
    header = (
        'Payment scheme="exact", network="base", asset="USDC", '
        'amount="2000", pay_to="0xAbC1230000000000000000000000000000dEaD"'
    )

    result = parse_x402_payment_header(header)

    assert result == {
        "scheme": "exact",
        "network": "base",
        "asset": "USDC",
        "amount": "2000",
        "pay_to": "0xAbC1230000000000000000000000000000dEaD",
    }


def test_parses_backend_default_scheme():
    header = (
        'Payment scheme="exact", network="base-sepolia", asset="USDC", '
        'amount="500", pay_to="0x0000000000000000000000000000000000beef"'
    )

    result = parse_x402_payment_header(header)

    assert result["scheme"] == "exact"
    assert result["network"] == "base-sepolia"
    assert result["amount"] == "500"


def test_tolerant_of_extra_whitespace():
    header = 'Payment scheme="exact",   network="base",asset="USDC",   amount="100",pay_to="0xdead"'

    result = parse_x402_payment_header(header)

    assert result == {
        "scheme": "exact",
        "network": "base",
        "asset": "USDC",
        "amount": "100",
        "pay_to": "0xdead",
    }


def test_ignores_unknown_forward_compatible_params():
    header = (
        'Payment scheme="exact", network="base", asset="USDC", amount="100", '
        'pay_to="0xdead", expiry="2026-11-01T00:00:00Z"'
    )

    result = parse_x402_payment_header(header)

    assert result == {
        "scheme": "exact",
        "network": "base",
        "asset": "USDC",
        "amount": "100",
        "pay_to": "0xdead",
    }
    assert "expiry" not in result


@pytest.mark.parametrize("header", [None, "", "   "])
def test_returns_none_for_missing_header(header):
    assert parse_x402_payment_header(header) is None


def test_returns_none_for_malformed_header_wrong_scheme():
    assert parse_x402_payment_header('Bearer realm="api"') is None


def test_returns_none_for_malformed_header_no_parseable_params():
    assert parse_x402_payment_header("Payment this is garbage not key=value pairs at all") is None


def test_returns_none_for_malformed_header_unquoted_values():
    # The backend always double-quotes values; unquoted values don't match
    # the param pattern, so this should parse as "no recognized params".
    assert parse_x402_payment_header("Payment scheme=exact, network=base") is None


def test_parses_partial_headers_without_raising():
    header = 'Payment scheme="exact", amount="100"'

    result = parse_x402_payment_header(header)

    assert result == {"scheme": "exact", "amount": "100"}


def test_or_raise_returns_parsed_dict_on_valid_header():
    header = 'Payment scheme="exact", network="base", asset="USDC", amount="100", pay_to="0xdead"'

    assert parse_x402_payment_header_or_raise(header) == {
        "scheme": "exact",
        "network": "base",
        "asset": "USDC",
        "amount": "100",
        "pay_to": "0xdead",
    }


def test_or_raise_raises_value_error_on_malformed_header():
    with pytest.raises(ValueError, match="Could not parse WWW-Authenticate header"):
        parse_x402_payment_header_or_raise(None)

    with pytest.raises(ValueError, match="Could not parse WWW-Authenticate header"):
        parse_x402_payment_header_or_raise('Bearer realm="api"')
