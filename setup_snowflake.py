import random
import string

# Placeholder lists
databases = ["raw_prod", "analytics_prod", "analytics_dev"]
schemas = [
    "mysql", "stripe", "paypal", "shopify", "impact", "payoneer", "mongo", "mixpanel",
    "google_ads", "meta", "bing", "tiktok", "elastic_search", "ga4", "hubspot",
    "priority", "jira", "chargeflow", "connecteam", "userpilot", "trustpilot",
    "justt", "typeform", "youtube"
]
warehouses = ["wh_ingestion", "wh_transformation", "wh_reporting", "wh_data_team"]
roles = [
    "raw_prod_read", "raw_prod_write", "analytics_dev_read", "analytics_dev_write",
    "analytics_prod_dwh_read", "analytics_prod_dwh_write", "analytics_prod_stg_read",
    "analytics_prod_stg_write", "ingestion_tool", "reporting_tool", "transformation_tool",
    "data_engineer", "data_analyst", "data_user"
]

# Function to generate a random password
def generate_random_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))


# Generate database creation statements
database_creation_statements = "\n".join([f"CREATE DATABASE IF NOT EXISTS {database};" for database in databases])
# Generate schema creation statements
schema_creation_statements = "\n".join([f"CREATE SCHEMA IF NOT EXISTS {schema};" for schema in schemas])

# Generate warehouse creation statements
warehouse_creation_statements = "\n".join(
    [f"CREATE WAREHOUSE IF NOT EXISTS {warehouse} WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;"
     for warehouse in warehouses]
)

# Generate role creation and grant statements
role_creation_statements = "\n".join([f"CREATE ROLE IF NOT EXISTS {role};" for role in roles])

grants_statements = """GRANT CREATE SCHEMA, MONITOR, USAGE on database raw_prod to ROLE raw_prod_write;
GRANT ALL on all SCHEMAS IN DATABASE raw_prod to ROLE raw_prod_write;
GRANT ALL on ALL TABLES IN DATABASE raw_prod to ROLE raw_prod_write;"""

# Granting sysadmin access to all generated roles
grant_sysadmin_statements = "\n".join([f"GRANT ROLE {role} TO ROLE sysadmin;" for role in roles])

# Generate random passwords for each user
passwords = {
    "rivery_password": generate_random_password(),
    "dbt_password": generate_random_password(),
    "data_engineer_password": generate_random_password(),
    "data_analyst_password": generate_random_password(),
    "data_user_password": generate_random_password()
}

# Read the template and replace placeholders
with open('structure_sql_template.sql', 'r') as file:
    sql_template = file.read()

# Format the SQL script with placeholders
sql_script = sql_template.format(
    database_creation=database_creation_statements,
    schema_creation=schema_creation_statements,
    warehouse_creation=warehouse_creation_statements,
    role_creation=role_creation_statements,
    grants_statement=grants_statements,
    grant_sysadmin_statements=grant_sysadmin_statements,
    **passwords
)

# Write the generated SQL script to a file
with open("structure_sql_output.sql", "w") as f:
    f.write(sql_script)

print("SQL script generated and saved to structure_sql_output.sql")
