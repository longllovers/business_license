import re
from datetime import datetime

def extract_time_period(text):
    """
    Extract time period string from text according to the specified formats.
    Returns the extracted time period string.
    """
    # Pattern for date format: YYYY年MM月DD日
    date_pattern = r'(\d{4}年\d{1,2}月\d{1,2}日)'
    
    # Standalone '长期' pattern
    if text.strip() == '长期':
        return '长期'
    
    # Date to Date pattern: 年月日至年月日
    date_to_date = f'{date_pattern}至{date_pattern}'
    match = re.search(date_to_date, text)
    if match:
        return match.group(0)
    
    # Date to special end type patterns
    special_end_types = [
        '长期有效',
        '长期',
        '永久',
        '不约定期限'
    ]
    
    for end_type in special_end_types:
        pattern = f'{date_pattern}至{end_type}'
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    # Date to unspecified pattern: 年月日至
    date_to_unspecified = f'{date_pattern}至'
    match = re.search(date_to_unspecified, text)
    if match:
        # Make sure it's not matching one of the other patterns with something after "至"
        end_pos = match.end()
        if end_pos >= len(text) or text[end_pos:].strip() == '':
            return match.group(0)
    
    # Single date pattern: 年月日
    match = re.search(date_pattern, text)
    if match:
        return match.group(0)
    
    # If no patterns matched
    return text

# # Test the function with examples
# def test_extraction():
#     examples = [
#         "日期是2022年01月01日至2023年12月31日",
#         "合同期限为2022年1月1日至",
#         "有效期：2022年1月1日至长期",
#         "项目起止：2022年1月1日至永久",
#         "授权时间2022年1月1日至不约定期限",
#         "长期",
#         "约定日期：2022年1月1日至长期有效",
#         "出生日期：2021年10月22日",
#     ]
    
#     for example in examples:
#         result = extract_time_period(example)
#         print(f"Extracted: {result}")
#         print("-" * 50)

# # Run the test function
# if __name__ == "__main__":
#     test_extraction()