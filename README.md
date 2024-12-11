# Trino Iceberg Integration with Databricks

This repository demonstrates how to integrate Trino using Iceberg REST Catalog on Unity Catalog Databricks.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Databricks Notebook](#databricks-notebook)
4. [Trino Configuration](#trino-configuration)
5. [Usage](#usage)

## Prerequisites

* Databricks Runtime 14.3 LTS or above
* Trino installed and configured
* Unity Catalog enabled on your Databricks workspace

## Setup

### Step 1: Create a Delta table in UC

To create a Delta table in the Unity Catalog, follow these steps:

1. Run the `CREATE CATALOG` command to create a new catalog (optional)
2. Run the `CREATE DATABASE` command to create a new schema (optional)
3. Use the catalog and database you created.

```sql
CREATE CATALOG iceberg_catalog;
USE CATALOG iceberg_catalog;
CREATE DATABASE IF NOT EXISTS demo;
USE DATABASE demo;
```

4. Create a Delta table with the desired schema, setting Iceberg properties

```sql
CREATE TABLE trino (texto string) 
TBLPROPERTIES (
    'delta.enableIcebergCompatV2' = 'true',
    'delta.universalFormat.enabledFormats' = 'iceberg'
);
```

### Step 2: Configure Trino

To configure Trino, follow these steps:

1. Create a catalog integration using the `CREATE CATALOG` command.
2. Set the required properties for the catalog integration.

```sql
CREATE CATALOG iceberg_catalog USING iceberg WITH (
  "iceberg.catalog.type" = 'rest',
  "iceberg.rest-catalog.uri" = 'https://<WORKSPACE>/api/2.1/unity-catalog/iceberg',
  "iceberg.security" = 'read_only',
  "iceberg.rest-catalog.security" = 'OAUTH2',
  "iceberg.rest-catalog.oauth2.token" = '< PAT TOKEN >',
  "iceberg.rest-catalog.warehouse" = 'iceberg_catalog',
  "iceberg.rest-catalog.vended-credentials-enabled" = 'true',
  "fs.native-s3.enabled" = 'true',
  "s3.region" = 'us-west-2'
);
```

### Step 3: Read the table

To read data from Trino, use the `SELECT` statement.

```sql
SELECT * FROM trino;
```

## Usage

This repository provides a basic example of how to integrate Trino with Delta Lake using Iceberg REST Catalog on Databricks. You can modify and extend this code to suit your specific use case.

### Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

### License

This project is licensed under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license.
```

You can modify this `README.md` file as needed to fit your specific use case and project requirements.