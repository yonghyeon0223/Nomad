import requests
from bs4 import BeautifulSoup


class EndOfRequestException(Exception):
    def __init__(self):
        super().__init__("Request Process Finished!")


def extract_num(line):
    line = list(line)
    num = ""
    for chr in line:
        if chr in "0123456789":
            num += chr
        else:
            return int(num)
    return int(num)


def utf_encode(text):
    utf_text = str(text).encode("utf-8")
    return str(utf_text)


class Webpage:
    def __init__(self, url, pagination_info, search_info):
        self.url = url
        self.soup = self.get_soup()

        self.pagination = list()
        self.pagination_info = pagination_info

        self.current_page = self.get_current_page()  # current page index
        self.find_pagination()  # stores pages' index and link in a list
        self.next_page_link = self.get_next_page_link()  # next page url

        self.search_info = search_info

    def get_soup(self):
        while True:
            req = requests.get(self.url)
            soup = BeautifulSoup(req.text, "html.parser")
            if not (req is None or soup is None):
                break
            print("requesting again..")
        return soup

    def find_pagination(self):
        location = self.pagination_info.get("location")
        classname = self.pagination_info.get("classname")
        query_line = self.pagination_info.get("query_line")
        try:
            pagination = self.soup.find(location, {"class": classname})
            pages = pagination.find_all("a")

            for page in pages:
                self.pagination.append(Pagination(page.get("href"), query_line))
        except AttributeError as e:
            print(self.url, self.pagination_info)
            print(e)

    def get_current_page(self):
        query_line = self.pagination_info["query_line"]
        try:
            start = int(self.url.index(query_line)) + len(query_line)
            return extract_num(self.url[start:])
        except ValueError as e:
            return 0

    def get_next_page_link(self):
        next_p = self.pagination[-1]
        query_line = self.pagination_info.get("query_line")
        if self.current_page < next_p.location:
            if query_line in self.url:
                return self.url.replace(query_line + str(self.current_page), query_line + str(next_p.location))
            else:
                return (self.url + next_p.page_link)
        else:
            raise EndOfRequestException

    def search_element(self, search_info):
        location = search_info["tag_location"]
        classname = search_info["classname"]

        found_ls = self.soup.find_all(location, {"class": classname})
        result = list()

        for found in found_ls:
            string_res = found.text
            try:
                result.append(utf_encode(string_res)[2:-1])
            except UnicodeDecodeError as e:
                result.append("encoding failed :(")
        return result

    def search_elements(self):
        result_ls = list()
        for search in self.search_info:
            result_ls.append(self.search_element(search))
        return result_ls

    def get_progress(self, i, freq=1):
        if i % freq != 0:
            return ""
        line = "----------WEBPAGE INFORmATION----------" \
               + "\nURL:" + self.url \
               + "\nCURRENT PAGE:" + str(self.current_page) \
               + "\nNEXT PAGE:" + self.next_page_link \
               + "Pagination:\n"

        for page in self.pagination:
            line += page.toString()
        line += "==========================================\n\n"
        return line


class Pagination:
    def __init__(self, page_link, query_line):
        try:
            start = int(page_link.index(query_line)) + len(query_line)
            self.location = extract_num(page_link[start:])
        except ValueError as e:
            self.location = 0
        self.page_link = page_link

    def toString(self):
        return "\tpage location: " + str(self.location) + " page_link: " + self.page_link + "\n"
