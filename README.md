Reading:
1) Permits  C++-style double-slash comments.
2) Permits leading and trailing decimals in floating point values
      e.g. ".01" or "10."
3) Permits trailing comma after last entry in dictionaries.
4) If it fails to parse, tries to localize it more clearly to the
   problematic line in the file.

Writing:
1) Simple call to both convert to string and dump to file.
2) Better defaults:
      - indentation, 4 spaces
      - use commas and colons as separators
      - Don't sort

