# UIC Attribute Rules

## Setup

1. create local database from sql management studio named `UIC`
1. enable as enterprise gdb via pro

    ```py
    arcpy.management.EnableEnterpriseGeodatabase(r'...\uic-attribute-rules\pro-project\localhost.sde', r'C:\Program Files\ESRI\License10.6\sysgen\keycodes')
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
