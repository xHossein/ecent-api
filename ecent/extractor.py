from typing import List
from ecent.types import Assignment, Course, ShortAssignment, ShortCourse,Resource, Url
import html
import re
from bs4 import BeautifulSoup as bs


def extract_short_course(text) -> List[ShortCourse]:
    courses_box = html.unescape(re.findall(r'class="courses frontpage-course-list-enrolled"(.*)id="skipmycourses"',text)[0])
    courses_id = re.findall(r'data-courseid="(.*?)"',courses_box)[:-1]
    courses_title = re.findall(r'course/view.php\?id=\d+">(.*?)</a>',courses_box)[:-1]
    courses_master = re.findall(r'course=1">(.*?)</a></li>',courses_box)
    return [ShortCourse(**{
                "id": courses_id[i],
                "link": f'https://ecent2.guilan.ac.ir/course/view.php?id={courses_id[i]}',
                "title": courses_title[i],
                "master": courses_master[i],
                }) 
            for i in range(len(courses_id))]

def extract_course(text) -> Course:
    adobe_connect = (re.findall(r'"(https://ecent2.guilan.ac.ir/mod/adobeconnect/view.php\?id=\d*?)"',text) or [None])[0]
    id = re.findall(r'id=(\d*?)" aria-current="page"',text)[0]
    link = f'https://ecent2.guilan.ac.ir/course/view.php?id={id}'
    title = re.findall(r'class="page-header-headings"><h1>(.*?)<',text)[0]
    return Course(**{
                'id': id,
                'link': link,
                'title': title,
                'adobe_connect': adobe_connect,
                'urls': extract_urls(text),
                'resources': extract_resources(text),
                'assignments': extract_short_assignments(text),
                })

def extract_resources(text) -> List[Resource]:
    soup = bs(text,'lxml')
    resource_class = soup.find_all(name='li', class_='activity resource modtype_resource')
    resources = []
    for item in resource_class:
        div = item.find(name='div',class_='activityinstance')
        a = div.find('a')
        link = a['href']
        id = a['href'].split('id=')[1]
        title = a.find(name='span',class_='instancename').contents[0]
        details = div.find(class_='resourcelinkdetails').text
        unit = 'MB' if 'مگابایت' in details else 'KB'
        size = re.findall(r'[+-]?(\d+([.]\d*)?(e[+-]?\d+)?|[.]\d+(e[+-]?\d+)?)',details)[0][0] + " " + unit
        type = (re.findall(r'\((.*)\)',details) or ['UNKNOWN'])[0]
        resources.append(Resource(**{
                        'id': id,
                        'link': link,
                        'title': title,
                        'size': size,
                        'type': type,
                    }))
    return resources

def extract_short_assignments(text) -> List[ShortAssignment]:
    soup = bs(text,'lxml')
    assign_class = soup.find_all(name='li', class_='activity assign modtype_assign')
    assignments = []
    for item in assign_class:
        div = item.find(name='div',class_='activityinstance')
        a = div.find('a')
        link = a['href']
        id = a['href'].split('id=')[1]
        title = a.find(name='span',class_='instancename').contents[0]
        assignments.append(ShortAssignment(**{
                        'id': id,
                        'link': link,
                        'title': title,
                    }))
    return assignments

def extract_urls(text) -> List[Url]:
    soup = bs(text,'lxml')
    url_class = soup.find_all(name='li', class_='activity url modtype_url')
    urls = []
    for item in url_class:
        div = item.find(name='div',class_='activityinstance')
        a = div.find('a')
        link = a['href']
        id = a['href'].split('id=')[1]
        title = a.find(name='span',class_='instancename').contents[0]
        urls.append(Url(**{
                        'id': id,
                        'link': link,
                        'title': title,
                    }))
    return urls

def extract_assignment(text) -> Assignment:
    id = re.findall(r'name="id" value="(.*?)"',text)[0]
    title = re.findall(r'maincontent"></span><h2>(.*?)<',text)[0]
    details  = re.findall(r'cell c1 lastcol" style="">(.*?)<',text)
    return Assignment(**{
                    'id':id,
                    'title': title,
                    'status': details[0],
                    'deadline': details[2],
                    'remaining_time': details[3],
                    'last_change': None if details[4]=='-' else details[4],
                })