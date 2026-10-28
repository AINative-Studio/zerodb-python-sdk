"""
Parser for AINative's x402 payment-protocol `WWW-Authenticate: Payment ...`
header.

This mirrors the TypeScript SDK's `parseX402PaymentHeader` (see
developer-tools/sdks/typescript/src/x402/parseHeader.ts) for IF-TIME-PERMITS
parity. Only the pure header parser is mirrored here -- a typed backend-call
wrapper (equivalent to the TS SDK's `X402Client`) is out of scope for this
pass; see core#<G6 issue> for the TypeScript implementation this was
derived from.

The REAL header format, as emitted by
`app/api/v1/endpoints/x402_subscriptions.py::subscribe_via_x402`
(core#9247, Machine Payments Protocol discovery convention):

    Payment scheme="exact", network="base", asset="USDC", amount="2000", pay_to="0xabc..."

i.e. the literal word ``Payment`` followed by a comma-separated list of
``key="value"`` pairs. This is NOT full RFC 7235 challenge syntax (no
``realm``, ``Payment`` is not an IANA-registered auth-scheme) -- it is
AINative's own convention, so this parser matches that exact shape rather
than a generic WWW-Authenticate grammar.
"""

import re
from typing import Dict, Optional

# The literal auth-scheme word the backend emits.
_PAYMENT_SCHEME_PREFIX = "payment"

# Matches one key="value" pair. Values are always double-quoted by the backend.
_PARAM_PATTERN = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"((?:[^"\\]|\\.)*)"')

# The only fields this parser recognizes -- anything else in the header is
# ignored (forward-compatible) rather than causing a failure.
_KNOWN_FIELDS = frozenset({"scheme", "network", "asset", "amount", "pay_to"})


def parse_x402_payment_header(header: Optional[str]) -> Optional[Dict[str, str]]:
    """Parse a ``WWW-Authenticate: Payment ...`` header value into a dict.

    Returns ``None`` when ``header`` is falsy, does not start with the
    ``Payment`` scheme, or contains no recognized ``key="value"`` pairs --
    callers should treat ``None`` as "not an x402 challenge" rather than
    raising, since a 401/other-scheme WWW-Authenticate header on the same
    route is a normal, non-x402 case.

    Any individual field missing from the header is simply omitted from the
    result rather than defaulted -- callers that need a guaranteed
    ``scheme`` should fall back to ``"exact"`` themselves, matching the
    backend's own default when building the header.

    >>> parse_x402_payment_header(
    ...     'Payment scheme="exact", network="base", asset="USDC", '
    ...     'amount="2000", pay_to="0xdead"'
    ... )
    {'scheme': 'exact', 'network': 'base', 'asset': 'USDC', 'amount': '2000', 'pay_to': '0xdead'}
    """
    if not header or not isinstance(header, str):
        return None

    trimmed = header.strip()
    if not trimmed.lower().startswith(_PAYMENT_SCHEME_PREFIX):
        return None

    # Everything after the leading scheme word is the param list.
    params_part = trimmed[len(_PAYMENT_SCHEME_PREFIX):]

    result: Dict[str, str] = {}
    for match in _PARAM_PATTERN.finditer(params_part):
        key = match.group(1).lower()
        if key not in _KNOWN_FIELDS:
            # Unknown/forward-compatible param -- ignore rather than fail.
            continue
        value = re.sub(r"\\(.)", r"\1", match.group(2))  # unescape \" and \\
        result[key] = value

    # No recognized params at all means this wasn't really a Payment
    # challenge we understand, even though the scheme word matched.
    if not result:
        return None

    return result


def parse_x402_payment_header_or_raise(header: Optional[str]) -> Dict[str, str]:
    """Like :func:`parse_x402_payment_header`, but raises ``ValueError``
    instead of returning ``None`` when the header is missing or
    unparseable. Useful once a caller has already confirmed (e.g. via a
    402 status code) that a payment challenge is expected.
    """
    parsed = parse_x402_payment_header(header)
    if parsed is None:
        raise ValueError(
            "Could not parse WWW-Authenticate header as an x402 Payment "
            f"challenge: {header!r}"
        )
    return parsed
