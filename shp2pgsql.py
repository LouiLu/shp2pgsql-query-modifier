import re
import argparse
import psycopg2
import subprocess
from datetime import datetime

def set_columns(query, removeColumns, timesColumns, mappingColumns, schema, table):
    	# Extract the objects within parentheses using regular expressions
	objects_array = re.findall(r'\((.*?)\)', query)
	extra_time_columns = ['"startTime"', '"endTime"', '"startDate"', '"endDate"']
	extra_time_values = ["'" + timesColumns['startTime'] + "'", "'" + timesColumns['endTime'] + "'", "'"+ timesColumns['startDate'] +"'", "'"+timesColumns['endDate']+"'"]

	# Process each object to remove leading/trailing whitespace and split into individual items
	if len(objects_array) > 0:
		keys_array = objects_array[0].split(',')
		values_array = objects_array[1].split(',')

		# Mapping columns name as needed
		if len(mappingColumns) > 0:
			for origin_column in mappingColumns:
				origin_column_name = '"'+ origin_column +'"' if origin_column != 'geom' else origin_column
				origin_column_index = keys_array.index(origin_column_name)
				keys_array[origin_column_index] = '"'+mappingColumns[origin_column]+'"'
				print('Mapped ' + origin_column + ' to ' + keys_array[origin_column_index])

		# Remove columns
		for remove_column in removeColumns:
			remove_column_name = '"'+ remove_column +'"' if remove_column != 'geom' else remove_column
			try:
				column_index = keys_array.index(remove_column_name)
			except ValueError:
				continue
			keys_array.pop(column_index)
			values_array.pop(column_index)
			print('Removed ' + remove_column)

		# Add table needed columns
		keys_array += extra_time_columns
		values_array += extra_time_values
		modified_query = 'INSERT INTO '+ schema + '."' + table+ '" (' + ', '.join(keys_array) + ')' + ' VALUES (' + ', '.join(values_array) + ')'
		return modified_query

	return query

# Read params from command line
# Set up command-line argument parser
current_datetime = datetime.now()
print('Start generating SQL script at '+ current_datetime.isoformat())
parser = argparse.ArgumentParser()
parser.add_argument('shape_file', help='Path to the shapefile')
parser.add_argument('-i', '--input_file', help='Path to the input SQL file', default='shp2pgsql_init.sql')
parser.add_argument('-o', '--output_file', help='Path to the output SQL file', default='output.sql')
parser.add_argument('-O', '--output_folder', help='Folder path to the output SQL files', default='outputs')
parser.add_argument('-H', '--host', help='Database host', default='localhost')
parser.add_argument('-U', '--user', help='Database user', default='xxx')
parser.add_argument('-P', '--password', help='Database password', default='xxx')
parser.add_argument('-p', '--port', help='Database port', default=5432)
parser.add_argument('-s', '--schema', help='Database schema', default='transportiq')
parser.add_argument('-d', '--database', help='Database name', default='iq-map')
parser.add_argument('-t', '--table', help='Table name', default='ADABoundary')
parser.add_argument('-r', '--removeColumns', help='Columns name to remove', default='bufferdist,count')
parser.add_argument('-m', '--mappingColumns', help='Customize column name, using format <shpCol>:<tableCol> and separated with comma if multiple mapping needed', default='id:name')
parser.add_argument('-T', '--times', help='File related times to set')
parser.add_argument('-f', '--forward', help='Forward importing generated sql file to database', action='store_true')
args = parser.parse_args()

# Generate init insert query by using shp2pgsql
command = ['shp2pgsql', '-a', '-s', '4326', '-g', 'geom', args.shape_file, args.schema + '.' + args.table]

# Execute the shp2pgsql command
process1 = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
shp2pgsql_output, _ = process1.communicate()

# Write the modified SQL query to a file
with open(args.output_folder + '/' + args.input_file, 'w') as file:
    file.write(shp2pgsql_output.decode('utf-8'))

# Read the init query from the input file
with open(args.output_folder + '/' + args.input_file, 'r') as file:
    sql_queries = file.read()

# Manipulate the SQL queries
columns_to_remove = args.removeColumns.split(',')
columns_mapping_pairs = args.mappingColumns.split(',')
shapefile_times = args.times.split(',') if type(args.times) != type(None) else {}
shapefile_times_columns = ['startDate', 'endDate', 'startTime', 'endTime']

extra_times_column = {}
if len(shapefile_times) > 0:
	extra_times_column = [{k: v} for k, v in zip(shapefile_times_columns, shapefile_times)]
else:
	extra_times_column['startDate'] = current_datetime.isoformat()
	extra_times_column['endDate'] = current_datetime.isoformat()
	extra_times_column['startTime'] = '00:00:00'
	extra_times_column['endTime'] = '23:59:59'

# Iterate over the pairs and split them by the colon sign
columns_mapping = {}
for pair in columns_mapping_pairs:
    key, value = pair.split(':')
    columns_mapping[key] = value

modified_queries = []
for query in sql_queries.split(';'):
    query = query.strip()
    if query.startswith("INSERT INTO"):
        # Manipulate the query
        modified_query = query
        modified_query = set_columns(modified_query, columns_to_remove, extra_times_column, columns_mapping, args.schema, args.table)
        modified_queries.append(modified_query)
    elif query.startswith("ANALYZE"):
        modified_queries.append('ANALYZE ' + args.schema + '."' + args.table + '"')
    else:
        modified_queries.append(query)

# Write the modified queries to a new SQL file
with open(args.output_folder + '/' + args.output_file, 'w') as file:
    for query in modified_queries:
        file.write(query + ";\n")

print('SQL file generated in file '+ args.output_file)

print('Start import shapefile to database '+ args.schema + '.' + args.database)
try:
	# Connect to the database
    conn = psycopg2.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )

    if args.forward:
        # Open and read the SQL file
        with open(args.output_folder + '/' + args.output_file, 'r') as sql_file:
            sql_commands = sql_file.read()

        # Execute the SQL commands
        cursor = conn.cursor()
        cursor.execute(sql_commands)
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()
        print('Shapefile been imported successfully')

except (psycopg2.Error, FileNotFoundError) as e:
    print("An error occurred while importing the SQL file to database:")
    print(str(e))