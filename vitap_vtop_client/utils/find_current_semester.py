from bs4 import BeautifulSoup


def find_current_sem_sub_id(html: str) -> str | None:
    """Parse semesterSubId from a page containing a semester select."""
    soup = BeautifulSoup(html, 'html.parser')

    select = soup.find('select', attrs={'name': 'semesterSubId'})
    if select:
        option = select.find('option', selected=True)
        if option and option.get('value'):
            return option['value']
        first_option = select.find('option')
        if first_option and first_option.get('value'):
            return first_option['value']

    input_el = soup.find('input', attrs={'name': 'semesterSubId'})
    if input_el and input_el.get('value'):
        return input_el['value']
    return None
