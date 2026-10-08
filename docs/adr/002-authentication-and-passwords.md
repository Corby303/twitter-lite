# ADR-002 - Argon2id passwords and signed session cookies

**Status:** Proposed for student adoption.

## Context

The MVP uses browser forms and requires secure password storage, login/logout
and protected post creation. A separate mobile/API client or external identity
provider is not required. The application is demonstrated locally over HTTP.

## Decision

Use the argon2-cffi library's Argon2id implementation with 19 MiB memory, two
iterations and one lane. Enforce 15-128 character passwords/passphrases without
arbitrary character-class rules. The library generates a random salt for each
hash and verifies it; never write password hashing cryptography ourselves.

Use Flask's signed session cookie containing the user ID and CSRF/session
metadata, with HttpOnly, SameSite=Lax and one-hour expiry. Clear existing state
on login/logout. Resolve the ID to a stored user before authorizing a post.
Store a generated signing key outside Git in the persistent data directory.
Use Flask-WTF CSRFProtect for all state-changing browser forms.

## Alternatives

- **Plaintext or reversible password encryption:** Rejected; plaintext leaks
  immediately, and reversible encryption exposes passwords if its key is
  compromised. Passwords should be verified through adaptive salted hashing.
- **scrypt:** A reasonable alternative if Argon2id is unavailable; has different
  resource/settings trade-offs. Argon2id is available here through a library.
- **JWT bearer authentication:** Can suit API/mobile clients, but token storage,
  expiry and revocation still need design. Adds no clear benefit to this
  server-rendered local app.
- **Server-side revocable sessions:** Better central logout/revocation control;
  adds server-side session storage/cleanup. A stronger future public deployment
  choice than this scoped local implementation.
- **Hosted identity provider:** Can provide mature identity features but adds
  an external service/account and harms the offline/local demonstration scope.

## Consequences and limitations

Adaptive hashing costs memory/CPU deliberately; authentication must be measured
on the actual deployment machine. Salts make equal passwords produce different
stored hashes. Passwords are not stored in cookies or rendered back in forms.

Signed cookies are integrity-protected **but not encrypted**: do not put secrets
in their payload. Logout clears this browser's session; a previously stolen
valid cookie is not centrally revoked and can be usable until expiry. HTTPS
and `Secure` cookies, server-side sessions, rate limiting, account recovery,
breached-password checks and abuse prevention require future design for public
deployment. Local HTTP deliberately leaves the Secure flag off.

Unknown-user login verifies a dummy hash to reduce a timing difference; this
does not prove the entire response path is constant-time or conceal the
registration form's existing-username message.

## Validation and sources

Tests verify Argon2id settings, salted hashes, password checks, cookie flags,
CSRF rejection, logout behavior and session-derived authorship. Review the
limitations rather than presenting this as a complete production identity
system.

- [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [OWASP authentication guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [argon2-cffi](https://argon2-cffi.readthedocs.io/en/stable/howto.html)
- [Flask-WTF CSRF](https://flask-wtf.readthedocs.io/en/1.2.x/csrf/)
