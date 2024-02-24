# Q.Daten

Q.Daten (qdaten) is a command line application enabling you to run SQL queries against a CSV file.

## Usage
**Open CSV file with the delimiter set to `;` in interative mode**
```bash
qdaten example.csv --delimiter=";"
```

**Run query in non-interative mode**
```bash
qdaten example.csv -c="SELECT * FROM table LIMIT 10" 
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

Q.Daten is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the full license text.