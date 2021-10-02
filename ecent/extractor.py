from typing import List
from ecent.types import Assignment, Course, Grade, ShortAssignment, ShortCourse,Resource, Url
import html
import re
from bs4 import BeautifulSoup as bs
from ecent.utils import Parser

def extract_short_course(data: str) -> List[ShortCourse]:
    courses_box = html.unescape(re.findall(r'class="courses frontpage-course-list-enrolled"(.*)id="skipmycourses"', data)[0])
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

def extract_course(data: str) -> Course:
    adobe_connect = (re.findall(r'"(https://ecent2.guilan.ac.ir/mod/adobeconnect/view.php\?id=\d*?)"', data) or [None])[0]
    id = re.findall(r'id=(\d*?)" aria-current="page"', data)[0]
    link = f'https://ecent2.guilan.ac.ir/course/view.php?id={id}'
    title = re.findall(r'class="page-header-headings"><h1>(.*?)<', data)[0]
    return Course(**{
                'id': id,
                'link': link,
                'title': title,
                'adobe_connect_link': adobe_connect,
                'urls': extract_urls(data),
                'resources': extract_resources(data),
                'short_assignments': extract_short_assignments(data),
                })

def extract_resources(data: str) -> List[Resource]:
    soup = bs(data, 'html.parser')
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
        type = (re.findall(r' (.{3,6})$',details) or ['UNKNOWN'])[0].replace('(','').replace(')','')
        resources.append(Resource(**{
                        'id': id,
                        'link': link,
                        'title': title,
                        'size': size,
                        'type': type,
                    }))
    return resources

def extract_short_assignments(data: str) -> List[ShortAssignment]:
    soup = bs(data, 'html.parser')
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

def extract_urls(data: str) -> List[Url]:
    soup = bs(data, 'html.parser')
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

def extract_assignment(data: str) -> Assignment:
    id = re.findall(r'name="id" value="(.*?)"', data)[0]
    title = re.findall(r'maincontent"></span><h2>(.*?)<', data)[0]
    details  = re.findall(r'cell c1 lastcol" style="">(.*?)<', data)
    return Assignment(**{
                    'id':id,
                    'link': f'https://ecent2.guilan.ac.ir/mod/assign/view.php?id={id}',
                    'title': title,
                    'is_submitted': True if details[0] == 'برای تصحیح تحویل داده شده است' else False,
                    'deadline': Parser.date(details[2]),
                    'remaining_time': None if details[0] == 'برای تصحیح تحویل داده شده است' else Parser.remaining(details[3]),
                    'last_change': None if details[4]=='-' else Parser.date(details[4]),
                })
    
def extract_join_link(data: str):
    soup = bs(data, 'html.parser')
    input_element = soup.find('input', {'value': 'پيوستن به كلاس'})
    return re.findall(r"window.open\('(.*?)'", input_element.get('onclick'))[0]

def extract_grades(data: str):
    soup = bs(data, 'html.parser')
    elements = soup.find_all('tr', class_='', id=re.compile('^grade-report-overview'))
    grades = []
    for element in elements:
        a = element.find('a')
        link = a['href']
        title = a.contents[0]
        if 'ارتباط با کارشناسان گروه' in title:
            continue
        grade = element.find(class_='cell c1').contents[0]
        grades.append(
            Grade(**{
                'link': link,
                'title': title,
                'grade': grade
            })
        )
    return grades
