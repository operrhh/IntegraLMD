#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import oracledb

sys.modules['cx_Oracle'] = oracledb

is_production = False

# Set the Oracle client library path
try:
    if is_production:
        #Produccion
        lib_path = "/opt/oracle/instantclient_21_17"
        oracledb.init_oracle_client(
            lib_dir=lib_path,
            driver_name="Oracle Client",  # Fuerza modo Thick
            config_dir=None,
            error_url=None
        )
        print(f"✅ Oracle Client configurado (Modo Thick) en {lib_path}")
    else:
        #Local
        lib_path = r"C:\oracle\instantclient_21_17"
        oracledb.init_oracle_client(lib_dir=lib_path)
except Exception as e:
    print(f"❌ Error configurando Oracle Client: {e}")
    sys.exit(1)

def main():
    """Run administrative tasks."""

    if is_production:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integra_lmd.settings.production')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integra_lmd.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv) 

if __name__ == '__main__':
    main()