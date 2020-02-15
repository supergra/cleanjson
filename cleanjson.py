import json

'''
Reading:
1) Permit  C++-style double-slash comments.
2) Permit leading and trailing decimals in floating point values
      e.g. .01, 10.
3) Permit trailing comma after last entry in dictionaries
4) If it fails to parse, try to localize it more clearly to the
   problematic line

Writing:
1) Wrap the conversion to string and writer in one simple call
2) Better defaults:
      - indentation, 4 spaces
      - use commas and colons as separators
      - Don't sort
'''

def writeCleanJson(filepath, data, sort=False,indent=4):
    try:
        txt = json.dumps(data,indent=indent,separators=(',',': '),sort_keys=sort)
    except TypeError:
        print("WriteCleanJson failed while writing:")
        print(data)
        raise

    with open(filepath,'w') as out:
        out.write(txt)

def readJson(filepath):
    '''
    Read a json-style file, which may contain C++-style double-slash comments.
    '''
    lines = []
    line_nums = []
    with open(filepath,'r') as f:
        for i,line in enumerate(f,start=1):
            # Strip out comments, which are non-standard JSON
            L = line.partition('//')[0].strip()
            if not L:
                continue

            # Remove leading and trailing decimals
            L = _fixJsonDecimals(L)

            lines.append(L)

            # Store line number in the original file to help find errors
            line_nums.append(i)

    json_str = ''.join(lines)

    # Permit trailing comma after last entry in dictionaries or arrays
    json_str = json_str.replace(',}','}')
    json_str = json_str.replace(',]',']')

    try:
        return json.loads(json_str)
    except ValueError as e:
        print("Error parsing JSON:",e)


    # If it failed to parse, try to localize it more clearly
    # Successively parse larger and larger portions until it fails.
    for i in range(1,len(lines)):
        # Skip errors in partial parses due simply to unclosed brackets.
        asdf = ''.join(lines[:i]).strip().rstrip(',')
        n_open_braces = asdf.count('{')-asdf.count('}')
        asdf += '}'*n_open_braces

        try:
            json.loads(asdf)
        except ValueError:
            print("Error appears to be around line {}:".format(line_nums[i-1]))
            print(lines[i-1])
            raise
    else:
        raise Exception("Error parsing JSON -- but couldn't automatically determine where the error is.")

def _fixJsonDecimals(string):
    ''' Fix leading and trailing decimals not supported by JSON '''
    chars = []
    enabled = True # Skip things that are quoted
    for j, char in enumerate(string):
        if char == '.' and enabled:
            if chars[-1] not in (str(_) for _ in range(10)):
                chars.append('0')

            chars.append('.')

            if string[j+1] not in (str(_) for _ in range(10)):
                chars.append('0')
        else:
            chars.append(char)
            if char in ("'", '"'):
                enabled = not enabled
    return ''.join(chars)
