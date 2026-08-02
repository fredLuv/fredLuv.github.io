# References

The explanations in this book are original summaries. Use these primary sources
when you want specification-level depth or behavior changes across Python versions.

## Role and book structure

- Supplied file: `QRT - Quant Dev QP (HK).docx` (the authority for this role pack).
- [QRT Quantitative Development careers](https://www.qube-rt.com/careers/technology/quantitative-development/singapore/)
- [GitBook content configuration](https://gitbook.com/docs/getting-started/git-sync/content-configuration)

## Python

- [Python language reference: data model](https://docs.python.org/3/reference/datamodel.html)
- [Python tutorial: data structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python typing specification](https://typing.python.org/en/latest/spec/)
- [`dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [`collections.abc`](https://docs.python.org/3/library/collections.abc.html)
- [`contextlib`](https://docs.python.org/3/library/contextlib.html)
- [`asyncio`](https://docs.python.org/3/library/asyncio.html)
- [`concurrent.futures`](https://docs.python.org/3/library/concurrent.futures.html)
- [`threading` and the GIL note](https://docs.python.org/3/library/threading.html)
- [`multiprocessing`](https://docs.python.org/3/library/multiprocessing.html)
- [Python profiling](https://docs.python.org/3/library/profile.html)
- [`timeit`](https://docs.python.org/3/library/timeit.html)
- [`unittest`](https://docs.python.org/3/library/unittest.html)
- [`decimal`](https://docs.python.org/3/library/decimal.html)

## Study caveat

Python implementation details evolve. Treat the language reference and the
documentation for the interpreter version used by the interview/team as final.
Do not rely on incidental atomicity, object interning, or one CPython build's GIL
behavior as a correctness contract.
