"""Parser module for extracting professional data from Houzz HTML."""
from bs4 import BeautifulSoup
import re
import json


def extract_professionals(html: str) -> list[dict]:
    """Extract professional listings from Houzz directory page.
    
    Args:
        html: Raw HTML content from Houzz professionals directory
        
    Returns:
        List of professional dictionaries with extracted fields
    """
    soup = BeautifulSoup(html, 'lxml')
    professionals = []
    
    # Try to find JSON-LD structured data first
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'ItemList':
                for item in data.get('itemListElement', []):
                    if isinstance(item, dict):
                        professionals.append(_parse_json_ld_item(item))
        except (json.JSONDecodeError, AttributeError):
            pass
    
    # Fallback: Parse HTML directly for professional cards
    if not professionals:
        # Look for common professional card patterns
        cards = soup.find_all(['div', 'article'], class_=re.compile(r'professional|pro-card|listing', re.I))
        for card in cards:
            pro_data = _parse_professional_card(card)
            if pro_data.get('name'):  # Only add if we got a name
                professionals.append(pro_data)
    
    return professionals


def _parse_json_ld_item(item: dict) -> dict:
    """Parse a JSON-LD professional item."""
    person = item.get('item', {})
    return {
        'name': person.get('name'),
        'url': person.get('url'),
        'rating': person.get('aggregateRating', {}).get('ratingValue'),
        'reviewCount': person.get('aggregateRating', {}).get('reviewCount'),
        'address': person.get('address', {}).get('streetAddress'),
        'city': person.get('address', {}).get('addressLocality'),
        'state': person.get('address', {}).get('addressRegion'),
        'zip': person.get('address', {}).get('postalCode'),
        'phone': person.get('telephone'),
        'description': person.get('description'),
    }


def _parse_professional_card(card) -> dict:
    """Parse a professional card HTML element."""
    data = {
        'name': None,
        'url': None,
        'rating': None,
        'reviewCount': None,
        'location': None,
        'specialty': None,
        'description': None,
        'phone': None,
        'website': None,
    }
    
    # Name and URL
    name_link = card.find('a', href=re.compile(r'/pro/'))
    if name_link:
        data['name'] = name_link.get_text(strip=True)
        data['url'] = 'https://www.houzz.com' + name_link.get('href') if name_link.get('href', '').startswith('/') else name_link.get('href')
    
    # Rating
    rating_elem = card.find(string=re.compile(r'\\d+\\.\\d+\\s*★|★\\s*\\d+'))
    if rating_elem:
        match = re.search(r'(\\d+\\.\\d+)', rating_elem)
        if match:
            data['rating'] = float(match.group(1))
    
    # Review count
    review_elem = card.find(string=re.compile(r'\\d+\\s*review', re.I))
    if review_elem:
        match = re.search(r'(\\d+)', review_elem)
        if match:
            data['reviewCount'] = int(match.group(1))
    
    # Location
    location_elem = card.find(string=re.compile(r',\\s*[A-Z]{2}\\b'))
    if location_elem:
        data['location'] = location_elem.strip()
    
    # Phone
    phone_elem = card.find('a', href=re.compile(r'^tel:'))
    if phone_elem:
        data['phone'] = phone_elem.get_text(strip=True)
    
    # Description
    desc_elem = card.find(['p', 'div'], class_=re.compile(r'description|bio|about', re.I))
    if desc_elem:
        data['description'] = desc_elem.get_text(strip=True)
    
    return data


def extract_next_page_url(html: str, current_url: str) -> str | None:
    """Extract next page URL from pagination links.
    
    Args:
        html: Raw HTML content
        current_url: Current page URL for context
        
    Returns:
        Next page URL or None if no next page
    """
    soup = BeautifulSoup(html, 'lxml')
    
    # Look for common pagination patterns
    next_link = (
        soup.find('a', text=re.compile(r'next', re.I)) or
        soup.find('a', rel='next') or
        soup.find('a', class_=re.compile(r'next|pagination-next', re.I))
    )
    
    if next_link and next_link.get('href'):
        href = next_link.get('href')
        if href.startswith('/'):
            return 'https://www.houzz.com' + href
        elif href.startswith('http'):
            return href
    
    return None
