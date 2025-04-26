#!/usr/bin/env python3
from rich.console import Console
from rich.panel import Panel

console = Console()

def show_error(message):
    """Toon error message"""
    console.print(Panel(str(message), title="Error", style="bold red"))

def show_success(message):
    """Toon success message"""
    console.print(Panel(str(message), title="Success", style="bold green"))

def confirm_action(message="Weet je het zeker?"):
    """Vraag gebruiker om bevestiging"""
    response = console.input(f"{message} (y/n): ")
    return response.lower() == 'y'

def get_system_info():
    """Basis systeem info"""
    try:
        info = {
            'status': 'running',
            'version': '1.0'
        }
        return True, info
    except Exception as e:
        return False, str(e)
