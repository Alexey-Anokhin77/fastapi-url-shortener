# FastAPI URL Shortener

## Develop

Setup:

Right click `url-shortener` -> Mark directory as -> Sources root

### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

### Install

Install packages:
```shell
uv install
```


### Run

Go to workdir:
```shell
cd url-shortener
```

Run dev server
```shell
fastapi dev
```

## Snippets
```shell
python -c "import secrets;print(secrets.token_urlsafe(16))"
```
