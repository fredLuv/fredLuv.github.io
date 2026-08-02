# Companion Python Project

This standard-library project supports the GitBook capstone. It favors explicit
contracts and inspectable code over framework setup.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m hedgeprep.demo
PYTHONPATH=src python3 -m hedgeprep.async_pipeline
```

The package expects Python 3.12+ and can run directly from this directory; an
editable installation (`python3 -m pip install -e .`) is optional.
