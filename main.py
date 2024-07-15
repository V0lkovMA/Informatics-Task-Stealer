from bs4 import BeautifulSoup
import urllib.request
import csv
from copy import deepcopy


def get_cur_tasks_id(cur_tasks_file_name):
    cur_tasks_file = open(cur_tasks_file_name, 'r', encoding = "utf8")
    cur_tasks = list(s.split('\t') for s in cur_tasks_file.readlines())

    cur_tasks_id = list()
    for line in cur_tasks:
        try:
            cur_tasks_id.append(int(line[2]))
        except ValueError:
            continue
    return cur_tasks_id
    
    
def get_urls(urls_file_name):
    return open(urls_file_name, 'r', encoding = "utf8").readlines()
    
    
def get_html_code(url):
    #print(url)

    fp = urllib.request.urlopen(urllib.request.Request(url, headers = {"User-Agent": "Chrome/35.0.1916.47"}))
    res = fp.read().decode("utf8")
    fp.close()
    return res


def get_tasks(contest_html):
    bs = BeautifulSoup(contest_html, features="html.parser")

    contest_name = bs.h1.text

    task_full_names = list()
    task_full_names.append(bs.h4.text)

    task_urls = list("https://informatics.msk.ru/mod/statements/" + line['href'] for line in bs.select("body > div > div > div > div > section > aside > section > div > div > div > ul > li > a"))
    #print("task urls built")

    for url in task_urls:
        #print("building task urls, url =", url)
        cur_bs = BeautifulSoup(get_html_code(url), features="html.parser")
        task_full_names.append(cur_bs.h4.text)
    #print("task full names built")

    task_table = list()
    for full_name in task_full_names:
        #print("building task table, full name = ", full_name)
        task_id = full_name[full_name.find('№') + 1:full_name.find('.')]
        task_name = full_name[full_name.find('.') + 2:]
        task_table.append([task_name, task_id, contest_name])
    #print("task table built")

    return task_table


def delete_same_tasks(task_table, cur_tasks_id):
    res = list()
    for line in task_table:
        if not int(line[1]) in cur_tasks_id:
            res.append(line)
    return res


urls = get_urls("urls.txt")
html_codes = list(get_html_code(s) for s in urls)

task_table = list()
for code in html_codes:
    task_table += get_tasks(code)

print("total task table built")
print(task_table)


cur_tasks_id = list()
cur_task_files = ["ЛМШ 2024 - Информатикс.tsv", "ЛМШ 2024 - Новые задачи.tsv"]
for file in cur_task_files:
    cur_tasks_id += get_cur_tasks_id(file)
task_table = delete_same_tasks(task_table, cur_tasks_id)

#print(task_table)

res_file = open("result.csv", 'w', newline = '', encoding = 'utf8')
writer = csv.writer(res_file, delimiter = '\t')
for line in task_table:
    writer.writerow(line)
res_file.close()

print("Finished")