# DB Text Extraction

This cli-based tool makes it easy to get the `data` and `set` tables (which hold a lot of the relevant text data) from the SQLite DB. You have options to either export to CSVs or insert into a PostgreSQL Database.

## Usage

Simple start with `python main.py --help`

The CLI rendering is done with [Typer](https://typer.tiangolo.com/)

### For CSVs

```bash
python main.py to-csv
```

This will output to the `data/` folder.

### For PostgreSQL

```bash
python main.py to-pg [OPTIONS] USERNAME PASSWORD SERVER_HOST PORT DB [SCHEMA]
```

This will extract from the SQLite DB and create the tables in PG instead. If you run it again it will, instead, replace those tables so be careful! The `SCHEMA` is optional and will use `public` if you do no specifiy.

I prefer doing work in Postgres vs SQLite so this is what I use.

## Install

As usual I recommend a virtual environment and I, personally, use Poetry as the manager for that. You're welcome to create your own `requirements.txt` but I will not be providing one at this time.
