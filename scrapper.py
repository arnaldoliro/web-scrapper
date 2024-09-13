import requests
from bs4 import BeautifulSoup

def scrap_courses():
    response = requests.get('https://alunoweb.ufba.br/SiacWWW/ListaCursosEmentaPublico.do?cdGrauCurso=01')

    if response.status_code != 200:
        print(f'Erro ao acessar o site: {response.status_code}')
        return None

    html = BeautifulSoup(response.text, 'html.parser')

    links = html.find_all('a')

    unique_courses = set()

    for link in links:
        course = link.get_text(strip=True)
        if course:
            parts = course.split('  ')
            if len(parts) > 1:
                unique_courses.add(parts[0])

    courses = sorted(unique_courses)

    for course in courses:
        response = requests.post('http://localhost:3000/courses', json={'name': course})
        if response.status_code == 201:
            print(f'Curso "{course}" foi adicionado com sucesso.')
        else:
            print(f'Erro ao adicionar o curso "{course}": {response.status_code}')

scrap_courses()