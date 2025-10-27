#!/usr/bin/env python3
"""
Experiment 3: Quick CLI Parser
Test different approaches to parsing commands
"""

def simple_parser(user_input):
    """Simple command parsing - what we have now"""
    parts = user_input.strip().split(maxsplit=1)
    command = parts[0].lower() if parts else ""
    args = parts[1] if len(parts) > 1 else ""
    return command, args

def advanced_parser(user_input):
    """
    Advanced parsing with flags
    Example: note --title "My Note" --tags python,ai --category learning
    """
    import shlex
    
    parts = shlex.split(user_input)
    if not parts:
        return None, {}
    
    command = parts[0].lower()
    args = {}
    
    i = 1
    current_flag = None
    
    while i < len(parts):
        if parts[i].startswith('--'):
            current_flag = parts[i][2:]
            args[current_flag] = True  # Boolean flag
            i += 1
        elif current_flag:
            args[current_flag] = parts[i]
            current_flag = None
            i += 1
        else:
            # Positional argument
            if 'text' not in args:
                args['text'] = parts[i]
            else:
                args['text'] += ' ' + parts[i]
            i += 1
    
    return command, args

def natural_language_hints():
    """Show how we might parse natural language commands"""
    
    examples = [
        "create a note about Python",
        "show me tasks due this week",
        "find notes tagged with AI",
        "add a high priority task to finish homework",
    ]
    
    print("\n🤖 Natural Language Examples:")
    print("="*60)
    
    patterns = {
        r"create.*note.*about (.+)": "note {title}",
        r"show.*tasks.*due.*week": "tasks --due-week",
        r"find.*notes.*tagged.*(.+)": "search --tags {tags}",
        r"add.*(high|medium|low).*task.*(.+)": "task --priority {priority} {title}",
    }
    
    import re
    
    for example in examples:
        print(f"\n📝 Input: '{example}'")
        
        for pattern, command_template in patterns.items():
            match = re.search(pattern, example, re.IGNORECASE)
            if match:
                print(f"   → Would execute: {command_template}")
                break
        else:
            print("   → No pattern matched (would use AI)")

def demo_parsers():
    """Demo different parsing approaches"""
    
    test_commands = [
        "note My Simple Note",
        "note --title 'My Complex Note' --tags python,ai --category learning",
        "task Complete homework",
        "task --title 'Complete homework' --priority high --due 2025-10-30",
        "search python",
        "search --query 'machine learning' --tags ai",
    ]
    
    print("\n" + "="*60)
    print("🔧 Command Parser Experiments")
    print("="*60)
    
    for cmd in test_commands:
        print(f"\n📝 Input: {cmd}")
        
        # Simple parser
        simple_cmd, simple_args = simple_parser(cmd)
        print(f"   Simple: command='{simple_cmd}', args='{simple_args}'")
        
        # Advanced parser
        adv_cmd, adv_args = advanced_parser(cmd)
        print(f"   Advanced: command='{adv_cmd}', args={adv_args}")
    
    natural_language_hints()

if __name__ == "__main__":
    demo_parsers()
