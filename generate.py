import yaml

def generate_api_code(yaml_file):
    with open(yaml_file, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    api_code = """import requests\nimport json\n"""
    for i in range(0,len(spec['servers'])): 
        base_url = spec['servers'][i]['url']
        
        for path, methods in spec['paths'].items():
            for method, details in methods.items():
                # 方法解析
                url = base_url + path
                # 描述解析
                summary = details.get('summary', '')
                description = details.get('description', '')
                
                # 參數解析
                parameters = ""
                json_data = ""
                if 'requestBody' in details:
                    properties = details['requestBody']['content']['application/json']['schema'].get('properties', {})
                    for param, value in properties.items():
                        parameters += f"{param}: {value['type']}, "
                        json_data += f"'{param}': {param}, "

                    print("json_data",json_data)    
                    parameters = parameters.rstrip(", ")
                    json_data = "{"+ json_data.rstrip(", ") + "}" 
                method_code = f"""
def {method}{path.replace('/', '_').replace('{', '').replace('}', '')}({parameters}):
    \"\"\"{summary}
    {description}
    \"\"\"
    url = "{url}"
    method = "{method.upper()}"
    # Prepare parameters as JSON if needed
    json_data = json.dumps({json_data})
    
    # Add request logic here (using requests library for example)
    if method.upper() == "GET":
        response = requests.get(url)
    elif method.upper() == "POST":
        response = requests.post(url, data=json_data, headers={{"Content-Type": "application/json"}})
    elif method.upper() == "PUT":
        response = requests.put(url, data=json_data, headers={{"Content-Type": "application/json"}})
    elif method.upper() == "DELETE":
        response = requests.delete(url)
    
    return response
            """
                api_code += method_code
    
    return api_code

if __name__=='__main__':
    python_code = generate_api_code("api.yaml")

    with open("api_client.py", "w", encoding="utf-8") as f:
        f.write(python_code)

    print("API client generated: api_client.py")