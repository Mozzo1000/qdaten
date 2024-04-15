# Q.Daten
<img src="https://img.shields.io/badge/maintenance-under%20development-informational"/>


Q.Daten (qdaten) is a command line application enabling you to run SQL queries against a CSV file. It starts by converting your CSV file into a SQLite database, you can then run SQL queries against the database in either interative TUI or non-interative mode. You can also open existing SQLite databases.

## Usage
**Open CSV file with the delimiter set to `;` in interative mode**
```bash
qdaten example.csv --delimiter=";"
```

**Run query in non-interative mode**
```bash
qdaten example.csv -c="SELECT * FROM table LIMIT 10" 
```

**Open SQLite in interactive mode**
```bash
qdaten example.db --file-type=sqlite" 
```

### Interactive mode built-in commands
While inside the interactive terminal, there are a few built-in commands that you can run besides normal sql queries.

| Command       | Result                       | 
| ------------- |:----------------------------:|
| exit          | Exit interactive mode        |
|.tables        | Get a list of all tables     |
|.save          | Save to SQLite database file |

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

Q.Daten is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.