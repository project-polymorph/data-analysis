#!/usr/bin/env python3
import yaml
import re
import sys
import argparse
from pathlib import Path

def load_yaml_file(file_path):
    """Load YAML file and return the parsed content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)

def filter_entries_by_regex(data, pattern):
    """Filter entries where the key matches the regex pattern."""
    regex = re.compile(pattern)
    filtered_entries = {}
    
    for key, value in data.items():
        if regex.search(key):
            filtered_entries[key] = value
            
    return filtered_entries

def convert_to_markdown(entries):
    """Convert the filtered entries to a nice markdown format."""
    markdown = "# Filtered Entries\n\n"
    
    for url, details in entries.items():
        # Use the URL as the heading
        markdown += f"## {url}\n\n"
        
        # Add description in a blockquote
        if "description" in details and details["description"]:
            markdown += f"{details['description']}  "
        
        # Add author and date if available
        if "author" in details and details["author"] != "未知":
            markdown += f"**Author:** {details['author']}  "
        if "date" in details and details["date"] != "未知":
            markdown += f"**Date:** {details['date']}  "
        markdown += f" Link: <{url}> \n"
        
        # Add archived date
        # if "archived date" in details:
        #     markdown += f"**Archived:** {details['archived date']}  \n"
        
        markdown += "\n"
        
        # Add tags in a nicely formatted way
        if "tags" in details and details["tags"]:
            markdown += "**Tags:** "
            tags = details["tags"]
            markdown += ", ".join([f"`{tag}`" for tag in tags])
            markdown += "\n\n"
        
        # # Add other relevant details in a table
        # markdown += "| Property | Value |\n"
        # markdown += "|----------|-------|\n"
        
        # for prop, value in sorted(details.items()):
        #     # Skip properties we've already displayed
        #     if prop in ["description", "author", "date", "archived date", "tags"]:
        #         continue
                
        #     # Format lists properly
        #     if isinstance(value, list):
        #         value = ", ".join(value)
                
        #     # Convert None to empty string
        #     if value is None:
        #         value = ""
                
        #     markdown += f"| {prop} | {value} |\n"
        
        markdown += "\n---\n\n"
    
    return markdown

def main():
    parser = argparse.ArgumentParser(description='Filter YAML entries by regex and output as Markdown')
    parser.add_argument('yaml_file', help='Path to the YAML file')
    parser.add_argument('pattern', help='Regex pattern to filter entries')
    parser.add_argument('-o', '--output', help='Output markdown file (default: print to stdout)')
    
    args = parser.parse_args()
    
    # Load the YAML file
    data = load_yaml_file(args.yaml_file)
    
    # Filter entries
    filtered_entries = filter_entries_by_regex(data, args.pattern)
    
    # Check if we found anything
    if not filtered_entries:
        print("No entries match the given pattern.")
        sys.exit(0)
    
    # Convert to markdown
    markdown_content = convert_to_markdown(filtered_entries)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Output written to {args.output}")
    else:
        print(markdown_content)

if __name__ == "__main__":
    main()
