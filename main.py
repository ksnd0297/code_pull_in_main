import re
import pprint

def extract_functions(code):
    functions = []
    pattern = re.compile(r'(\b\w+)\s+(\w+)\([^)]*\)\s*{([^}]*)}')
    matches = re.findall(pattern, code)
    for match in matches:
        function = {
            'name': match[1].strip(),
            'definition': match[2].strip()
        }
        functions.append(function)
    return functions

def replace_function_calls(extracted_functions):
    main_function = None
    function_calls = []
    for function in extracted_functions:
        if function['name'] == 'main':
            main_function = function
        else:
            function_calls.append(function['name'])
    
    if main_function is None:
        return extracted_functions
    
    for function_call in function_calls:
        pattern = r'\b' + re.escape(function_call) + r'\([^)]*\)'
        matches = re.findall(pattern, main_function['definition'])
        for match in matches:
            called_function = next((f for f in extracted_functions if f['name'] == function_call), None)
            if called_function is not None:
                main_function['definition'] = main_function['definition'].replace(match, called_function['definition'])
    
    return extracted_functions

# 주어진 C++ 코드
cpp_code = '''
#include <iostream>

using namespace std;

int add(int a, int b) {
  int temp = 10;
  int temp2 = 20;
  return a + b;
}

float multiply(float a, float b) {
  int temp3 = 10;
  int temp4 = 20;
  return a * b;
}

void print_message() {
  cout << "Hello, World!" << endl;
}

int main(void) {
  int add_result = add(10, 20);
  float multiply_result = multiply(5.5, 2.0);
  print_message();

  return 0;
}
'''

# 함수 추출
extracted_functions = extract_functions(cpp_code)

modified_functions = replace_function_calls(extracted_functions)

for function in extracted_functions:
    if(function['name'] == 'main'):
      print("Function Name:", function['definition'])