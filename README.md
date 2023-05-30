# README: Shapefile to SQL Conversion and Modification

This script allows you to convert a shapefile to an SQL file using the `shp2pgsql` command and perform additional modifications on the generated SQL file. Here's a guide on how to use the script and its command-line arguments.

## Prerequisites
- PostgreSQL/PostGIS should be installed on your system.
- Python 2.7 should be installed.

## Installation

1. Clone the repository or download the script to your local machine.


## Usage
python shapefile_converter.py shape_file [-h] [-i INPUT_FILE] [-o OUTPUT_FILE] [-O OUTPUT_FOLDER]
[-s SCHEMA] [-d DATABASE] [-t TABLE] [-r REMOVECOLUMNS]
[-m MAPPINGCOLUMNS] [-T TIMES]

### Arguments

- `shape_file` (required): Path to the shapefile that you want to convert to SQL.

Optional arguments:

- `-i, --input_file`: Path to the input SQL file. Default: `shp2pgsql_init.sql`.

- `-o, --output_file`: Path to the output SQL file. Default: `output.sql`.

- `-O, --output_folder`: Folder path to the output SQL files. Default: `outputs`.

- `-s, --schema`: Database schema. Default: `transportiq`.

- `-d, --database`: Database name. Default: `iq-map`.

- `-t, --table`: Table name. Default: `ADABoundary`.

- `-r, --removeColumns`: Columns names to remove. Default: `bufferdist`.

- `-m, --mappingColumns`: Customize column names using the format `<shpCol>:<tableCol>`, separated by commas if multiple mappings are needed. Default: `id:name`.

- `-T, --times`: File-related times to set.

### Example Usage
To convert a shapefile named `my_shapefile.shp` to an SQL file, perform modifications, and specify the output file and table name, you can use the following command:

python shapefile_converter.py my_shapefile.shp -o modified_output.sql -t MyTable -r column1,column2 -m shape_col:table_col1,name_col:table_col2

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to contribute or report any issues on the [GitHub repository](https://github.com/LouiLu/).
