# FastAPI URL Shortener

## Develop

Check GitHub Actions after any push.

Setup:

Right click `url-shortener` -> Mark directory as -> Sources root

### Install dependencies
### Configure pre-commit

Install pre-commit hook:
```shell
pre-commit install
```

Install all packages:
```shell
uv sync
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
