import requests
import re
import json
from pathlib import Path

def extract_aadhaar_info():
    """Enhanced Aadhaar OCR parser with better error handling and field extraction"""
    
    url = "https://api.ocr.space/parse/image"
    
    # Get API key - you'll need to replace this with a valid key from ocr.space
    api_key = input("Enter your OCR.space API key (get free key from ocr.space): ").strip()
    if not api_key:
        api_key = "helloworld"  # This likely won't work - need real API key
    
    payload = {
        "apikey": api_key,
        "language": "eng",
        "isOverlayRequired": False,
        "OCREngine": 2  # Use OCR Engine 2 for better accuracy
    }

    # Get image file from user input
    while True:
        image_file = input("Enter the image file path (e.g., aadhaar.jpg): ").strip()
        if Path(image_file).exists():
            break
        print(f"File '{image_file}' not found. Please check the path.")

    try:
        with open(image_file, "rb") as f:
            files = {"filename": f}
            
            print("Processing image with OCR...")
            res = requests.post(url, data=payload, files=files, timeout=30)
        
        # Enhanced response handling
        if res.status_code != 200:
            print(f"HTTP Error {res.status_code}: {res.text}")
            if res.status_code == 429:
                print("Rate limit exceeded. Please wait and try again.")
            return None
            
        try:
            data = res.json()
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            print("Response:", res.text[:500])
            return None
            
        # Check for API errors
        if isinstance(data, str):
            print("API Error:", data)
            return None
            
        if not data.get('ParsedResults') or len(data['ParsedResults']) == 0:
            print("No text found in image")
            return None
            
        if data['ParsedResults'][0].get('ErrorMessage'):
            print("OCR Error:", data['ParsedResults'][0]['ErrorMessage'])
            return None
        
        parsed_text = data['ParsedResults'][0].get('ParsedText', '')
        print("=== DEBUG: OCR TEXT ===")
        print(parsed_text)
        print("=" * 50)
        
        if not parsed_text.strip():
            print("No text extracted from image")
            return None

        # Enhanced field extraction function
        def extract_field(patterns, text, default=None):
            """Try multiple patterns and return the first match"""
            for pattern in patterns:
                try:
                    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                    if match:
                        result = match.group(1).strip()
                        # Clean up common OCR artifacts
                        result = re.sub(r'\s+', ' ', result)
                        result = result.replace('|', '').replace('_', '').strip()
                        if result:
                            return result
                except Exception as e:
                    print(f"Pattern error: {e}")
                    continue
            return default

        # Enhanced name extraction patterns
        name_patterns = [
            r'(?:Name|नाम)[\s:]*([A-Za-z\s]{3,50}?)(?=\n|\r|Address|Father|Mother|S/O|D/O|W/O)',
            r'To[\s\n:]+([A-Za-z\s]{3,50})(?=\n|\r|C/O|S/O|D/O)',
            r'^([A-Za-z\s]{3,50})(?=\n.*(?:C/O|S/O|D/O|Address))',
            r'([A-Za-z\s]{3,50})(?=\n.*[0-9]{6})',  # Name before PIN
        ]
        
        # Enhanced Aadhaar number patterns
        aadhaar_patterns = [
            r'(?:Aadhaar|आधार|UIDAI)[\s\w]*?([0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4})',
            r'\b([0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4})\b',
            r'([0-9]{12})',  # 12 consecutive digits
        ]
        
        # Enhanced address patterns
        address_patterns = [
            r'(?:C/O|S/O|D/O|W/O)[\s]*([^,\n]+(?:,\s*[^,\n]+)*?)(?=(?:VTC|Sub|District|PIN|Mobile|State|\d{6}))',
            r'Address[\s:]+([^,\n]+(?:,\s*[^,\n]+)*?)(?=(?:VTC|Sub|District|PIN|Mobile|State|\d{6}))',
            r'(?:To:?[^\n]*\n)((?:[^,\n]+,?\s*){2,}?)(?=(?:VTC|Sub|PIN|District|Mobile|State|\d{6}))'
        ]
        
        # Enhanced mobile patterns
        mobile_patterns = [
            r'(?:Mobile|Mob|मोबाइल)[\s:.-]*([0-9]{10})',
            r'(?:Phone|Ph)[\s:.-]*([0-9]{10})',
            r'\b([0-9]{10})\b'
        ]
        
        # Enhanced DOB patterns
        dob_patterns = [
            r'(?:DOB|Date\s+of\s+Birth|जन्म\s*तिथि)[\s:]*([0-9]{1,2}[/.-][0-9]{1,2}[/.-][0-9]{4})',
            r'(?:DOB|Date\s+of\s+Birth|जन्म\s*तिथि)[\s:]*([0-9]{2}[0-9]{2}[0-9]{4})',
            r'(\d{1,2}[/.-]\d{1,2}[/.-]\d{4})'
        ]
        
        # Enhanced gender patterns
        gender_patterns = [
            r'(?:Sex|Gender|लिंग)[\s:]*([MFmf](?:ale)?|पुरुष|महिला)',
            r'/\s*([MFmf])\s*/',
            r'\b(Male|Female|पुरुष|महिला)\b'
        ]
        
        # Location patterns
        vtc_patterns = [r'VTC[\s:]+([^,\n]+)', r'Village[\s:]+([^,\n]+)']
        po_patterns = [r'(?:PO|Post\s+Office)[\s:]+([^,\n]+)']
        sub_district_patterns = [r'(?:Sub[\s-]*District|Taluk|Tehsil)[\s:]+([^,\n]+)']
        district_patterns = [r'District[\s:]+([^,\n]+)']
        state_patterns = [r'State[\s:]+([^,\n]+)']
        pin_patterns = [r'(?:PIN|Postal)[\s:]*([0-9]{6})', r'\b([0-9]{6})\b']
        enrollment_patterns = [r'(?:Enrollment|Enrolment)[\s]*(?:No\.?|Number)[\s:.-]*([0-9/]+)']

        # Extract all fields
        extracted_info = {
            'name': extract_field(name_patterns, parsed_text),
            'aadhaar_number': extract_field(aadhaar_patterns, parsed_text),
            'address': extract_field(address_patterns, parsed_text),
            'mobile': extract_field(mobile_patterns, parsed_text),
            'dob': extract_field(dob_patterns, parsed_text),
            'gender': extract_field(gender_patterns, parsed_text),
            'vtc': extract_field(vtc_patterns, parsed_text),
            'po': extract_field(po_patterns, parsed_text),
            'sub_district': extract_field(sub_district_patterns, parsed_text),
            'district': extract_field(district_patterns, parsed_text),
            'state': extract_field(state_patterns, parsed_text),
            'pin': extract_field(pin_patterns, parsed_text),
            'enrollment': extract_field(enrollment_patterns, parsed_text)
        }
        
        
        # Special handling for this Aadhaar format - manual extraction if patterns fail
        if not extracted_info['name'] or extracted_info['name'] == 'Government of India':
            # Look for name pattern specific to this format
            lines = parsed_text.split('\n')
            for i, line in enumerate(lines):
                if 'Enrolment No' in line and i+2 < len(lines):
                    potential_name = lines[i+2].strip()
                    if len(potential_name.split()) >= 2 and not any(word in potential_name.lower() for word in ['government', 'india', 'authority']):
                        extracted_info['name'] = potential_name
                        break
        
        # Manual address extraction for this specific format
        if not extracted_info['address']:
            address_parts = []
            lines = parsed_text.split('\n')
            collecting = False
            for line in lines:
                line = line.strip()
                if 'C/O:' in line:
                    # Extract the part after C/O: on the same line
                    co_part = line.split('C/O:')[1].strip()
                    if co_part.endswith(','):
                        co_part = co_part[:-1]
                    address_parts.append(co_part)
                    collecting = True
                    continue
                elif collecting:
                    if (any(word in line.lower() for word in ['vtc:', 'mumbai', 'maharashtra', 'aadhaar', 'vid', 'mobile:', 'sub district']) or 
                        re.match(r'^\d{4}\s+\d{4}\s+\d{4}', line) or
                        line.startswith('KC') or
                        line.startswith('З')):
                        break
                    elif line and not line.isdigit():
                        # Clean up the line
                        clean_line = line.rstrip('.,')
                        if clean_line:
                            address_parts.append(clean_line)
            
            if address_parts:
                extracted_info['address'] = ', '.join(address_parts)
        
        # Post-process extracted data
        if extracted_info['aadhaar_number']:
            # Clean and format Aadhaar number
            aadhaar = re.sub(r'[\s-]', '', extracted_info['aadhaar_number'])
            if len(aadhaar) == 12 and aadhaar.isdigit():
                extracted_info['aadhaar_number'] = f"{aadhaar[:4]} {aadhaar[4:8]} {aadhaar[8:]}"
            else:
                extracted_info['aadhaar_number'] = None
        
        if extracted_info['mobile']:
            # Clean mobile number
            mobile = re.sub(r'[^\d]', '', extracted_info['mobile'])
            if len(mobile) == 10 and mobile.isdigit():
                extracted_info['mobile'] = mobile
            else:
                extracted_info['mobile'] = None
        
        if extracted_info['gender']:
            # Standardize gender
            gender_lower = extracted_info['gender'].lower()
            if any(x in gender_lower for x in ['f', 'female', 'महिला','स्त्री']):
                extracted_info['gender'] = 'Female'
            elif any(x in gender_lower for x in ['m', 'male', 'पुरुष']):
                extracted_info['gender'] = 'Male'
            else:
                extracted_info['gender'] = None
        
        if extracted_info['dob']:
            # Standardize date format
            dob = extracted_info['dob']
            dob = re.sub(r'[-.]', '/', dob)
            if len(dob.replace('/', '')) == 8:
                extracted_info['dob'] = dob
            else:
                extracted_info['dob'] = None
        
        # Display results
        print("\n" + "="*60)
        print("EXTRACTED AADHAAR INFORMATION")
        print("="*60)
        
        for field, value in extracted_info.items():
            status = "✓" if value else "✗"
            print(f"{status} {field.replace('_', ' ').title()}: {value or 'Not found'}")
        
        return extracted_info
        
    except FileNotFoundError:
        print(f"Error: Image file '{image_file}' not found")
        return None
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Aadhaar Card OCR Parser")
    print("=" * 30)
    print("Make sure you have:")
    print("1. A valid OCR.space API key (free at ocr.space)")
    print("2. A clear image of an Aadhaar card")
    print("3. Internet connection")
    print()
    
    result = extract_aadhaar_info()
    
    if result:
        print("\n" + "="*60)
        print("FORMATTED OUTPUT")
        print("="*60)
        print(f"""
Government of India
Unique Identification Authority of India
Enrollment No.: {result.get('enrollment', 'Not found')}

Recipient Details:
- Name: {result.get('name', 'Not found')}
- Address: {result.get('address', 'Not found')}
- VTC: {result.get('vtc', 'Not found')}, PO: {result.get('po', 'Not found')}
- Sub District: {result.get('sub_district', 'Not found')}, District: {result.get('district', 'Not found')}
- State: {result.get('state', 'Not found')}, PIN Code: {result.get('pin', 'Not found')}
- Mobile: {result.get('mobile', 'Not found')}

Aadhaar Number: {result.get('aadhaar_number', 'Not found')}
Date of Birth: {result.get('dob', 'Not found')}
Gender: {result.get('gender', 'Not found')}
""")
    else:
        print("\nFailed to extract information. Please check:")
        print("- Image quality and clarity")
        print("- API key validity") 
        print("- Internet connection")
        print("- File path correctness")
