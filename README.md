# griffe-modernized-annotations
![Build status](https://github.com/jonghwanhyeon/griffe-modernized-annotations/actions/workflows/publish.yml/badge.svg)

A Griffe extension that modernizes type annotations by adopting PEP 585 and PEP 604

## Example
Without extension:
![Without Extension](https://github.com/jonghwanhyeon/griffe-modernized-annotations/raw/main/assets/without-extension.png)

With extension:
![With Extension](https://github.com/jonghwanhyeon/griffe-modernized-annotations/raw/main/assets/with-extension.png)

## Install
To install **griffe-modernized-annotations**, simply use pip:

```console
$ pip install griffe-modernized-annotations
```

## Usage
```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          options:
            extensions:
              - griffe_modernized_annotations
```