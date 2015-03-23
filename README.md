# Glassfish Query Counter

Count queries printed to the Glassfish logs.  Tested on python 2.7.

## Set up Glassfish to log queries

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

### (B) Edit the ```persistence.xml``` file
1. Add a delimiters to the pages you would like to check.
1. Example: 
   1.  Edit the ```DatasetPage.java```
   1.  Add this line to the top of your ```init(...)``` method:
```java
logger.info("____QUERY_DEBUG____")
```




