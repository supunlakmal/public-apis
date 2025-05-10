import re
import json

def parse_api_doc_to_json_string(markdown_content):
    """
    Parses the markdown document to extract API information, categorize it,
    and returns it as a JSON formatted string.

    Args:
        markdown_content (str): The full markdown document content as a string.

    Returns:
        str: A JSON formatted string of the categorized APIs.
             Returns an empty JSON object string "{}" if parsing fails or no data.
    """
    categorized_apis = {}
    current_category = None

    # Regex to find category headers (e.g., "### Animals")
    category_regex = re.compile(r"^###\s+([^#\n]+)")

    # Regex to find table rows and extract API details
    # Handles API name as a link: | [Name](link) | ... |
    api_row_regex = re.compile(
        r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|"  # API Name and Link
        r"\s*([^|]+?)\s*\|"                     # Description
        r"\s*(?:`([^`]+?)`|([^|]+?))\s*\|"      # Auth (with or without backticks)
        r"\s*([^|]+?)\s*\|"                     # HTTPS
        r"\s*([^|]+?)\s*\|"                     # CORS
    )
    # Handles API name as plain text (no embedded link in the cell): | Name | ... |
    api_row_no_link_regex = re.compile(
        r"\|\s*([^|[]+?)\s*\|"                  # API Name (no link, not starting with '[')
        r"\s*([^|]+?)\s*\|"                     # Description
        r"\s*(?:`([^`]+?)`|([^|]+?))\s*\|"      # Auth
        r"\s*([^|]+?)\s*\|"                     # HTTPS
        r"\s*([^|]+?)\s*\|"                     # CORS
    )

    lines = markdown_content.splitlines()

    for line in lines:
        line = line.strip()

        category_match = category_regex.match(line)
        if category_match:
            current_category = category_match.group(1).strip()
            current_category = current_category.replace("&", "&") # Handle HTML entity
            categorized_apis[current_category] = []
            continue

        if current_category and line.startswith("|") and not line.startswith("|:") and "API | Description | Auth | HTTPS | CORS" not in line:
            api_match = api_row_regex.match(line)
            api_entry = None

            if api_match:
                name = api_match.group(1).strip()
                link = api_match.group(2).strip()
                description = api_match.group(3).strip()
                auth_val_group4 = api_match.group(4)
                auth_val_group5 = api_match.group(5)
                auth = (auth_val_group4.strip() if auth_val_group4 else (auth_val_group5.strip() if auth_val_group5 else ""))

                https_str = api_match.group(6).strip().lower()
                https_bool = https_str == 'yes'

                cors_str = api_match.group(7).strip().lower()
                if cors_str in ['unknown', '-', '']: # Check for empty string too
                    cors_val = "unknown"
                else:
                    cors_val = cors_str

                api_entry = {
                    "name": name,
                    "description": description,
                    "auth": auth,
                    "https": https_bool,
                    "cors": cors_val,
                    "link": link
                }
            else:
                api_match_no_link = api_row_no_link_regex.match(line)
                if api_match_no_link:
                    name = api_match_no_link.group(1).strip()
                    description = api_match_no_link.group(2).strip()
                    auth_val_group3 = api_match_no_link.group(3)
                    auth_val_group4_no_link = api_match_no_link.group(4)
                    auth = (auth_val_group3.strip() if auth_val_group3 else (auth_val_group4_no_link.strip() if auth_val_group4_no_link else ""))

                    https_str = api_match_no_link.group(5).strip().lower()
                    https_bool = https_str == 'yes'

                    cors_str = api_match_no_link.group(6).strip().lower()
                    if cors_str in ['unknown', '-', '']: # Check for empty string too
                        cors_val = "unknown"
                    else:
                        cors_val = cors_str
                    
                    api_entry = {
                        "name": name,
                        "description": description,
                        "auth": auth,
                        "https": https_bool,
                        "cors": cors_val,
                        "link": "" 
                    }

            if api_entry and current_category in categorized_apis:
                categorized_apis[current_category].append(api_entry)

    return json.dumps(categorized_apis, indent=2)


# --- Main execution: Read README.md, parse, and print/save JSON ---
if __name__ == "__main__":
    markdown_file_name = 'README.md'
    json_output_file_name = 'categorized_apis_from_readme.json'

    markdown_text_content = ""
    try:
        with open(markdown_file_name, 'r', encoding='utf-8') as f:
            markdown_text_content = f.read()
        print(f"Successfully read '{markdown_file_name}'.")
    except FileNotFoundError:
        print(f"Error: The markdown file '{markdown_file_name}' was not found.")
        print("Please ensure the file exists in the same directory as the script or provide the correct path.")
        exit()
    except Exception as e:
        print(f"An error occurred while reading '{markdown_file_name}': {e}")
        exit()

    if not markdown_text_content:
        print("Error: The markdown file is empty.")
        exit()

    print(f"Parsing '{markdown_file_name}'...")
    json_result_string = parse_api_doc_to_json_string(markdown_text_content)
    
    if json_result_string and json_result_string != "{}":
        print("Parsing complete.")
        # print("\n--- Generated JSON Output ---")
        # print(json_result_string) # You can uncomment this to print the full JSON to console
        # print("--- End of JSON Output ---\n")

        try:
            with open(json_output_file_name, 'w', encoding='utf-8') as outfile:
                outfile.write(json_result_string)
            print(f"Successfully saved categorized APIs to '{json_output_file_name}'")
        except IOError as e:
            print(f"Error: Could not write JSON to '{json_output_file_name}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred while writing the JSON file: {e}")
    else:
        print("Parsing resulted in empty or no data. No JSON file saved.")