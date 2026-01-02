# doc

Documentation viewer for Pynosaur CLI tools. It reads the YAML docs packaged with each tool (local or installed via `pget`) and shows them in a pager (black background, `man`-like navigation). Falls back to plain output when not attached to a TTY.

## Usage

- `doc <tool>` — show documentation for the given tool
- `doc --help` — show help for `doc`
- `doc --version` — show `doc` version

## How it works

1. Looks for `<tool>.yaml` in this repo's `doc/` directory (or bundled `doc/` when built).
2. Falls back to the installed helper docs at `~/.pget/helpers/<tool>/doc/<tool>.yaml`.
3. If nothing is found, exits with status 1 and prints an error.

## Development

- Run tests: `python -m unittest discover -s test`
- Lint is not configured; keep the code minimal and documented in YAML.

## License

MIT

