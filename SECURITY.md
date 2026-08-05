# Security Policy

## Scope

This policy covers the build configuration, scripts, and branding in this repository. SWAT is built from unmodified Debian packages, so a vulnerability in an installed package (the kernel, a library, an application) is a Debian issue, not a SWAT one — please report those upstream via the [Debian Security Tracker](https://security-tracker.debian.org/tracker/) instead.

Issues in scope here include things like: a build script or hook that introduces a vulnerability into the image (insecure permissions, exposed credentials, unsafe defaults), or a flaw in how the image is assembled.

## Reporting a vulnerability

Please don't open a public issue for security reports. Use GitHub's private vulnerability reporting instead: go to the **Security** tab of this repository and select **Report a vulnerability**.

Include what you found, how to reproduce it, and its potential impact if known. Response times aren't guaranteed — this is a personal project — but reports will be looked at.
