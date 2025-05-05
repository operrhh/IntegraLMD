#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import oracledb

sys.modules['cx_Oracle'] = oracledb

# Set the Oracle client library path
try:
    oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_17")
except Exception as e:
    print(f"Error al inicializar el cliente de Oracle: {e}")
    sys.exit(1)

# Iniciador Production
#oracledb.init_oracle_client(lib_dir=r"\oracle\instantclient_21_17")

def main():
    """Run administrative tasks."""
    #os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'integra_lmd.settings.production')
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