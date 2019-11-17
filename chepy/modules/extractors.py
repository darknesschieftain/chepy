import json
import regex as re
import jsonpath_rw
from urllib.parse import urlparse as _pyurlparse
from parsel import Selector
from ..core import Core


class Extractors(Core):
    def extract_strings(self, length: int = 4):
        """Extract strings from state
        
        Args:
            length (int, optional): Min length of string. Defaults to 4.
        
        Returns:
            Chepy: The Chepy object. 
        """
        pattern = b"[^\x00-\x1F\x7F-\xFF]{" + str(length).encode() + b",}"
        self.state = re.findall(pattern, self._convert_to_bytes())
        return self

    def extract_ips(self, invalid: bool = False, is_binary: bool = False):
        """Extract ipv4 and ipv6 addresses
        
        Args:
            invalid (bool, optional): Include :: addresses. Defaults to False.
            is_binary (bool, optional): The state is in binary format. It will then first 
                extract the strings from it before matching.
        
        Returns:
            Chepy: The Chepy object. 
        """
        pattern = b"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))"
        if is_binary: # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    def extract_email(self, is_binary: bool = False):
        """Extract email

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first 
                extract the strings from it before matching.
        
        Returns:
            Chepy: The Chepy object. 
        """
        pattern = b"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if is_binary:
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else: # pragma: no cover
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    def extract_mac_address(self, is_binary: bool = False):
        """Extract MAC addresses

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first 
                extract the strings from it before matching.
        
        Returns:
            Chepy: The Chepy object. 
        """
        pattern = b"^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$"
        if is_binary: # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    def extract_urls(self, is_binary: bool = False):
        """Extract urls including http, file, ssh and ftp

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first 
                extract the strings from it before matching.
        
        Returns:
            Chepy: The Chepy object. 
        """
        pattern = b"(file|ftps?|http[s]?|ssh)://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        if is_binary: # pragma: no cover
            matched = list(
                filter(lambda x: re.search(pattern, x), self.extract_strings().o)
            )
        else:
            matched = list(
                filter(
                    lambda x: re.search(pattern, x), self._convert_to_bytes().split()
                )
            )
        self.state = matched
        return self

    def extract_domains(self, is_binary: bool = False):
        """Extract domains

        Args:
            is_binary (bool, optional): The state is in binary format. It will then first 
                extract the strings from it before matching.
        
        Returns:
            Chepy: The Chepy object. 
        """
        # pattern = b"[a-z0-9]([a-z0-9-]+\.){1,}[a-z0-9]+\Z"
        if is_binary: # pragma: no cover
            matched = list(_pyurlparse(x).netloc for x in self.extract_strings().o)
        else:
            matched = list(
                _pyurlparse(x).netloc
                for x in self._convert_to_bytes().split()
                if x.startswith(b"http")
            )
        self.state = matched
        return self

    def xpath_selector(self, query: str, namespaces: str = None):
        """Extract data using valid xpath selectors
        
        Args:
            query (str): Xpath query
            namespaces (str, optional): Namespace. Applies for XML data. Defaults to None.
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = (
            Selector(self._convert_to_str(), namespaces=namespaces)
            .xpath(query)
            .getall()
        )
        return self

    def css_selector(self, query: str):
        """Extract data using valid CSS selectors
        
        Args:
            query (str): CSS query
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = Selector(self._convert_to_str()).css(query).getall()
        return self

    def jpath_selector(self, query: str):
        """Query JSON with jpath query

        `Reference <https://goessner.net/articles/JsonPath/index.html#e2>`__
        
        Args:
            query (str): Query. For reference, see the help
        
        Returns:
            Chepy: The Chepy object. 
        """
        self.state = list(
            j.value
            for j in jsonpath_rw.parse(query).find(json.loads(self._convert_to_str()))
        )
        return self
