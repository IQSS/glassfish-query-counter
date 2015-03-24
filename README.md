# Glassfish Query Counter

Count queries printed to the Glassfish logs.  This basically:
 1. Takes the last 'n' lines from the glassfish log file, marked by a logging statement in Java 
 1. Writes the lines to a file
 1. Runs them though the python [collections.Counter](https://docs.python.org/2/library/collections.html#collections.Counter). 
 
Tested on python 2.7.

## I. Set up Glassfish to log queries

### (A) Edit the ```persistence.xml``` file
1.  Open the ```persistence.xml``` file
1.  Add this line to the end of the ```<properties>`` list:
```xml
<property name="eclipselink.logging.level.sql" value="FINE"/>
```
 - Example:
``` xml
<properties>
    <!--property name="toplink.logging.level" value="FINE"/-->
    <property name="eclipselink.weaving" value="false"/>
    <property name="eclipselink.ddl-generation" value="create-tables"/>
    <property name="eclipselink.cache.shared.default" value="false"/>
    <!-- The following property allows primary keys of 0 -->
    <property name="eclipselink.id-validation" value="NULL"/>
    <property name="eclipselink.logging.level.sql" value="FINE"/>
</properties>
```

### (B) For the pages you are interested in, add a logging line
1. Add delimiters to the pages you would like to check.
1. Example: 
   1.  Edit the ```DatasetPage.java```
   1.  Add this line to the top of your ```init(...)``` method:
```java
logger.info("_YE_OLDE_QUERY_COUNTER_")
```
  - Assumes page has a logger as in 
``` java 
private static final Logger logger = Logger.getLogger(DatasetPage.class.getCanonicalName());
```

## II. Update the python settings to point to your Glassfish Log
1. Copy the file ```scripts/settings_template.json``` to ```scripts/settings.json```
1. Update ```scripts/settings.json``` with the path to your Glassfish log file
1. Example:
```json
{ "GLASSFISH_LOG_FILE_PATH" : "/Users/rp/Documents/iqss-git/glassfish4.1/glassfish/domains/domain1/logs/server.log" }
```

## III. Run It

1. Go to the page you would like to check: e.g. ```http://localhost:8080/dataset.xhtml?id=3&versionId=15```
  - The log should continue SQL statements from the page load
1. Run the python script, with the name of an output file:
```
> cd 'glassfish-query-counter/scripts'
> python count_queries.py dataset-page-check
```

- This does the following:
  1.  Creates a text file in: ```query_lists/dataset-page-check.txt```
  1.  Creates a .csv file with query counts: ```query_counts/dataset-page-check.csv```
  1.  Prints output to the terminal

  
  




