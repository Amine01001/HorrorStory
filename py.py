import requests
from bs4 import BeautifulSoup
import os
import sys

directory = 'Stories'
ascii_art = """\


 ██░ ██  ▒█████   ██▀███   ██▀███   ▒█████   ██▀███  
▓██░ ██▒▒██▒  ██▒▓██ ▒ ██▒▓██ ▒ ██▒▒██▒  ██▒▓██ ▒ ██▒
▒██▀▀██░▒██░  ██▒▓██ ░▄█ ▒▓██ ░▄█ ▒▒██░  ██▒▓██ ░▄█ ▒
░▓█ ░██ ▒██   ██░▒██▀▀█▄  ▒██▀▀█▄  ▒██   ██░▒██▀▀█▄  
░▓█▒░██▓░ ████▓▒░░██▓ ▒██▒░██▓ ▒██▒░ ████▓▒░░██▓ ▒██▒
 ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ▒ ░▒░ ░  ░ ▒ ▒░   ░▒ ░ ▒░  ░▒ ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░
 ░  ░░ ░░ ░ ░ ▒    ░░   ░   ░░   ░ ░ ░ ░ ▒    ░░   ░ 
 ░  ░  ░    ░ ░     ░        ░         ░ ░     ░     
"""

# Run the animation
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
def print_message(story_count):
    clear_screen()
    message = f"[+] You have {story_count} Stories saved [ Story : {story_name} ]"
    print(ascii_art)
    print("\n")
    print(message)
    sys.stdout.flush()
story_count = 0
story_name = ""
print_message(story_count)
def parseno(text, start_delim, end_delim):
    start_index = text.find(start_delim)
    if start_index == -1:
        return None

    start_index += len(start_delim)
    end_index = text.find(end_delim, start_index)
    if end_index == -1:
        return None

    return text[start_index:end_index]
def antidup(lst):
    unique_list = []
    seen = set()
    for item in lst:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list
def htt(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    return text
def parse(text, start_delim, end_delim):
    def parse_segment(start_index):
        results = []
        while True:
            start_index = text.find(start_delim, start_index)
            if start_index == -1:
                break
            start_index += len(start_delim)
            end_index = text.find(end_delim, start_index)
            if end_index == -1:
                break
            result = text[start_index:end_index]
            results.append(result)
            start_index = end_index + len(end_delim)
            results.extend(parse_segment(start_index))
            break
        return results
    return parse_segment(0)
r = requests.get('https://www.reddit.com/svc/shreddit/community-more-posts/hot/?after=&t=DAY&name=nosleep&feedLength=1000&adDistance=4').text
results = antidup(parse(r, "permalink=\"", "\""))
for result in results:
    story = requests.get("https://www.reddit.com"+result).text
    plain = htt(story)
    final = parseno(plain, "MOD", "Read more")
    name = parseno(result , 'comments/',"/")
    namee = parseno(result, name+"/",'/')
    storyname = namee.replace('_', ' ') +".txt"
    file_path = os.path.join(directory, storyname)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(final)
        story_count += 1
        story_name = storyname
        print_message(story_count)
for i in range(10):
    creepyreq = requests.get("https://www.creepypasta.com/?_page="+str(i)).text
    links = parse(creepyreq, "<div class=\"pt-cv-ifield\"><a href=\"", "\" class=\"")
    for link in links:
        yes = requests.get(link).text
        no = htt(yes)
        final = parseno(no, " Search Advertisement Please wait... ", " Credit:")
        if final is None:
            continue
        name = parseno(link, "https://www.creepypasta.com/", "/")
        storyname = name.replace('-', ' ') + ".txt"
        file_path = os.path.join(directory, storyname)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(final)
            story_count += 1
            story_name = storyname
            print_message(story_count)
print_message(story_count)