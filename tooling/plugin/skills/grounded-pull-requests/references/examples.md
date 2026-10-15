# Grounded Pull Requests: examples

One commit, no issue:

```
Title: export: close the query cursor when the client disconnects

Closes the cursor leak reported after last week's incident.

### Check
The cursor is closed from the response's context-done hook; check that nothing else in handler.go relies on that hook running exactly once.
Reproduction against staging not run; the "close the query cursor" commit says why.
```

Four commits, one outcome:

```
export: extract row serialisation from the buffered writer
export: add a streaming writer behind the existing interface
export: stream CSV exports instead of buffering them in memory
docs: describe the X-Row-Count trailer for export clients
```

```
Title: export: stream CSV exports instead of buffering them in memory

Exports of over a million rows kill the worker at 2 GB (https://github.com/example/reports/issues/318). This branch streams rows as the cursor advances and moves the row count to a trailer.

### Read
The first two commits are mechanical and keep the buffered path; the third, "stream CSV exports", is the behaviour change. Start with export/stream.go.

### Check
Content-Length disappears from export responses; the "stream CSV exports" commit records the break. Do we know of any client that reads it?
Production-volume replay not run; the "stream CSV exports" commit says why.

### Try
Against staging, request /exports/1.4m.csv with curl -N; worker RSS should stay flat where it used to climb to 2 GB.

### Not in this PR
A progress signal for clients that used Content-Length to show one; not tracked yet.
```

Neither body repeats a commit's reasoning, lists files or states a result.
