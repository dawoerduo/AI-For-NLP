# search subway stations info from web crawel
# created by Nan Apr.18.2019

import requests
import re
import time


seed = "http://service.shmetro.com"
target_html=seed+"/axlcz01/index.htm"
target_pattern=re.compile(seed+"/axlcz\d+/index\.htm")


index = []
subway_map = {}

def get_page(url):
    try:
        response = requests.get(url)
        #       print (response.status_code)
        response.encoding = 'utf-8'
        html_content = response.text
        #       print (html_content)
        url_pattern1 = re.compile('href="/czxx/index\.htm\?id=\d+&stationname=([\w\s]+)">')
        url_pattern2 = re.compile('<div class="axlcz(\d{2})">')
        subway_station_menu = url_pattern1.findall(html_content)
        subway_line_num = url_pattern2.findall(html_content)
        return subway_station_menu,subway_line_num
    except:
        return []


def add_to_index(index, station, connect):
    if not connect: return
    for entry in index:
        if entry[0] == station:
            if connect not in entry[1]:
                entry[1].append(connect)
            return
    index.append([station, [connect]])

    return

def add_page_to_index( stations, linenum):
    subway_map[linenum]=[]
    for i,e in enumerate(stations):
        subway_map[linenum].append(e)
        if i == 0 :
            add_to_index(index,e,stations[i+1])
            continue
        if i == len(stations)-1:
            add_to_index(index,e,stations[i-1])
            break
        add_to_index(index,e,stations[i-1])
        add_to_index(index,e,stations[i+1])
    return


def get_next_target(page):
    pos=re.search(r'<a\s+href=',page)
    if not pos:
        return None,0
    start_link = pos.span()[1]

    star_quote=page.find('"',start_link)
    end_quote =page.find('"',star_quote+1)
    url_entity=page[star_quote+1:end_quote]
    return url_entity, end_quote

def get_all_links(url):
    response=requests.get(url)
    if response.status_code !=200:
        return []
    content=response.text
    links=[]
    while True :
        url_entity, endpos = get_next_target(content)
        if not url_entity: break
        if url_entity.startswith('/'):
            links.append(seed+url_entity)
        content = content[endpos:]
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    target =[]
    srcflag=0
    while tocrawl:
        url = tocrawl.pop()
        print ("process :",url)
        if url not in crawled:
            if url == target_html:
                srcflag=1
                break
                #  entry=requests.get(seed+url)
                #  metroline=get_page(entry)
                #  add_page_to_index(metroline,'一号线')
            else:
     #          time.sleep(1)
                union(tocrawl, get_all_links(url))
                crawled.append(url)
    print("search complete")
    if not srcflag : return []
    getlinks = get_all_links(url)
    for element in getlinks:
        page = target_pattern.match(element)
        if page:
            target.append(page.group(0))
    return set(target)



#result=crawl_web(seed)
#print (result)