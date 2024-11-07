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

-- 3. Warehouses Setup
{warehouse_creation}

-- Switch to SECURITYADMIN role for granting permissions to roles
USE ROLE SECURITYADMIN;

-- 2. Roles Setup
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
GRANT ROLE raw_prod_read TO ROLE ingestion_tool;
GRANT ROLE raw_prod_write TO ROLE ingestion_tool;
CREATE ROLE IF NOT EXISTS reporting_tool;
GRANT ROLE analytics_prod_dwh_read TO ROLE reporting_tool;
CREATE ROLE IF NOT EXISTS transformation_tool;
GRANT ROLE analytics_prod_dwh_read TO ROLE transformation_tool;
GRANT ROLE analytics_prod_dwh_write TO ROLE transformation_tool;
GRANT ROLE analytics_prod_stg_read TO ROLE transformation_tool;
GRANT ROLE analytics_prod_stg_write TO ROLE transformation_tool;
CREATE ROLE IF NOT EXISTS data_engineer;
GRANT ROLE analytics_prod_dwh_read TO ROLE data_engineer;
GRANT ROLE analytics_prod_dwh_write TO ROLE data_engineer;
GRANT ROLE analytics_prod_stg_read TO ROLE data_engineer;
GRANT ROLE analytics_prod_stg_write TO ROLE data_engineer;
GRANT ROLE raw_prod_read TO ROLE data_engineer;
CREATE ROLE IF NOT EXISTS data_analyst;
GRANT ROLE analytics_dev_read TO ROLE data_analyst;
GRANT ROLE analytics_prod_dwh_read TO ROLE data_analyst;
GRANT ROLE analytics_dev_write TO ROLE data_analyst;
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

-- Additional user creation examples
-- CREATE USER data_engineer_user PASSWORD = '{data_engineer_password}' DEFAULT_ROLE = data_engineer DEFAULT_WAREHOUSE = wh_data_team MUST_CHANGE_PASSWORD = TRUE MFA_ENABLED = TRUE;
-- SELECT 'data_engineer_user' AS username, '{data_engineer_password}' AS password;
-- GRANT ROLE data_engineer TO USER data_engineer_user;

-- Security configurations (optional)
-- Uncomment to enforce stricter data security settings
-- ALTER ACCOUNT SET REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION = TRUE;
-- ALTER ACCOUNT SET PREVENT_UNLOAD_TO_INLINE_URL = TRUE;
