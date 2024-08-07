import marimo

__generated_with = "0.7.2"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import sqlalchemy as alc
    import psycopg2 as ps
    import duckdb
    return alc, duckdb, mo, pd, ps


@app.cell
def __(mo):
    _df = mo.sql(
        f"""
        ATTACH 'dbname=testDB host=localhost user=postgres password=postgres port=5432' AS testDB (TYPE POSTGRES);
        """
    )
    return


@app.cell
def __(mo):
    _df = mo.sql(
        f"""
        show all tables;
        """
    )
    return


@app.cell
def __():
    return


@app.cell
def __(mo):
    _df = mo.sql(
        f"""
        INSERT INTO testDB.public.test_survey (question1, question2, code) VALUES ('hello', 'goodbye", 1234);
        """
    )
    return


if __name__ == "__main__":
    app.run()
