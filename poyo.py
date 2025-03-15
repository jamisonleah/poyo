#!/usr/bin/env python3

import argparse, emoji
import os, string
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Setup
DB_PATH = os.path.expanduser("~/.poyo.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class CommandAlias(Base):
  """Defines the table structure for storing commands."""
  __tablename__ = "commands"
  id = Column(Integer, primary_key=True, autoincrement=True)
  key = Column(String, unique=True, nullable=False)
  command = Column(String, nullable=False)

# Initialize database
def init_db():
  Base.metadata.create_all(engine)

# Add command
def add_command(key, command):
  if session.query(CommandAlias).filter_by(key=key).first():
      print(f"Key '{key}' already exists. Use 'poyo update {key} \"new command\"' to modify it.")
  else:
      new_entry = CommandAlias(key=key, command=command)
      session.add(new_entry)
      session.commit()
      print(f"🤩 Added: '{key}' → '{command}'")

# Get and execute command
def get_command(key, extra_args):
    alias = session.query(CommandAlias).filter_by(key=key).first()
    if alias:
        # getting placeholders from the command
        placeholders = extract_placeholders(alias.command)
        placeholder_values = {
            arg.split('=')[0]: arg.split('=', 1)[1]
            for arg in extra_args if '=' in arg
        }

        # Identify missing placeholders
        missing_placeholders = [p for p in placeholders if p not in placeholder_values]

        # Prompt interactively for any missing placeholder values
        for ph in missing_placeholders:
            placeholder_values[ph] = input(f"Enter value for '{ph}': ")

        # Format the command with all placeholders
        command_to_run = alias.command.format(**placeholder_values)
        print(f"🚀 Running: {command_to_run}")
        os.system(command_to_run)
    else:
        print(f"❌ No command found for '{key}'.")

# Extract placeholders from a command ex: poyo run hello name=John
def extract_placeholders(command):
    formatter = string.Formatter()
    return [field_name for _, field_name, _, _ in formatter.parse(command) if field_name]
# List all commands
def list_commands():
  aliases = session.query(CommandAlias).all()
  if aliases:
      print("📌 Saved Commands:")
      for alias in aliases:
          print(f"  {alias.key} → {alias.command}")
  else:
      print("🔍 No saved commands yet.")

# Update an existing command
def update_command(key, new_command):
  alias = session.query(CommandAlias).filter_by(key=key).first()
  if alias:
      alias.command = new_command
      session.commit()
      print(f"🔄 Updated '{key}' → '{new_command}'")
  else:
      print(f"❌ No command found for '{key}'. Use 'poyo add' to create one.")

# Delete a command
def delete_command(key):
  alias = session.query(CommandAlias).filter_by(key=key).first()
  if alias:
      session.delete(alias)
      session.commit()
      print(f"🗑️ Deleted '{key}'")
  else:
      print(f"❌ No command found for '{key}'.")

# Main CLI function
def main():
  init_db()  # Ensure DB is initialized

  parser = argparse.ArgumentParser(description="Poyo - A CLI shortcut manager")
  subparsers = parser.add_subparsers(dest="command")

  # Add command
  parser_add = subparsers.add_parser("add", help="Add a new command alias")
  parser_add.add_argument("key", help="Shortcut key")
  parser_add.add_argument("cmd", help="Actual command to execute")

  # Run command
  parser_run = subparsers.add_parser("run", help="Run a saved command")
  parser_run.add_argument("key", help="Shortcut key to run")
  parser_run.add_argument("extra_args", nargs="*", help="Placeholder values (e.g., name=John)")

  # List commands
  subparsers.add_parser("list", help="List all saved command aliases")

  # Update command
  parser_update = subparsers.add_parser("update", help="Update an existing command")
  parser_update.add_argument("key", help="Shortcut key to update")
  parser_update.add_argument("cmd", help="New command to replace the old one")

  # Delete command
  parser_delete = subparsers.add_parser("delete", help="Delete a command alias")
  parser_delete.add_argument("key", help="Shortcut key to delete")

  args = parser.parse_args()

  if args.command == "add":
    add_command(args.key, args.cmd)
  elif args.command == "run":
    get_command(args.key, args.extra_args)
  elif args.command == "list":
    list_commands()
  elif args.command == "update":
    update_command(args.key, args.cmd)
  elif args.command == "delete":
    delete_command(args.key)
  else:
    parser.print_help()

if __name__ == "__main__":
  main()
