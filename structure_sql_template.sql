-- Switch to SYSADMIN role for creating database entities
USE ROLE SYSADMIN;

-- 1. Databases and Schemas Setup

-- Creating database and source system schemas
{database_creation}
-- Creating schemas per source system
USE DATABASE raw_prod;
{schema_creation}

-- Creating additional databases and schemas
CREATE DATABASE IF NOT EXISTS analytics_prod;
USE DATABASE analytics_prod;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS dwh;

CREATE DATABASE IF NOT EXISTS analytics_dev;
USE DATABASE analytics_dev;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS dwh;

CREATE DATABASE IF NOT EXISTS analytics_stg;
USE DATABASE analytics_stg;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS dwh;

-- 2. Warehouses Setup
{warehouse_creation}

-- Switch to SECURITYADMIN role for granting permissions to roles
USE ROLE SECURITYADMIN;

-- 3. Roles Setup
{role_creation}

-- Granting roles to schemas and future tables
{grants_statement}

-- Granting sysadmin access to all generated roles
{grant_sysadmin_statements}

-- Granting warehouse access
GRANT USAGE ON WAREHOUSE wh_data_team TO ROLE data_analyst;
GRANT USAGE ON WAREHOUSE wh_data_team TO ROLE data_user;
GRANT ALL PRIVILEGES ON WAREHOUSE wh_ingestion TO ROLE ingestion_tool;
GRANT ALL PRIVILEGES ON WAREHOUSE wh_reporting TO ROLE reporting_tool;
GRANT ALL PRIVILEGES ON WAREHOUSE wh_transformation TO ROLE transformation_tool;
GRANT ALL PRIVILEGES ON WAREHOUSE wh_data_team TO ROLE data_engineer;
GRANT ALL PRIVILEGES ON WAREHOUSE wh_data_team TO ROLE securityadmin;

-- Creating profile roles with specific access permissions
CREATE ROLE IF NOT EXISTS ingestion_tool;
GRANT ROLE raw_prod_read, raw_prod_write TO ROLE ingestion_tool;

CREATE ROLE IF NOT EXISTS reporting_tool;
GRANT ROLE analytics_prod_dwh_read TO ROLE reporting_tool;

CREATE ROLE IF NOT EXISTS transformation_tool;
GRANT ROLE analytics_prod_dwh_read, analytics_prod_dwh_write, analytics_prod_stg_read,analytics_prod_stg_write TO ROLE transformation_tool;
GRANT ROLE analytics_stg_dwh_read, analytics_stg_dwh_write, analytics_stg_stg_read,analytics_stg_stg_write TO ROLE transformation_tool;

CREATE ROLE IF NOT EXISTS data_engineer;
GRANT ROLE analytics_prod_dwh_read,analytics_prod_dwh_write,analytics_prod_stg_read,analytics_prod_stg_write,raw_prod_read,analytics_dev_write, analytics_dev_read
,analytics_stg_dwh_read, analytics_stg_dwh_write, analytics_stg_stg_read,analytics_stg_stg_write
TO ROLE data_engineer;


CREATE ROLE IF NOT EXISTS data_analyst;
GRANT ROLE analytics_dev_read,analytics_prod_dwh_read,analytics_dev_write TO ROLE data_analyst;


CREATE ROLE IF NOT EXISTS data_user;
GRANT ROLE analytics_prod_dwh_read TO ROLE data_user;
GRANT ROLE data_user TO ROLE data_engineer;
GRANT ROLE data_user TO ROLE data_analyst;


-- Creating users with random passwords and MFA configuration
CREATE USER rivery PASSWORD = '{rivery_password}' DEFAULT_ROLE = ingestion_tool DEFAULT_WAREHOUSE = wh_ingestion;
SELECT 'rivery' AS username, '{rivery_password}' AS password;
GRANT ROLE ingestion_tool TO USER rivery;

CREATE USER dbt PASSWORD = '{dbt_password}' DEFAULT_ROLE = transformation_tool DEFAULT_WAREHOUSE = wh_transformation;
SELECT 'dbt' AS username, '{dbt_password}' AS password;
GRANT ROLE transformation_tool TO USER dbt;
