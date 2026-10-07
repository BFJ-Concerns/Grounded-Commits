# Area derivation

The procedure the checker applies to turn a changed path into a subject area.
Two writers get the same answer because nothing in it is a judgement; the
checker's `--areas` command prints the result for the staged change, so read
this when you cannot run it, when a candidate surprises you, or when you are
configuring a repository's path map.

1. If the repository has a **path map** (`[area_map]` in `.grounded-
   commits.toml`, or a list in its guidance), the longest matching prefix
   gives the area. A path no entry matches is derived as below. 2. Otherwise
   walk the path's directories from the top. A **collection** directory
   (`packages`, `apps`, `crates`, `modules`, `services`, `cmd`, `pkg`,
   `internal`) is skipped, and so is a scope such as `@acme` directly inside
   it; the next segment is the area, even one named like a collection. A
   **layout** directory (`src`, `source`, `sources`, `lib`, `libs`, `include`,
   `app`, `main`, `java`, `kotlin`, `scala`, and `test` or `tests` directly
   inside one of those) is skipped; directly after a layout directory, a
   directory that is its parent's only tracked subdirectory is skipped too,
   and after `java`, `kotlin` or `scala` the reverse-domain package root
   (`com/acme`, `io/github/user`) is skipped as well. Any other directory is
   the area. With no directory left, the area is the file's name without its
   extension (`README.md` gives `readme`), or the directory's name for a file
   that stands for its directory (`__init__.py`, `mod.rs`, `index.ts`,
   `main.go`, `lib.rs`). 3. Lower-case it, drop characters outside
   `[a-z0-9._/-]`, and trim anything that is not a letter or digit from both
   ends (`.github` gives `github`). A result longer than 24 characters is not
   an area: use `all` and name the directory in the body, or add a path-map
   entry. 4. A change-type word (`feat`, `fix`, `perf`, `chore`, `refactor`,
   `style`, `revert`) is never an area, and `ci`, `docs`, `test`, `tests` and
   `build` are areas only when they name a directory, a path-map label or a
   listed area. A file whose stem reads as one of those keeps its extension
   (`fix.py`, `build.gradle`); a directory named for a change type gives
   `all`, named in the body; a `docs/` or `build/` directory gives `docs` or
   `build`.

So `internal/scheduler/worker.go` gives `scheduler`, `src/mypkg/cli.py` gives
`cli`, `app/models/user.rb` gives `models` beside other directories under
`app`, `src/main/java/com/acme/billing/Invoice.java` gives `billing`,
`packages/@acme/payments/src/charge.ts` gives `payments`,
`.github/workflows/ci.yml` gives `github`, and a root `Cargo.toml` gives
`cargo`. The only-subdirectory rule reads the tracked tree, so
`src/mypkg/cli.py` gives `cli` while `mypkg` is the only directory under `src`
and `mypkg` once a second appears; crossing that line in either direction is
the one way a change elsewhere moves an area. Derivation is a default: a
repository it does not fit writes a path map, and the areas it lists (`areas`
in `.grounded-commits.toml`) are always valid.
