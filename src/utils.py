"""Utility functions for fetching and handling HTTP requests."""
import httpx
import os
from typing import Optional


def create_proxy_config(proxy_url: Optional[str]) -> Optional[str]:
    """Parse Apify proxy URL and create httpx-compatible proxy string.
    
    Args:
        proxy_url: Apify proxy URL in format http://user:pass@proxy.apify.com:8000
        
    Returns:
        Proxy URL string or None
    """
    if not proxy_url:
        return None
    return proxy_url


async def fetch(url: str, proxy_url: Optional[str] = None, max_retries: int = 3) -> str:
    """Fetch a URL with retries and optional proxy.
    
    Args:
        url: URL to fetch
        proxy_url: Optional proxy URL
        max_retries: Maximum number of retry attempts
        
    Returns:
        HTML content as string
        
    Raises:
        httpx.HTTPError: If all retries fail
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # httpx uses mounts for proxies, not proxies dict
    client_kwargs = {'timeout': 90.0, 'follow_redirects': True}
    if proxy_url:
        client_kwargs['proxy'] = proxy_url
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(**client_kwargs) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                # Check for minimal content
                if len(response.text) < 500:
                    raise ValueError(f"Response too short ({len(response.text)} bytes) - likely blocked")
                
                return response.text
                
        except (httpx.HTTPError, ValueError) as e:
            if attempt == max_retries - 1:
                raise
            # Exponential backoff
            import asyncio
            await asyncio.sleep(2 ** attempt)
    
    raise httpx.HTTPError(f"Failed to fetch {url} after {max_retries} attempts")
