#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ


def main():
    """Run administrative tasks."""

    # Initialize environment reading
    env = environ.Env()

    # Get the environment variable (defaults to 'development' if not set)
    env_name = os.getenv('ENV', 'development')

    # Load the corresponding .env file based on the ENV environment variable
    env_file = f".env.{env_name}"
    if os.path.exists(env_file):
        environ.Env.read_env(env_file)
        print(f"Loading environment from {env_file}")
    else:
        print(f"Warning: {env_file} not found. Using default settings.")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
   
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
