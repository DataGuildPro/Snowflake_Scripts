import random
import string

"""
This code creates a sql template file (structure_sql_output.sql) that you can run in order to setup snowflakes initial structure.
The placeholder lists hold names for- databases, schemas, warehouses and roles to create. 

Some specific setups are defined under structure_sql_template.sql:
* Creating profile roles with specific access permissions
* Creating schemas: dwh, stg for databases analytics_prod and analytics_dev
* Granting warehouse access
* Creating users with random passwords and MFA configuration (for users - rivery, dbt)

 
"""
# Placeholder lists
databases = ["raw_prod", "analytics_prod", "analytics_dev","analytics_stg"]
#schemas that appear here will get raw_prod_read access and raw_prod_write access.
# If there is a schema that shouldn't get these privileges omit it from the following list and add its specificaly to - structure_sql_template.sql
raw_prod_schemas = ["honest_fulphilment",
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
    "data_engineer", "data_analyst", "data_user", "analytics_stg_dwh_read", "analytics_stg_dwh_write", "analytics_stg_stg_read",
    "analytics_stg_stg_write",
]

# Function to generate a random password
def generate_random_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))


# Generate database creation statements
database_creation_statements = "\n".join([f"CREATE DATABASE IF NOT EXISTS {database};" for database in databases])
# Generate schema creation statements
schema_creation_statements = "\n".join([f"CREATE SCHEMA IF NOT EXISTS {schema};" for schema in raw_prod_schemas])

# Generate warehouse creation statements
warehouse_creation_statements = "\n".join(
    [f"CREATE WAREHOUSE IF NOT EXISTS {warehouse} WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE;"
     for warehouse in warehouses]
)

grant_roles = [("raw_prod","raw_prod_write"),("raw_prod","raw_prod_read")
,("analytics_prod","analytics_prod_dwh_read"),("analytics_prod","analytics_prod_dwh_write"),
("analytics_prod","analytics_prod_stg_read"),("analytics_prod","analytics_prod_stg_write"),
("analytics_stg","analytics_stg_dwh_read"),("analytics_stg","analytics_stg_dwh_write"),
("analytics_stg","analytics_stg_stg_read"),("analytics_stg","analytics_stg_stg_write"),
("analytics_dev","analytics_dev_read"),("analytics_dev","analytics_dev_write")]

grant_write_roles = [("analytics_prod","analytics_prod_dwh_write"),
("analytics_prod","analytics_prod_stg_write"),
("analytics_stg","analytics_stg_dwh_write"),
("analytics_stg","analytics_stg_stg_write"),
("analytics_dev","analytics_dev_write")]

grant_read_roles = [("raw_prod","raw_prod_read")
,("analytics_prod","analytics_prod_dwh_read"),
("analytics_prod","analytics_prod_stg_read"),
("analytics_stg","analytics_stg_dwh_read"),
("analytics_stg","analytics_stg_stg_read"),
("analytics_dev","analytics_dev_read")]


grant_write_statements = ("GRANT CREATE SCHEMA, MONITOR, USAGE on database raw_prod to ROLE raw_prod_write;\n" +
                            "\n".join([f"GRANT USAGE ON DATABASE {db} TO ROLE {role};\n"
                                       f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {db} TO ROLE {role};\n"
                                        f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {db} to ROLE {role};\n"    
                                        f"GRANT ALL on DATABASE {db} to ROLE {role};\n"
                                        f"GRANT ALL on all SCHEMAS IN DATABASE {db} to ROLE {role};\n"
                                        f"GRANT ALL on ALL TABLES IN DATABASE {db} to ROLE {role};\n"
                                        f"GRANT ALL on ALL VIEWS IN DATABASE {db} to ROLE {role};\n"                                 
                                        f"GRANT ALL ON FUTURE SCHEMAS IN DATABASE {db} to ROLE {role};\n"                                                                
                                        f"GRANT ALL ON FUTURE TABLES IN DATABASE {db} TO ROLE {role};\n"
                                        f"GRANT ALL ON FUTURE VIEWS IN DATABASE {db} TO ROLE {role};\n"
                                       for db, role in grant_write_roles]))
