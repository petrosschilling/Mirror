# Mirror

This is a framework to help to check consistency of database data between two different tables whether or not they are in the same database.

# Usage

The steps are as follow:
1. Configure database connection(s)
2. Mapping tables columns
    1. Configure uinique identifiers (UIDs)
    2. Filters
    3. Functions


## Configure database connection(s)

To compare two tables you need first to create the Database Configuration to access the database. If you are comparing tables from two distinct databases you will need to create two configurations.

To create a Database Configuration you use the class `dba.DBConfiguration`.

```python
from dba import DBConfiguration

config = DBConfiguration()
config.usr = "dbuser"
config.pwd = "dbpassword"
config.host = "dbip"
config.databse = "dbname"
```

## Mapping tables columns

To check whether or not the columns have the same value we must create a map from the first table columns to the second table columns.

The `Mirror` uses an array of `mirror.FieldLink` object to do the mapping.

Let's consider we have the followig structure in the tables we want to compare:

### First table

#### person
id | name | gender
-- | ---- | ------
1 | John Doe | M
2 | Peter Chan | M
3 | Catherine Mustache | F

### Second table

#### person
id | full_name | gender
-- | ---- | ------
1 | John Doe | Male
2 | Peter Chan | Male
3 | Catherine Mustache | Female

The configuration for a table like this would be:

```python
from dba import FieldLink

links = [
    FieldLink("id", "id"),
    FieldLink("name", "full_name"),
    FieldLink("gender", "gender")
]
```

### Cofigure unique identifiers (UIDs)

To successfully compare the data from the tables, the `Mirror` must know what makes a record in your table unique and these values must match in both tables.
> In this example we only have the `id` column to distinguish the records. Its preferrable to avoid using it. If not possible you need to make sure the `id` values match for each record. Preferrably use fields that are unique but there is no chance that they will cahnge from one table to another like `username` or `email`.

To do this you just need to set the property `uid` to `True` in the field link constructor.

```python
links = [
    FieldLink("id", "id", uid=True),
    FieldLink("name", "full_name"),
    FieldLink("gender", "gender")
]
```

You can also have more than one field as `uid` e.g.:

```python
links = [
    FieldLink("id", "id", uid=True),
    FieldLink("email", "email", uid=True),
    FieldLink("name", "full_name"),
    FieldLink("gender", "gender")
]
```

> What we ar looking for here is to find what makes that record unique trying to ignore the auto generated id field whenever possible.

### Filters

When comparing data from two distinct tables you may want to compare just a small dataset of the whole table.
For this you can use the `filterr` property when initializing your link.

Let's say you only want to compare records of the Male gender:

```python
links = [
    FieldLink("id", "id", uid=True),
    FieldLink("name", "full_name"),
    FieldLink("gender", "gender", filterr=True, filter1_val="M", filter2_val="Male")
]
```

### Functions

You may have noted that the value of `gender` in both tables are different. In this case we will always have a negative when comparing this two tables.
To be able to get a positive when comparing these values you can create a custom function that will take the column value as an argument and pass it in the `FieldLink` constructor.

```python
def gender_parser(val):
    if val == "M":
        return "Male"
    elif val == "F":
        return "Female"
    else:
        return val

links = [
    FieldLink("id", "id", uid=True),
    FieldLink("name", "full_name"),
    FieldLink("gender", "gender", func1=gender_parser)
]
```

> You also have the option of parsing the values of the second table using the `func2` argument. This is very unlikely to be used but it is there in case both values need to be converted to something else for comparison.

# The gran finale

After creating the DBConfigurations and all the neccessary links we need the create the `Mirror` object which is who does all the work.

```python
mirror = Mirror(config, config, "Person", "person", links) # Tables are in the same database since we are using the same configuration.
mirror.run_diff()
mirror.to_csv() # Export all the unmatched found to csv file in current directory