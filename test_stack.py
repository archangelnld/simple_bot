#!/usr/bin/env python3
from azrael_manager.stack_manager import StackManager

def main():
    print("\n=== Stack Storage Connection Test ===")
    print("\nTesting stack connection...")
    stack = StackManager()
    success, status = stack.check_stack_connection()
    print(f"Connection status: {Success if success else Failed}")
    if not success:
        print(f"Error details: {status}")
        return
    
    print("\nSyncing logs to stack...")
    success, result = stack.sync_logs_to_stack()
    print(f"Log sync: {Success if success else Failed}")
    if not success:
        print(f"Error: {result}")
    
    print("\nSyncing backups to stack...")
    success, result = stack.sync_backups_to_stack()
    print(f"Backup sync: {Success if success else Failed}")
    if not success:
        print(f"Error: {result}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {e}")

