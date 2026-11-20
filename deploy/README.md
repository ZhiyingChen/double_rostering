# Double Rostering deployment

- Directory: `/opt/double_rostering_app`
- Service: `double-rostering-app.service`
- Internal port: `127.0.0.1:8093`
- Public path: `/double-rostering/`

Caddy rule:

```caddy
redir /double-rostering /double-rostering/ 308
handle_path /double-rostering/* {
    reverse_proxy 127.0.0.1:8093
}
```

The Git submodule must be initialized during deployment.
