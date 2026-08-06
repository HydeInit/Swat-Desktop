# Packaging

Source for `.deb` packages built outside the ISO itself, so branding and
tooling updates can ship via `apt` instead of a fresh respin.

Each package is a standard Debian source tree (native format — no
separate upstream tarball, since these only exist as part of this
project):

```
packaging/<name>/
├── debian/
│   ├── control
│   ├── changelog
│   ├── rules
│   ├── install
│   └── source/format
└── <files installed by debian/install>
```

Build with `dpkg-buildpackage -us -uc -b` from inside a package
directory (needs `dpkg-dev`, `debhelper`, and `build-essential` — same
Debian build environment as the ISO itself, not the host).

## `swat-branding`

Minimal package (default wallpaper only) that exists to validate the
build → sign → publish → install pipeline before anything with real
behavior is packaged the same way. See `docs/decisions.md` for what was
verified.
