# UIC Attribute Rules

## Setup

1. create local database from sql management studio named `UIC`
1. enable as enterprise gdb via pro

    ```py
    import arcpy
    arcpy.management.EnableEnterpriseGeodatabase(r'...\uic-attribute-rules\pro-project\localhost.sde', r'C:\Program Files\ESRI\License10.6\sysgen\keycodes')
    ```

    _If you receive errors, you may need to execute the following sql_

    ```sql
    ALTER DATABASE UIC
    SET ALLOW_SNAPSHOT_ISOLATION ON

    ALTER DATABASE UIC
    SET READ_COMMITTED_SNAPSHOT ON
    ```

1. import the XML Workspace for the existing UIC database

    ```py
    arcpy.management.ImportXMLWorkspaceDocument(r'...\uic-attribute-rules\pro-project\localhost.sde', r'...\uic-attribute-rules\data\UIC_STAGING.XML', 'SCHEMA_ONLY', None)
    ```

1. Create a python conda workspace for the project

    ```sh
    conda create --clone arcgispro-py3 --name uic
    ```

1. install the development requirements

    ```sh
    pip install -r requirements.dev.txt
    ```

## Database Migrations

### Remove feature dataset

1. Import the individual feature classes contained within the feature datasets
1. Import everything outside the feature dataset

### python migrations

1. update config.py to set correct source
1. run migration code
   - `python migrations.py`

#### What happens

1. removes unused tables
1. unversions tables
1. disables editor tracking
1. adds and removes table fields
1. removes unused domains
1. moves fields from one table to another
1. creates well contingency
1. adds editor tracking
1. versions tables
