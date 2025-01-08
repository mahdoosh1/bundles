class _Parser:
    def __init__(self):
        self.allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"
    def parse_string_literal(self, s):
        if len(s) < 3:
            if len(s) < 2 or s[0] not in ('"', "'"):
                raise ValueError(f"Invalid string literal: {s}")
            quote = s[0]
            if len(s) == 2 and s[1] == quote:
                return ""
            else:
                raise ValueError(f"Invalid string literal: {s}")

        if s[:3] == '"""' and s[-3:] == '"""':
            quote = '"""'
            s = s[3:-3]
        elif s[:2] == '"""':
            raise ValueError(f"Invalid string literal: {s}")
        elif s[:3] == "'''":
            quote = "'''"
            s = s[3:-3] if s[-3:] == "'''" else s[3:]
        elif s[:3] == "'''":
            raise ValueError(f"Invalid string literal: {s}")
        elif s[0] in ('"', "'"):
            quote = s[0]
            if s[1] == quote:
                raise ValueError(f"Invalid string literal: {s}")
            s = s[1:]
        else:
            raise ValueError(f"Invalid string literal: {s}")

        result = []
        escape = False

        for char in s:
          if escape:
            if char == '\\':
                result.append('\\')
            elif char == 'n':
                result.append('\n')
            elif char == 't':
                result.append('\t')
            elif char == 'r':
                result.append('\r')
            elif char == '"':
                result.append('"')
            elif char == "'":
                result.append("'")
            else:
                raise ValueError(f"Invalid escape sequence: {s}")
            escape = False
          elif char == '\\':
            escape = True
          elif char == '\n' and quote != '"""' and quote != "'''":
            raise ValueError(f"Invalid string literal: {s}")
          else:
            result.append(char)

        if escape:
          raise ValueError(f"Invalid string literal: {s}")

        return ''.join(result)
    def parse_leftside(self,text):
        if text.startswith(' ') or text.startswith('\t'):
            raise NameError(f"Invalid name: {text}")
        return filter(text,self.allowed)
    def parse_rightside(self,text):
        return self.parse_string_literal(text.strip())
    def parse_line(self,text):
        left, right = text.split("=")
        left = self.parse_leftside(left)
        right = self.parse_rightside(right)
        return left, right
    def parse_all(self, text):
        output = dict()
        for line in text.split('\n'):
            key, value = self.parse_line(line)
            output[key] = value
        return output

_PARSER = _Parser()
import pathlib as _pl

class Bundle:
    def __init__(self, file_dir):
        with open(file_dir) as file:
            file_data_parsed = _PARSER.parse_all(file)
        self.data = file_data_parsed
    def get_translation(self,identifier):
        return self.data[identifier]

class Bundles:
    def __init__(self, bundles_dir):
        bundles = dict()
        path = _pl.Path(bundles_dir)
        if not path.exists():
            raise FileExistsError(f"Path doesn't exist: {str(path)}")
        if path.is_file():
            raise IsADirectoryError(f"Path does not lead to a directory: {str(path)}")
        for subpath in path.iterdir():
            if subpath.is_file():
                if subpath.suffix.lower() != '.bundle':
                    continue
                filename = subpath.stem
                bundles[filename] = Bundle(str(subpath))
        self.bundles = bundles
        self.languages = list(bundles.keys())
    def get_bundle(self,language):
        return self.bundles[language]
    def get_translation(self,language,identifier):
        return self.get_bundle(language).get_translation(identifier)

class Language:
    def __init__(self, bundle):
        if not isinstance(bundle, Bundle):
            bundle = Bundle(bundle)
        for key, val in bundle.data:
            setattr(self, key, val)

class Languages:
    def __init__(self, bundles):
        if not isinstance(bundles, Bundles):
            bundles = Bundles(bundles)
        for language_name, bundle in bundles.bundles:
            language = Language(bundle)
            setattr(self,language_name,language)