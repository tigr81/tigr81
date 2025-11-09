# Dev Container for tigr81

This dev container is configured to test the `tigr81` package using `uvx` without installing it in the container.

## Setup

1. Open the project in VS Code
2. When prompted, click "Reopen in Container" or use the Command Palette: `Dev Containers: Reopen in Container`
3. Wait for the container to build and `uv` to be installed

## Usage

Once the dev container is running, you can test your package using `uvx` in several ways:

### Option 1: Run from the package directory (Recommended)

```bash
cd /workspace
uvx --from . tigr81 --help
```

### Option 2: Run specific commands

```bash
cd /workspace
uvx --from . tigr81 version
uvx --from . tigr81 scaffold fastapi
uvx --from . tigr81 hub --help
uvx --from . tigr81 monorepo --help
```

### Option 3: Test with different Python versions

```bash
cd /workspace
uvx --python 3.9 --from . tigr81 --help
uvx --python 3.10 --from . tigr81 --help
uvx --python 3.11 --from . tigr81 --help
```

### Option 4: Test from PyPI (as users would)

To test the package as it would be installed from PyPI:

```bash
uvx tigr81 --help
uvx tigr81 version
uvx tigr81 scaffold fastapi
uvx tigr81 hub --help
uvx tigr81 monorepo --help
```

You can also test with different Python versions:

```bash
uvx --python 3.9 tigr81 --help
uvx --python 3.10 tigr81 --help
uvx --python 3.11 tigr81 --help
```

## Features

- Python 3.9 pre-installed
- `uv` and `uvx` installed automatically via postCreateCommand
- Workspace automatically mounted at `/workspace`
- VS Code Python extensions pre-configured (Python, Pylance, Ruff)

## Notes

- The package is **not installed** in the container, allowing you to test it exactly as users would experience it via `uvx`
- Each `uvx` command runs in an isolated environment, simulating how users would run your package
- The container starts in `/workspace` directory (which is the `tigr81` package root)
- `uv` is installed in `~/.cargo/bin` and added to PATH automatically
