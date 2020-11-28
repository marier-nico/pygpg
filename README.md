<h2 align="center">A better way to use GPG</h2>

<p align="center">

![Python Build](https://github.com/marier-nico/pygpg/workflows/Python%20Build/badge.svg?branch=add-style-linters)
![Release](https://img.shields.io/github/v/release/marier-nico/pygpg)
![GitHub](https://img.shields.io/github/license/marier-nico/pygpg)

</p>

pygpg is an easy to use wrapper around the GPG CLI. It simplifies some operations that really shouldn't be as tedious
as they are when using the GPG CLI. The aim is to offer a cohesive and intuitive set of commands that makes GPG key
management and usage simple and easy!

---

## Installation

### With Pip

Installing is simply done by running `pip install pygpg`.

### From Source

This is fairly simple as well. Just clone the project and run `python setup.py install` (note that you should specify
the package version on the CLI, because the version is not in `setup.py` or `setup.cfg`. For an example, see the
[publish workflow](.github/workflows/publish.yml). Specifically, the `Build & Publish` step of the `publish` job.)

## Usage

Using pygpg is super simple :

```
pg {options}
```

or

```
pygpg {options}
```

Both versions behave the same way, but `pg` is shorter and more convenient to type. Running either command yields the
help menu, which should be detailed enough to use pygpg effectively!
