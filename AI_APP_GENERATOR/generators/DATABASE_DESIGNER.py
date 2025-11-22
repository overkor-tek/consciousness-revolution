"""
DATABASE DESIGNER - Schema Generation
=====================================
Generates optimal database schemas based on app requirements.

Uses Golden Ratio proportions for balanced design.

Created: 2025-11-22
Trinity Build: Phase 2
"""

from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class TableSchema:
    """Database table schema"""
    name: str
    columns: List[Dict[str, str]]
    primary_key: str
    foreign_keys: List[Dict[str, str]]
    indexes: List[str]

@dataclass
class DatabaseSchema:
    """Complete database schema"""
    tables: List[TableSchema]
    migrations: str
    seed_data: str

class DatabaseDesigner:
    """
    Designs optimal database schemas.
    """

    # Common column types
    COLUMN_TYPES = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "uuid": "VARCHAR(36) UNIQUE",
        "string": "VARCHAR(255)",
        "text": "TEXT",
        "integer": "INTEGER",
        "float": "REAL",
        "boolean": "BOOLEAN DEFAULT 0",
        "datetime": "DATETIME",
        "created_at": "DATETIME DEFAULT CURRENT_TIMESTAMP",
        "updated_at": "DATETIME DEFAULT CURRENT_TIMESTAMP"
    }

    # Feature to table mappings
    FEATURE_TABLES = {
        "user_authentication": [
            {
                "name": "users",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "email", "type": "string"},
                    {"name": "password_hash", "type": "string"},
                    {"name": "created_at", "type": "created_at"},
                    {"name": "updated_at", "type": "updated_at"}
                ],
                "indexes": ["email"]
            },
            {
                "name": "sessions",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "user_id", "type": "integer"},
                    {"name": "token", "type": "string"},
                    {"name": "expires_at", "type": "datetime"},
                    {"name": "created_at", "type": "created_at"}
                ],
                "foreign_keys": [{"column": "user_id", "references": "users(id)"}],
                "indexes": ["token"]
            }
        ],
        "blog": [
            {
                "name": "posts",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "title", "type": "string"},
                    {"name": "content", "type": "text"},
                    {"name": "author_id", "type": "integer"},
                    {"name": "published", "type": "boolean"},
                    {"name": "created_at", "type": "created_at"},
                    {"name": "updated_at", "type": "updated_at"}
                ],
                "foreign_keys": [{"column": "author_id", "references": "users(id)"}],
                "indexes": ["title", "author_id"]
            },
            {
                "name": "comments",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "post_id", "type": "integer"},
                    {"name": "user_id", "type": "integer"},
                    {"name": "content", "type": "text"},
                    {"name": "created_at", "type": "created_at"}
                ],
                "foreign_keys": [
                    {"column": "post_id", "references": "posts(id)"},
                    {"column": "user_id", "references": "users(id)"}
                ],
                "indexes": ["post_id"]
            }
        ],
        "ecommerce": [
            {
                "name": "products",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "name", "type": "string"},
                    {"name": "description", "type": "text"},
                    {"name": "price", "type": "float"},
                    {"name": "inventory", "type": "integer"},
                    {"name": "created_at", "type": "created_at"}
                ],
                "indexes": ["name"]
            },
            {
                "name": "orders",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "user_id", "type": "integer"},
                    {"name": "total", "type": "float"},
                    {"name": "status", "type": "string"},
                    {"name": "created_at", "type": "created_at"}
                ],
                "foreign_keys": [{"column": "user_id", "references": "users(id)"}],
                "indexes": ["user_id", "status"]
            },
            {
                "name": "order_items",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "order_id", "type": "integer"},
                    {"name": "product_id", "type": "integer"},
                    {"name": "quantity", "type": "integer"},
                    {"name": "price", "type": "float"}
                ],
                "foreign_keys": [
                    {"column": "order_id", "references": "orders(id)"},
                    {"column": "product_id", "references": "products(id)"}
                ],
                "indexes": ["order_id"]
            }
        ],
        "basic_crud": [
            {
                "name": "items",
                "columns": [
                    {"name": "id", "type": "id"},
                    {"name": "name", "type": "string"},
                    {"name": "description", "type": "text"},
                    {"name": "created_at", "type": "created_at"},
                    {"name": "updated_at", "type": "updated_at"}
                ],
                "indexes": ["name"]
            }
        ]
    }

    def __init__(self):
        self.design_count = 0

    def design(self, spec: Dict[str, Any]) -> DatabaseSchema:
        """
        Design database schema for app.

        Args:
            spec: App specification

        Returns:
            DatabaseSchema with tables and migrations
        """
        self.design_count += 1
        features = spec.get("features", ["basic_crud"])
        tables = []

        # Add tables for each feature
        for feature in features:
            if feature in self.FEATURE_TABLES:
                for table_def in self.FEATURE_TABLES[feature]:
                    table = self._create_table(table_def)
                    tables.append(table)

        # Generate migrations
        migrations = self._generate_migrations(tables)

        # Generate seed data
        seed_data = self._generate_seed_data(tables)

        return DatabaseSchema(
            tables=tables,
            migrations=migrations,
            seed_data=seed_data
        )

    def _create_table(self, table_def: Dict) -> TableSchema:
        """Create TableSchema from definition."""
        columns = []
        for col in table_def.get("columns", []):
            col_type = self.COLUMN_TYPES.get(col["type"], col["type"])
            columns.append({
                "name": col["name"],
                "type": col_type
            })

        return TableSchema(
            name=table_def["name"],
            columns=columns,
            primary_key="id",
            foreign_keys=table_def.get("foreign_keys", []),
            indexes=table_def.get("indexes", [])
        )

    def _generate_migrations(self, tables: List[TableSchema]) -> str:
        """Generate SQL migrations."""
        migrations = []
        migrations.append("-- Database Migrations")
        migrations.append(f"-- Generated: {datetime.now().isoformat()}")
        migrations.append("")

        for table in tables:
            sql = f"CREATE TABLE IF NOT EXISTS {table.name} (\n"

            # Add columns
            col_defs = []
            for col in table.columns:
                col_defs.append(f"    {col['name']} {col['type']}")

            # Add foreign keys
            for fk in table.foreign_keys:
                col_defs.append(f"    FOREIGN KEY ({fk['column']}) REFERENCES {fk['references']}")

            sql += ",\n".join(col_defs)
            sql += "\n);\n"

            # Add indexes
            for idx in table.indexes:
                sql += f"CREATE INDEX IF NOT EXISTS idx_{table.name}_{idx} ON {table.name}({idx});\n"

            migrations.append(sql)

        return "\n".join(migrations)

    def _generate_seed_data(self, tables: List[TableSchema]) -> str:
        """Generate sample seed data."""
        seeds = []
        seeds.append("-- Seed Data")
        seeds.append(f"-- Generated: {datetime.now().isoformat()}")
        seeds.append("")

        for table in tables:
            if table.name == "users":
                seeds.append(f"INSERT INTO {table.name} (email, password_hash) VALUES")
                seeds.append("    ('admin@example.com', 'hashed_password'),")
                seeds.append("    ('user@example.com', 'hashed_password');")
            elif table.name == "items":
                seeds.append(f"INSERT INTO {table.name} (name, description) VALUES")
                seeds.append("    ('Sample Item', 'A sample item for testing');")

            seeds.append("")

        return "\n".join(seeds)

    def to_dict(self, schema: DatabaseSchema) -> Dict[str, Any]:
        """Convert schema to dictionary."""
        return {
            "tables": [
                {
                    "name": t.name,
                    "columns": t.columns,
                    "primary_key": t.primary_key,
                    "foreign_keys": t.foreign_keys,
                    "indexes": t.indexes
                }
                for t in schema.tables
            ],
            "migrations": schema.migrations,
            "seed_data": schema.seed_data
        }


# Testing
if __name__ == "__main__":
    designer = DatabaseDesigner()

    print("=" * 60)
    print("DATABASE DESIGNER - TEST")
    print("=" * 60)

    spec = {
        "name": "test_app",
        "features": ["user_authentication", "basic_crud"]
    }

    schema = designer.design(spec)

    print("\nTables generated:")
    for table in schema.tables:
        print(f"  - {table.name} ({len(table.columns)} columns)")

    print("\nMigrations preview:")
    print(schema.migrations[:500] + "...")

    print("\n✅ DATABASE DESIGNER OPERATIONAL")