# for raw_prod_write - we want to give the privileges to a specific list of schemas
# this is because there are cases where a schema in this db needs restricted access, therefore we don't want to automatically give write privileges to all schemas.
# if there is such a case please add the role and schema (creation and privileges) explicitly and don't add it to the list - raw_prod_schemas .

grant_raw_prod_write_statement = (f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE raw_prod to ROLE raw_prod_write;\n"
                                  + "\n".join(
                                [f"GRANT USAGE ON SCHEMA raw_prod.{schema} TO ROLE raw_prod_read;\n"
                                 f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA raw_prod.{schema} TO ROLE raw_prod_write;\n"
                                 f"GRANT ALL PRIVILEGES ON ALL VIEWS IN SCHEMA raw_prod.{schema} TO ROLE raw_prod_write;\n"
                                 f"GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA raw_prod.{schema} TO ROLE raw_prod_write;\n"
                                 f"GRANT ALL PRIVILEGES ON FUTURE VIEWS IN SCHEMA raw_prod.{schema} TO ROLE raw_prod_write;\n"
                                 for schema in raw_prod_schemas]))

grant_read_statements = (" \n".join([f"GRANT USAGE ON DATABASE {db} TO ROLE {role};\n"
                                        f"GRANT USAGE ON ALL SCHEMAS IN DATABASE {db} TO ROLE {role};\n"
                                        f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {db} to ROLE {role};\n"    
                                        f"GRANT select on ALL TABLES IN DATABASE {db} to ROLE {role};\n"
                                        f"GRANT select on ALL VIEWS IN DATABASE {db} to ROLE {role};\n"                                 
                                        f"GRANT select ON FUTURE TABLES IN DATABASE {db} TO ROLE {role};\n"
                                        f"GRANT select ON FUTURE VIEWS IN DATABASE {db} TO ROLE {role};\n"
                                       for db, role in grant_read_roles]))
# grants_statements = ("GRANT CREATE SCHEMA, MONITOR, USAGE on database raw_prod to ROLE raw_prod_write;" +
#                             "\n".join([f"GRANT USAGE ON DATABASE {db} TO ROLE {role};\n"
#                                         f"GRANT USAGE ON FUTURE SCHEMAS IN DATABASE {db} to ROLE {role};\n"
#                                         f"GRANT ALL on DATABASE {db} to ROLE {role};\n"
#                                         f"GRANT ALL on all SCHEMAS IN DATABASE {db} to ROLE {role};\n"
#                                         f"GRANT ALL on ALL TABLES IN DATABASE {db} to ROLE {role};\n"
#                                         f"GRANT ALL on ALL VIEWS IN DATABASE {db} to ROLE {role};\n"
#                                         f"GRANT ALL ON FUTURE SCHEMAS IN DATABASE {db} to ROLE {role};\n"
#                                         f"GRANT SELECT ON FUTURE TABLES IN DATABASE {db} TO ROLE {role};\n"
#
#                                        for db, role in grant_roles]))
# Generate role creation and grant statements
role_creation_statements = "\n".join([f"CREATE ROLE IF NOT EXISTS {role};" for role in roles])



# Granting sysadmin access to all generated roles
grant_sysadmin_statements = "\n".join([f"GRANT ROLE {role} TO ROLE sysadmin;" for role in roles])

# Generate random passwords for each user
passwords = {
    "rivery_password": generate_random_password(),
    "dbt_password": generate_random_password()
    # "data_engineer_password": generate_random_password(),
    # "data_analyst_password": generate_random_password(),
    # "data_user_password": generate_random_password()
}

if __name__ == "__main__":
# Read the template and replace placeholders
    with open('structure_sql_template.sql', 'r') as file:
        sql_template = file.read()

    # Format the SQL script with placeholders
    sql_script = sql_template.format(
        database_creation=database_creation_statements,
        schema_creation=schema_creation_statements,
        warehouse_creation=warehouse_creation_statements,
        role_creation=role_creation_statements,
        grants_statement=grant_read_statements + grant_write_statements + grant_raw_prod_write_statement,
        grant_sysadmin_statements=grant_sysadmin_statements,
        **passwords
    )

    # Write the generated SQL script to a file
    with open("structure_sql_output.sql", "w") as f:
        f.write(sql_script)

    print("SQL script generated and saved to structure_sql_output.sql")
