from Webpage import Webpage
import csv
import os


def progress_file_setup(filename):
    with open(filename, "w") as f:
        f.write("")


def result_file_setup(filename, description_ls):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(description_ls)


def write_progress(filename, content):
    with open(filename, "a") as f:
        f.write(str(content))


def write_result(filename, result_ls):
    length = len(result_ls[0])

    for result in result_ls:
        # print(len(result))
        assert (len(result) == length)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        for i in range(length):
            row = list()
            for result in result_ls:
                row.append(result[i])
            writer.writerow(row)


def run(url, pagination_info, search_info, progress_file, result_file, contain_num):
    folder = "query_result"
    if not os.path.exists(folder):
        os.system(f"mkdir {folder}")
    folder += "/"
    progress_file = folder + progress_file
    result_file = folder + result_file
    progress_file_setup(progress_file)
    result_file_setup(result_file, search_info[0])

    search_info = search_info[1:]
    Current_page = Webpage(url, pagination_info, search_info)

    i = 0
    while True:
        write_progress(progress_file, Current_page.get_progress(i))
        write_result(result_file, Current_page.search_elements())
        Current_page = Webpage(Current_page.next_page_link, pagination_info, search_info)
        print(f"Over {(i + 1) * contain_num} Queries Processed")
        i += 1


if __name__ == "__main__":
    # INDEED COOK JOB SEARCH
    # URL and PAGINATION
    url = "https://au.indeed.com/jobs?q=cook&vjk=6493e1124836c3fc"
    pagination = dict(location="div", classname="pagination", query_line="start=")
    # QUERY SEARCH
    job_search = dict(tag_location="h2", classname="jobTitle")
    company_search = dict(tag_location="span", classname="companyName")
    compnay_location = dict(tag_location="div", classname="companyLocation")
    search_info = (["Job Title", "Company", "Location"], job_search, company_search, compnay_location)
    # RUN PROGRAM
    run(url, pagination, search_info, "INDEED-process.txt", "INDEED-result.csv", 15)
