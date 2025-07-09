import logging
import traceback
import json
logging.basicConfig(level=logging.DEBUG)

from app import app

with app.app_context():
    print('Testing get_yesterdays_late_comers endpoint')
    try:
        from app import get_yesterdays_late_comers
        result = get_yesterdays_late_comers()
        print(f"Result type: {type(result)}")
        print(f"Result status code: {result[1] if isinstance(result, tuple) else 'N/A'}")
        
        # If it's a response object, try to get the data
        if hasattr(result, 'get_data'):
            data = result.get_data(as_text=True)
            print(f"Response data: {data}")
            
            # Try to parse the JSON data
            try:
                json_data = json.loads(data)
                print(f"\nParsed JSON data:")
                print(json.dumps(json_data, indent=2))
                print(f"\nNumber of late comers: {len(json_data)}")
            except json.JSONDecodeError:
                print("Could not parse response as JSON")
            
        # If it's a tuple with a response object
        elif isinstance(result, tuple) and len(result) > 0 and hasattr(result[0], 'get_data'):
            data = result[0].get_data(as_text=True)
            print(f"Response data: {data}")
            
            # Try to parse the JSON data
            try:
                json_data = json.loads(data)
                print(f"\nParsed JSON data:")
                print(json.dumps(json_data, indent=2))
                print(f"\nNumber of late comers: {len(json_data)}")
            except json.JSONDecodeError:
                print("Could not parse response as JSON")
    except Exception as e:
        print(f"Error: {str(e)}")
        traceback.print_exc()