# Databricks notebook source
# MAGIC %md
# MAGIC # Demonstração
# MAGIC ## Como ler tabelas do Unity Catalog no Trino

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Write a Delta Table in UC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG iceberg_catalog;

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG iceberg_catalog;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE DATABASE IF NOT EXISTS demo;
# MAGIC USE DATABASE demo;

# COMMAND ----------

# MAGIC %sql
# MAGIC --DROP TABLE IF EXISTS trino;
# MAGIC
# MAGIC -- https://docs.databricks.com/en/delta/uniform.html
# MAGIC -- Databricks Runtime 14.3 LTS or above
# MAGIC CREATE TABLE trino (texto string) 
# MAGIC TBLPROPERTIES (
# MAGIC     'delta.enableIcebergCompatV2' = 'true',
# MAGIC     'delta.universalFormat.enabledFormats' = 'iceberg'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC -- In Databricks Runtime 15.4 LTS and above
# MAGIC ALTER TABLE trino SET TBLPROPERTIES(
# MAGIC   'delta.enableIcebergCompatV2' = 'true',
# MAGIC   'delta.universalFormat.enabledFormats' = 'iceberg'
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED trino;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO trino VALUES ("Hello Trino from Delta")

# COMMAND ----------

import os
os.environ["WORKSPACE"] = "<WORKSPACE>" # indicar o workspace aqui
os.environ["TOKEN"] = dbutils.entry_point.getDbutils().notebook().getContext().apiToken().get() # criar o PAT antes

# COMMAND ----------

# MAGIC %sh
# MAGIC curl -X GET -H "Authentication: Bearer $TOKEN" -H "Accept: application/json" https://${WORKSPACE}/api/2.1/unity-catalog/iceberg/v1/catalogs/iceberg_catalog/namespaces/demo/tables/trino

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Create an Iceberg table with a catalog integration
# MAGIC executar os comandos abaixo no Trino

# COMMAND ----------

"""

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

"""

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Read the table
# MAGIC executar os comandos abaixo no Trino

# COMMAND ----------

"""

show catalogs;
show schemas in iceberg_catalog;
use iceberg_catalog.demo;
show tables;
select * from trino;

"""


# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Insert new records

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO iceberg_catalog.demo.trino VALUES ("Inserindo novo registro na tabela v3")