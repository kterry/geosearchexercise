# geosearchexercise

Find a restaurant near a post code.

## Setup

The program requires two CSV files to work:
* A post codes coordinates file (see `resources/postcodes_swift_sample.csv`)
* A restaurant post codes file (see `resources/pubnames_swift_sample.csv`)

The configuration file `geofinder.ini` can be edited to change the path of the files.
```
[files]
postcodes = <path to post codes file>
restaurants = <path to restaurants file>
```

## Usage

The program is a command line Python application with the following syntax:

```
$ ./findmyrestaurant.py [-h] [-d DISTANCE] [-p] <postcode>
```

Arguments:
* `postcode`: Post code to search.
* `-d|--distance`: max distance on metres from the given postal code.
* `-p|--pretty-print`: Pretty print output.
* `-h|--help`: Show help.

The output is printed as a list of restaurants and distances to the post code in metres separated by a tab.

# Run tests

To run the tests run the following command:
```
$ python geofinder_test.py 
```
