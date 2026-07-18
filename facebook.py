#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ███╗   ███╗███████╗████████╗ █████╗  ██████╗ ███╗   ██╗███████╗██╗  ██╗  ║
║     ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝╚██╗██╔╝  ║
║     ██╔████╔██║█████╗     ██║   ███████║██║   ██║██╔██╗ ██║█████╗   ╚███╔╝   ║
║     ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║╚██╗██║██╔══╝   ██╔██╗   ║
║     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██║ ╚████║███████╗██╔╝ ██╗  ║
║     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ║
║                                                                               ║
║     ███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  ██████╗ ██╗  ██╗       ║
║     ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝       ║
║     █████╗  ███████║██║     █████╗  ██████╔╝██║   ██║██║   ██║█████╔╝        ║
║     ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔═██╗        ║
║     ██║     ██║  ██║╚██████╗███████╗██████  ╚██████╔╝╚██████╔╝██║  ██╗       ║
║     ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝       ║
║                                                                               ║
║                    FACEBOOK INTELLIGENCE SUITE v9.0.0                         ║
║                                                                               ║
║                      Author: SYLHETYHACKVENGER                                ║
║                           (THE-ERROR808)                                     ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Features:                                                                     ║
║   ✅ Account Checker (Email/Phone/Username)                                   ║
║   ✅ Full Profile Extraction                                                  ║
║   ✅ Social Mapper (Multi-Platform)                                           ║
║   ✅ Batch Processing with Threading                                          ║
║   ✅ SQLite Database Storage                                                  ║
║   ✅ Multi-Format Export (JSON/CSV/HTML)                                      ║
║   ✅ Rich TUI Interface                                                       ║
║   ✅ Fallback CLI Mode                                                        ║
║   ✅ Rate Limiting & Anti-Detection                                           ║
║   ✅ Proxy Support (Optional)                                                 ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import re
import json
import time
import csv
import sqlite3
import hashlib
import logging
import random
import threading
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from contextlib import contextmanager
import traceback
import warnings

warnings.filterwarnings("ignore")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VERSION & AUTHOR INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERSION = "9.0.0"
AUTHOR = "SYLHETYHACKVENGER"
HANDLE = "THE-ERROR808"
TOOL_NAME = "METAØNEX"
DESCRIPTION = "Facebook Intelligence Suite - Complete Reconnaissance Tool"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEPENDENCY CHECK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[!] requests not installed. Run: pip install requests")

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    print("[!] beautifulsoup4 not installed. Run: pip install beautifulsoup4")

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.text import Text
    from rich import box
    from rich.align import Align
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("[!] rich not installed. Run: pip install rich")

if not REQUESTS_AVAILABLE or not BEAUTIFULSOUP_AVAILABLE:
    print("\n[ERROR] Required dependencies missing. Please install:")
    print("pip install requests beautifulsoup4")
    sys.exit(1)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LOGGING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metaohex_intelligence.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONSTANTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FB_MBASIC = "https://mbasic.facebook.com"
FB_LOGIN = f"{FB_MBASIC}/login"
FB_IDENTIFY = f"{FB_MBASIC}/login/identify"
FB_RECOVER = f"{FB_MBASIC}/recover/initiate"

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'
]

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt"
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# BANNER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ███╗   ███╗███████╗████████╗ █████╗  ██████╗ ███╗   ██╗███████╗██╗  ██╗  ║
║     ████╗ ████║██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║██╔════╝╚██╗██╔╝  ║
║     ██╔████╔██║█████╗     ██║   ███████║██║   ██║██╔██╗ ██║█████╗   ╚███╔╝   ║
║     ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║╚██╗██║██╔══╝   ██╔██╗   ║
║     ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██║ ╚████║███████╗██╔╝ ██╗  ║
║     ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ║
║                                                                               ║
║     ███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  ██████╗ ██╗  ██╗       ║
║     ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝       ║
║     █████╗  ███████║██║     █████╗  ██████╔╝██║   ██║██║   ██║█████╔╝        ║
║     ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║██║   ██║██╔═██╗        ║
║     ██║     ██║  ██║╚██████╗███████╗███████║╚██████╔╝╚██████╔╝██║  ██╗       ║
║     ╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝       ║
║                                                                               ║
║                    FACEBOOK INTELLIGENCE SUITE v9.0.0                         ║
║                                                                               ║
║                      Author: SYLHETYHACKVENGER                                ║
║                           (THE-ERROR808)                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class ProfilePhoto:
    url: str = ""
    width: int = 0
    height: int = 0
    downloaded_path: str = ""
    
@dataclass
class WorkExperience:
    company: str = ""
    role: str = ""
    start_date: str = ""
    end_date: str = ""
    location: str = ""
    description: str = ""
    is_current: bool = False

@dataclass
class Education:
    school: str = ""
    degree: str = ""
    field_of_study: str = ""
    start_date: str = ""
    end_date: str = ""
    grade: str = ""
    is_current: bool = False

@dataclass
class AccountInfo:
    """Complete Facebook account information"""
    # Identification
    user_id: str = ""
    username: str = ""
    name: str = ""
    profile_url: str = ""
    
    # Contact
    email: str = ""
    phone: str = ""
    address: str = ""
    
    # Profile
    gender: str = ""
    birthday: str = ""
    bio: str = ""
    is_verified: bool = False
    is_memorialized: bool = False
    is_private: bool = False
    is_business: bool = False
    
    # Media
    profile_photo: Optional[ProfilePhoto] = None
    cover_photo: str = ""
    
    # History
    work_history: List[WorkExperience] = field(default_factory=list)
    education_history: List[Education] = field(default_factory=list)
    
    # Statistics
    friends_count: int = 0
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    photos_count: int = 0
    videos_count: int = 0
    
    # Metadata
    discovery_method: str = ""
    status: str = ""
    error_message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    confidence_score: float = 0.0
    source_url: str = ""
    processing_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_csv_row(self) -> List[str]:
        return [
            self.user_id, self.username, self.name, self.email, self.phone,
            self.gender, self.birthday, self.profile_url,
            self.profile_photo.url if self.profile_photo else "",
            str(self.is_verified), str(self.friends_count), self.status, self.timestamp
        ]
    
    @staticmethod
    def csv_headers() -> List[str]:
        return [
            "User ID", "Username", "Name", "Email", "Phone",
            "Gender", "Birthday", "Profile URL", "Profile Photo",
            "Verified", "Friends Count", "Status", "Timestamp"
        ]

@dataclass
class SearchResult:
    input_query: str = ""
    query_type: str = ""
    account: Optional[AccountInfo] = None
    found: bool = False
    error: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    duration: float = 0.0
    attempts: int = 0
    proxy_used: str = ""
    user_agent: str = ""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROXY MANAGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ProxyManager:
    """Intelligent proxy management with rotation and validation"""
    
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.failed_proxies = set()
        self.lock = Lock()
        
    def load_proxies(self) -> List[str]:
        """Load proxies from sources"""
        proxies = []
        
        # Try to load from each source
        for source in PROXY_SOURCES:
            try:
                response = requests.get(source, timeout=10)
                for line in response.text.splitlines():
                    line = line.strip()
                    if ':' in line and not line.startswith('#'):
                        proxies.append(line)
            except:
                continue
                
        # Format proxies
        for proxy in proxies:
            parts = proxy.split(':')
            if len(parts) == 2:
                self.proxies.append({
                    'host': parts[0],
                    'port': int(parts[1]),
                    'protocol': 'http',
                    'full': f"http://{parts[0]}:{parts[1]}"
                })
                
        logger.info(f"[+] Loaded {len(self.proxies)} proxies")
        return proxies
        
    def get_proxy(self) -> Optional[str]:
        """Get next working proxy"""
        with self.lock:
            if not self.proxies:
                return None
                
            attempts = 0
            while attempts < len(self.proxies):
                proxy = self.proxies[self.current_index]
                self.current_index = (self.current_index + 1) % len(self.proxies)
                
                if proxy['full'] not in self.failed_proxies:
                    return proxy['full']
                    
                attempts += 1
                
            return None
            
    def mark_failed(self, proxy: str):
        """Mark proxy as failed"""
        with self.lock:
            self.failed_proxies.add(proxy)
            
    def reset(self):
        """Reset failed proxies"""
        with self.lock:
            self.failed_proxies.clear()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CORE ENGINE - FACEBOOK CHECKER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class FacebookChecker:
    """Core Facebook account checker engine"""
    
    def __init__(self, use_proxy: bool = False, timeout: int = 30, max_retries: int = 3):
        self.use_proxy = use_proxy
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = None
        self.proxy_manager = ProxyManager() if use_proxy else None
        self.current_proxy = None
        self.rate_limiter = None
        self._initialize_session()
        
    def _initialize_session(self):
        """Initialize HTTP session with proper headers"""
        self.session = requests.Session()
        
        # Set random user agent
        user_agent = random.choice(USER_AGENTS)
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Configure retries
        retry = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504, 520, 521, 522, 524],
            allowed_methods=['GET', 'POST']
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
    def _get_proxy(self) -> Optional[str]:
        """Get proxy for request"""
        if self.use_proxy and self.proxy_manager:
            return self.proxy_manager.get_proxy()
        return None
        
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make request with proxy support"""
        # Add random delay
        time.sleep(random.uniform(0.5, 2.0))
        
        # Get proxy if enabled
        if self.use_proxy:
            proxy = self._get_proxy()
            if proxy:
                self.current_proxy = proxy
                self.session.proxies = {
                    'http': proxy,
                    'https': proxy
                }
                
        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            
            # Check if proxy failed
            if response.status_code in [407, 502, 503, 504] and self.current_proxy:
                self.proxy_manager.mark_failed(self.current_proxy)
                
            return response
            
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if self.current_proxy:
                self.proxy_manager.mark_failed(self.current_proxy)
            raise
            
    def check_account(self, query: str) -> SearchResult:
        """Main method to check if a Facebook account exists"""
        start_time = time.time()
        result = SearchResult(input_query=query.strip())
        result.attempts = 1
        
        try:
            query = query.strip()
            result.query_type = self._detect_query_type(query)
            result.user_agent = self.session.headers.get('User-Agent', '')
            
            # Perform check based on query type
            if result.query_type == "phone":
                result = self._check_by_phone(query, result)
            elif result.query_type == "email":
                result = self._check_by_email(query, result)
            else:
                result = self._check_by_username(query, result)
                
        except Exception as e:
            result.found = False
            result.error = str(e)
            logger.error(f"Check failed: {e}")
            logger.debug(traceback.format_exc())
            
        result.duration = time.time() - start_time
        result.timestamp = datetime.now().isoformat()
        result.proxy_used = self.current_proxy or "Direct"
        
        return result
        
    def _detect_query_type(self, query: str) -> str:
        """Detect the type of query"""
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
            return "email"
        if re.match(r'^\+?[0-9\s\-()]{8,20}$', query):
            return "phone"
        if query.isdigit():
            return "user_id"
        return "username"
        
    def _check_by_phone(self, phone: str, result: SearchResult) -> SearchResult:
        """Check account by phone number"""
        # Clean phone number
        phone = re.sub(r'[\s\-()]', '', phone)
        if not phone.startswith('+'):
            phone = '+' + phone
            
        try:
            # Get the identify page
            response = self._make_request(
                'GET',
                FB_IDENTIFY,
                params={'ctx': 'recover', 'search_attempts': 0}
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to load page: {response.status_code}")
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract form tokens
            lsd = soup.find('input', {'name': 'lsd'})
            jazoest = soup.find('input', {'name': 'jazoest'})
            
            if not lsd or not jazoest:
                lsd = soup.find('input', {'name': 'lsd', 'type': 'hidden'})
                jazoest = soup.find('input', {'name': 'jazoest', 'type': 'hidden'})
                
            if not lsd or not jazoest:
                raise Exception("Could not find form tokens")
                
            # Prepare form data
            form_data = {
                'lsd': lsd.get('value', ''),
                'jazoest': jazoest.get('value', ''),
                'email': phone,
                'did_submit': 'Search'
            }
            
            # Submit the form
            response = self._make_request(
                'POST',
                FB_IDENTIFY,
                data=form_data,
                allow_redirects=True,
                headers={'Referer': FB_IDENTIFY}
            )
            
            if response.status_code != 200:
                raise Exception(f"Search failed: {response.status_code}")
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for error messages
            error_elements = soup.find_all('div', class_='_4rbf')
            for error in error_elements:
                error_text = error.text.lower()
                if "not associated" in error_text or "doesn't match" in error_text:
                    result.found = False
                    result.error = f"Phone {phone} not associated with any account"
                    return result
                    
            # Extract account information
            account = self._extract_account_info(soup, phone, "phone")
            
            if account and account.name:
                result.found = True
                result.account = account
            else:
                result.found = False
                result.error = "Could not extract account information"
                
        except requests.exceptions.Timeout:
            raise Exception("Request timed out - please try again")
        except requests.exceptions.ConnectionError:
            raise Exception("Connection error - check your internet connection")
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
            
        return result
        
    def _check_by_email(self, email: str, result: SearchResult) -> SearchResult:
        """Check account by email address"""
        try:
            response = self._make_request(
                'GET',
                FB_IDENTIFY,
                params={'ctx': 'recover', 'search_attempts': 0}
            )
            
            if response.status_code != 200:
                raise Exception(f"Failed to load page: {response.status_code}")
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            lsd = soup.find('input', {'name': 'lsd'})
            jazoest = soup.find('input', {'name': 'jazoest'})
            
            if not lsd or not jazoest:
                raise Exception("Could not find form tokens")
                
            form_data = {
                'lsd': lsd.get('value', ''),
                'jazoest': jazoest.get('value', ''),
                'email': email,
                'did_submit': 'Search'
            }
            
            response = self._make_request(
                'POST',
                FB_IDENTIFY,
                data=form_data,
                allow_redirects=True
            )
            
            if response.status_code != 200:
                raise Exception(f"Search failed: {response.status_code}")
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            error_elements = soup.find_all('div', class_='_4rbf')
            for error in error_elements:
                error_text = error.text.lower()
                if "not associated" in error_text or "doesn't match" in error_text:
                    result.found = False
                    result.error = f"Email {email} not associated with any account"
                    return result
                    
            account = self._extract_account_info(soup, email, "email")
            
            if account and account.name:
                result.found = True
                result.account = account
            else:
                result.found = False
                result.error = "Could not extract account information"
                
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
            
        return result
        
    def _check_by_username(self, username: str, result: SearchResult) -> SearchResult:
        """Check account by username"""
        try:
            response = self._make_request(
                'GET',
                f"{FB_MBASIC}/{username}",
                allow_redirects=True
            )
            
            if response.status_code == 404:
                result.found = False
                result.error = f"Username {username} not found"
                return result
                
            if response.status_code != 200:
                raise Exception(f"Failed to access profile: {response.status_code}")
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if it's a valid profile
            title = soup.find('title')
            if not title or "Facebook" not in title.text:
                result.found = False
                result.error = f"Username {username} not found"
                return result
                
            account = self._extract_account_info(soup, username, "username")
            
            if account and account.name:
                result.found = True
                result.account = account
            else:
                result.found = False
                result.error = "Could not extract profile information"
                
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
            
        return result
        
    def _extract_account_info(self, soup: BeautifulSoup, query: str, query_type: str) -> Optional[AccountInfo]:
        """Extract account information from HTML"""
        account = AccountInfo()
        account.discovery_method = query_type
        account.source_url = f"https://facebook.com/{query}"
        
        # Extract name - try multiple methods
        name_selectors = [
            'div.bb.bc', 'h1._7wc', 'h1', 'title',
            'div[class*="profile"] span[class*="name"]',
            'span[class*="profileName"]',
            'div[class*="profileName"]',
            'strong', 'span[class*="name"]'
        ]
        
        for selector in name_selectors:
            try:
                elem = soup.select_one(selector)
                if elem:
                    name = elem.text.strip()
                    if name and len(name) > 1 and "Facebook" not in name:
                        account.name = name
                        break
            except:
                continue
                
        # If name not found, try to get from title
        if not account.name:
            title = soup.find('title')
            if title:
                name = title.text.strip()
                if "Facebook" in name:
                    name = name.replace(' | Facebook', '').strip()
                    if name:
                        account.name = name
                        
        # Extract profile picture
        img_selectors = [
            'img.x.y.l.z', 'img[src*="profile"]', 'img[src*="fbcdn"]',
            'img.profilePic', 'img[alt*="profile"]', 'img[class*="profile"]'
        ]
        
        for selector in img_selectors:
            try:
                img = soup.select_one(selector)
                if img and img.get('src'):
                    src = img.get('src')
                    if 'profile' in src or 'fbcdn' in src:
                        account.profile_photo = ProfilePhoto(
                            url=src,
                            width=int(img.get('width', 0)) if img.get('width') else 0,
                            height=int(img.get('height', 0)) if img.get('height') else 0
                        )
                        break
            except:
                continue
                
        # Extract user ID - multiple methods
        # Method 1: From profile link
        profile_link = soup.find('a', href=re.compile(r'/profile\.php\?id=\d+'))
        if profile_link and profile_link.get('href'):
            match = re.search(r'id=(\d+)', profile_link.get('href'))
            if match:
                account.user_id = match.group(1)
                
        # Method 2: From canonical URL
        if not account.user_id:
            canonical = soup.find('link', {'rel': 'canonical'})
            if canonical and canonical.get('href'):
                match = re.search(r'facebook\.com/([^/?]+)', canonical.get('href'))
                if match:
                    potential = match.group(1)
                    if potential.isdigit():
                        account.user_id = potential
                    else:
                        account.username = potential
                        
        # Method 3: From og:url
        if not account.user_id:
            og_url = soup.find('meta', {'property': 'og:url'})
            if og_url and og_url.get('content'):
                match = re.search(r'facebook\.com/([^/?]+)', og_url.get('content'))
                if match:
                    potential = match.group(1)
                    if potential.isdigit():
                        account.user_id = potential
                    else:
                        account.username = potential
                        
        # Extract bio
        bio_meta = soup.find('meta', {'property': 'og:description'})
        if bio_meta and bio_meta.get('content'):
            account.bio = bio_meta.get('content')
            
        # Extract contact info
        contact_divs = soup.find_all('div', class_='bk bl')
        for div in contact_divs:
            text = div.text.strip()
            if '@' in text and not account.email:
                account.email = text
            elif re.search(r'\+?\d{8,}', text) and not account.phone:
                account.phone = text
                
        # Check if verified
        verified_elem = soup.find('span', class_='_5x8r')
        if verified_elem:
            account.is_verified = True
            
        # Set profile URL
        if account.user_id:
            account.profile_url = f"https://facebook.com/profile.php?id={account.user_id}"
        elif account.username:
            account.profile_url = f"https://facebook.com/{account.username}"
        else:
            account.profile_url = f"https://facebook.com/{query}"
            
        # Set status and confidence
        if account.name:
            account.status = "found"
            account.confidence_score = 0.9 if account.user_id else 0.7
        else:
            account.status = "partial"
            account.confidence_score = 0.3
            
        return account if account.name else None
        
    def close(self):
        """Close session"""
        if self.session:
            self.session.close()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SOCIAL MAPPER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SocialMapper:
    """Multi-platform social media mapper"""
    
    PLATFORMS = {
        'facebook': 'https://facebook.com/{}',
        'instagram': 'https://instagram.com/{}',
        'twitter': 'https://twitter.com/{}',
        'linkedin': 'https://linkedin.com/in/{}',
        'github': 'https://github.com/{}',
        'reddit': 'https://reddit.com/user/{}',
        'youtube': 'https://youtube.com/@{}',
        'tiktok': 'https://tiktok.com/@{}',
        'pinterest': 'https://pinterest.com/{}'
    }
    
    def __init__(self, checker: FacebookChecker):
        self.checker = checker
        self.results = []
        
    def find_by_name(self, first_name: str, last_name: str) -> Dict:
        """Find social media accounts by name"""
        full_name = f"{first_name} {last_name}"
        result = {
            "name": full_name,
            "first_name": first_name,
            "last_name": last_name,
            "facebook": None
        }
        
        # Search Facebook
        try:
            fb_result = self.checker.check_account(full_name)
            if fb_result.found and fb_result.account:
                result["facebook"] = {
                    "url": fb_result.account.profile_url,
                    "name": fb_result.account.name,
                    "id": fb_result.account.user_id,
                    "verified": fb_result.account.is_verified,
                    "email": fb_result.account.email,
                    "phone": fb_result.account.phone
                }
        except Exception as e:
            logger.debug(f"Facebook search failed for {full_name}: {e}")
            
        self.results.append(result)
        return result
        
    def batch_search(self, names: List[Tuple[str, str]], max_workers: int = 5) -> List[Dict]:
        """Batch search multiple names"""
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.find_by_name, first, last): (first, last)
                for first, last in names
            }
            
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    first, last = futures[future]
                    logger.error(f"Search failed for {first} {last}: {e}")
                    
        return results
        
    def export_results(self, format: str = "json") -> str:
        """Export results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = Path("social_mapper_results")
        results_dir.mkdir(exist_ok=True)
        
        if format == "json":
            filepath = results_dir / f"results_{timestamp}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str)
                
        elif format == "csv":
            filepath = results_dir / f"results_{timestamp}.csv"
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Facebook URL", "Facebook ID", "Verified", "Email", "Phone"])
                for result in self.results:
                    fb = result.get("facebook")
                    writer.writerow([
                        result["name"],
                        fb.get("url", "") if fb else "",
                        fb.get("id", "") if fb else "",
                        fb.get("verified", False) if fb else "",
                        fb.get("email", "") if fb else "",
                        fb.get("phone", "") if fb else ""
                    ])
                    
        elif format == "html":
            filepath = results_dir / f"results_{timestamp}.html"
            self._export_html(filepath)
            
        return str(filepath)
        
    def _export_html(self, filepath: Path):
        """Export results as HTML"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>METAØNEX - Social Mapper Results</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; max-width: 1200px; margin: 0 auto; }
                h1 { color: #1877f2; }
                .header { background: linear-gradient(135deg, #1877f2, #42b72a); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #1877f2; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
                tr:hover { background-color: #ddd; }
                .found { color: #28a745; font-weight: bold; }
                .not-found { color: #dc3545; }
                .verified { color: #1877f2; }
                .timestamp { color: #666; margin-top: 20px; }
                .badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
                .badge-found { background: #28a745; color: white; }
                .badge-verified { background: #1877f2; color: white; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 METAØNEX - Social Mapper Results</h1>
                <p>Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                <p>Tool: METAØNEX v9.0.0 | Author: SYLHETYHACKVENGER</p>
            </div>
            <table>
                <tr>
                    <th>Name</th>
                    <th>Facebook</th>
                    <th>Verified</th>
                    <th>Email</th>
                    <th>Phone</th>
                </tr>
        """
        
        for result in self.results:
            fb = result.get("facebook")
            if fb:
                verified = "✅ Yes" if fb.get("verified") else "No"
                html += f'''
                <tr>
                    <td><strong>{result["name"]}</strong></td>
                    <td class="found"><a href="{fb["url"]}" target="_blank">{fb["name"]}</a></td>
                    <td>{verified}</td>
                    <td>{fb.get("email", "N/A")}</td>
                    <td>{fb.get("phone", "N/A")}</td>
                </tr>
                '''
            else:
                html += f'''
                <tr>
                    <td><strong>{result["name"]}</strong></td>
                    <td class="not-found">❌ Not found</td>
                    <td>N/A</td>
                    <td>N/A</td>
                    <td>N/A</td>
                </tr>
                '''
                
        html += """
            </table>
            <div class="timestamp">
                <p>Total profiles searched: """ + str(len(self.results)) + """</p>
                <p>Found: """ + str(sum(1 for r in self.results if r.get("facebook"))) + """</p>
                <p><small>METAØNEX v9.0.0 | SYLHETYHACKVENGER (THE-ERROR808)</small></p>
            </div>
        </body>
        </html>
        """
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA EXPORTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DataExporter:
    """Export account data to various formats"""
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def export_account(self, account: AccountInfo, format: str = "json") -> Path:
        """Export account to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', account.name or account.user_id or "unknown")
        filename = f"{safe_name}_{timestamp}"
        
        if format == "json":
            filepath = self.output_dir / f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(account.to_dict(), f, indent=2, default=str)
                
        elif format == "csv":
            filepath = self.output_dir / f"{filename}.csv"
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(AccountInfo.csv_headers())
                writer.writerow(account.to_csv_row())
                
        elif format == "html":
            filepath = self.output_dir / f"{filename}.html"
            self._export_html(account, filepath)
            
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        return filepath
        
    def _export_html(self, account: AccountInfo, filepath: Path):
        """Export as HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>METAØNEX - Facebook Profile</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f0f2f5; }}
                .header {{ background: linear-gradient(135deg, #1877f2, #42b72a); color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; }}
                .section {{ background: white; margin: 20px 0; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .section h2 {{ color: #1877f2; margin-top: 0; border-bottom: 2px solid #1877f2; padding-bottom: 10px; }}
                .grid {{ display: grid; grid-template-columns: 150px 1fr; gap: 10px; padding: 10px 0; }}
                .label {{ font-weight: bold; color: #555; }}
                .verified {{ color: #1877f2; }}
                .status-badge {{ display: inline-block; padding: 3px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; }}
                .status-found {{ background: #28a745; color: white; }}
                .status-partial {{ background: #ffc107; color: white; }}
                .profile-pic {{ max-width: 150px; border-radius: 50%; border: 3px solid #1877f2; }}
                .timestamp {{ color: #999; font-size: 12px; margin-top: 20px; text-align: center; }}
                .work-item, .edu-item {{ padding: 10px; margin: 5px 0; background: #f8f9fa; border-radius: 5px; }}
                .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Facebook Profile</h1>
                <h2>{account.name or "Unknown"}</h2>
                <p>User ID: {account.user_id or "N/A"}</p>
                <p>Status: <span class="status-badge status-{account.status}">{account.status}</span></p>
            </div>
            
            <div class="section">
                <h2>📋 Profile Information</h2>
                <div class="grid">
                    <span class="label">Username:</span>
                    <span>{account.username or "N/A"}</span>
                    <span class="label">Profile URL:</span>
                    <span><a href="{account.profile_url}" target="_blank">{account.profile_url}</a></span>
                    <span class="label">Verified:</span>
                    <span class="verified">{"✅ Yes" if account.is_verified else "No"}</span>
                    <span class="label">Gender:</span>
                    <span>{account.gender or "N/A"}</span>
                    <span class="label">Birthday:</span>
                    <span>{account.birthday or "N/A"}</span>
                    <span class="label">Bio:</span>
                    <span>{account.bio or "N/A"}</span>
                </div>
            </div>
            
            <div class="section">
                <h2>📞 Contact Information</h2>
                <div class="grid">
                    <span class="label">Email:</span>
                    <span>{account.email or "N/A"}</span>
                    <span class="label">Phone:</span>
                    <span>{account.phone or "N/A"}</span>
                    <span class="label">Address:</span>
                    <span>{account.address or "N/A"}</span>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Statistics</h2>
                <div class="grid">
                    <span class="label">Friends:</span>
                    <span>{account.friends_count or "N/A"}</span>
                    <span class="label">Followers:</span>
                    <span>{account.followers_count or "N/A"}</span>
                    <span class="label">Posts:</span>
                    <span>{account.posts_count or "N/A"}</span>
                </div>
            </div>
            
            <div class="section">
                <h2>💼 Work History</h2>
                {self._format_work_html(account.work_history)}
            </div>
            
            <div class="section">
                <h2>🎓 Education</h2>
                {self._format_education_html(account.education_history)}
            </div>
            
            <div class="section">
                <h2>📸 Profile Picture</h2>
                <img src="{account.profile_photo.url if account.profile_photo else ''}" class="profile-pic" />
            </div>
            
            <div class="timestamp">
                <p>Scraped: {account.timestamp}</p>
                <p>Confidence Score: {account.confidence_score:.1%}</p>
                <p>Discovery Method: {account.discovery_method or "N/A"}</p>
            </div>
            
            <div class="footer">
                <p>Generated by METAØNEX v9.0.0 | SYLHETYHACKVENGER (THE-ERROR808)</p>
            </div>
        </body>
        </html>
        """
        
        # Format work history
        work_html = ""
        for work in account.work_history:
            work_html += f"""
            <div class="work-item">
                <strong>{work.company}</strong>
                <br>{work.role}
                <br><small>{work.start_date} - {work.end_date}</small>
                {f'<br><small>{work.location}</small>' if work.location else ''}
            </div>
            """
        
        # Format education
        edu_html = ""
        for edu in account.education_history:
            edu_html += f"""
            <div class="edu-item">
                <strong>{edu.school}</strong>
                <br>{edu.degree} {f'({edu.field_of_study})' if edu.field_of_study else ''}
                <br><small>{edu.start_date} - {edu.end_date}</small>
            </div>
            """
        
        html = html.format(work_history=work_html or "<p>No work history</p>", 
                          education=edu_html or "<p>No education history</p>")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
            
    def _format_work_html(self, work: List[WorkExperience]) -> str:
        """Format work history for HTML"""
        if not work:
            return "<p>No work history available</p>"
        html = ""
        for w in work:
            html += f"""
            <div style="margin: 5px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong>{w.company}</strong><br>
                {w.role}<br>
                <small>{w.start_date} - {w.end_date}</small>
                {f'<br><small>{w.location}</small>' if w.location else ''}
            </div>
            """
        return html
        
    def _format_education_html(self, edu: List[Education]) -> str:
        """Format education for HTML"""
        if not edu:
            return "<p>No education history available</p>"
        html = ""
        for e in edu:
            html += f"""
            <div style="margin: 5px 0; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong>{e.school}</strong><br>
                {e.degree} {f'({e.field_of_study})' if e.field_of_study else ''}<br>
                <small>{e.start_date} - {e.end_date}</small>
            </div>
            """
        return html
            
    def export_batch(self, accounts: List[AccountInfo], format: str = "json") -> List[Path]:
        """Export multiple accounts"""
        return [self.export_account(account, format) for account in accounts]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATABASE MANAGER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DatabaseManager:
    """SQLite database manager"""
    
    def __init__(self, db_path: str = "metaohex.db"):
        self.db_path = Path(db_path)
        self._initialize_db()
        
    @contextmanager
    def connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
            
    def _initialize_db(self):
        with self.connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    username TEXT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    gender TEXT,
                    birthday TEXT,
                    profile_url TEXT,
                    profile_picture TEXT,
                    verified INTEGER DEFAULT 0,
                    status TEXT,
                    discovered_at TIMESTAMP,
                    last_check TIMESTAMP,
                    confidence_score REAL DEFAULT 0.0,
                    source_url TEXT,
                    friends_count INTEGER DEFAULT 0,
                    followers_count INTEGER DEFAULT 0,
                    posts_count INTEGER DEFAULT 0
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT,
                    query_type TEXT,
                    found INTEGER DEFAULT 0,
                    account_id TEXT,
                    timestamp TIMESTAMP,
                    duration REAL,
                    error TEXT,
                    attempts INTEGER DEFAULT 1,
                    proxy_used TEXT,
                    user_agent TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS work_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id TEXT,
                    company TEXT,
                    role TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    location TEXT,
                    description TEXT,
                    is_current INTEGER DEFAULT 0,
                    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS education_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id TEXT,
                    school TEXT,
                    degree TEXT,
                    field_of_study TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    grade TEXT,
                    is_current INTEGER DEFAULT 0,
                    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
                )
            ''')
            
            conn.execute('CREATE INDEX IF NOT EXISTS idx_accounts_name ON accounts(name)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_accounts_email ON accounts(email)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_accounts_phone ON accounts(phone)')
            conn.commit()
            
    def save_account(self, account: AccountInfo) -> bool:
        try:
            with self.connection() as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO accounts (
                        id, username, name, email, phone, gender, birthday,
                        profile_url, profile_picture, verified, status,
                        discovered_at, last_check, confidence_score, source_url,
                        friends_count, followers_count, posts_count
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    account.user_id, account.username, account.name,
                    account.email, account.phone, account.gender,
                    account.birthday, account.profile_url,
                    account.profile_photo.url if account.profile_photo else "",
                    1 if account.is_verified else 0,
                    account.status, account.timestamp,
                    datetime.now().isoformat(),
                    account.confidence_score,
                    account.source_url,
                    account.friends_count,
                    account.followers_count,
                    account.posts_count
                ))
                
                # Save work history
                conn.execute('DELETE FROM work_history WHERE account_id = ?', (account.user_id,))
                for work in account.work_history:
                    conn.execute('''
                        INSERT INTO work_history (
                            account_id, company, role, start_date, end_date,
                            location, description, is_current
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        account.user_id, work.company, work.role,
                        work.start_date, work.end_date,
                        work.location, work.description,
                        1 if work.is_current else 0
                    ))
                    
                # Save education history
                conn.execute('DELETE FROM education_history WHERE account_id = ?', (account.user_id,))
                for edu in account.education_history:
                    conn.execute('''
                        INSERT INTO education_history (
                            account_id, school, degree, field_of_study,
                            start_date, end_date, grade, is_current
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        account.user_id, edu.school, edu.degree,
                        edu.field_of_study, edu.start_date, edu.end_date,
                        edu.grade, 1 if edu.is_current else 0
                    ))
                    
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Database save error: {e}")
            return False
            
    def save_search_result(self, result: SearchResult) -> bool:
        try:
            with self.connection() as conn:
                conn.execute('''
                    INSERT INTO search_history (
                        query, query_type, found, account_id, timestamp,
                        duration, error, attempts, proxy_used, user_agent
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    result.input_query,
                    result.query_type,
                    1 if result.found else 0,
                    result.account.user_id if result.account else '',
                    result.timestamp,
                    result.duration,
                    result.error,
                    result.attempts,
                    result.proxy_used,
                    result.user_agent
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Failed to save search result: {e}")
            return False
            
    def get_accounts(self) -> List[Dict]:
        with self.connection() as conn:
            return [dict(row) for row in conn.execute('SELECT * FROM accounts ORDER BY discovered_at DESC')]
            
    def get_statistics(self) -> Dict:
        with self.connection() as conn:
            stats = {}
            stats['total_accounts'] = conn.execute('SELECT COUNT(*) FROM accounts').fetchone()[0]
            stats['verified_accounts'] = conn.execute('SELECT COUNT(*) FROM accounts WHERE verified = 1').fetchone()[0]
            stats['total_searches'] = conn.execute('SELECT COUNT(*) FROM search_history').fetchone()[0]
            stats['found_count'] = conn.execute('SELECT COUNT(*) FROM search_history WHERE found = 1').fetchone()[0]
            stats['success_rate'] = (stats['found_count'] / stats['total_searches'] * 100) if stats['total_searches'] > 0 else 0
            return stats

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USER INTERFACE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MetaonexUI:
    """Complete user interface for METAØNEX"""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.db = DatabaseManager()
        self.exporter = DataExporter()
        self.checker = None
        self.current_account: Optional[AccountInfo] = None
        self.search_history: List[SearchResult] = []
        self.running = True
        self.use_proxy = False
        
    def run(self):
        """Main application loop"""
        if not RICH_AVAILABLE:
            return self._fallback_interface()
            
        self._show_banner()
        
        while self.running:
            try:
                choice = self._show_menu()
                self._handle_choice(choice)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
                logger.error(traceback.format_exc())
                
        self._cleanup()
        
    def _show_banner(self):
        """Show the METAØNEX banner"""
        self.console.clear()
        
        banner_text = Text.assemble(
            ("\n", ""),
            (BANNER, "cyan"),
            ("\n", ""),
            (f"📌 Author: {AUTHOR} ({HANDLE})\n", "yellow"),
            (f"📌 Version: {VERSION}\n", "green"),
            (f"📌 Description: {DESCRIPTION}\n", "white"),
            ("\n", ""),
            ("[dim]Use responsibly. Education and research only.[/dim]")
        )
        
        panel = Panel(banner_text, border_style="blue", padding=(1, 2))
        self.console.print(panel)
        
        # Show stats
        stats = self.db.get_statistics()
        if stats['total_accounts'] > 0:
            self.console.print(
                f"[dim]📊 Database: {stats['total_accounts']} accounts, "
                f"{stats['verified_accounts']} verified, {stats['total_searches']} searches[/dim]\n"
            )
            
    def _show_menu(self) -> str:
        """Show main menu"""
        menu = Panel(
            Align.left(
                Text.assemble(
                    ("📋 MAIN MENU\n", "bold cyan"),
                    ("─" * 40 + "\n", "blue"),
                    ("1. ", "yellow"), ("🔍 Search Account\n", "white"),
                    ("2. ", "yellow"), ("📦 Batch Search\n", "white"),
                    ("3. ", "yellow"), ("🌐 Social Mapper\n", "white"),
                    ("4. ", "yellow"), ("📜 View History\n", "white"),
                    ("5. ", "yellow"), ("📤 Export Data\n", "white"),
                    ("6. ", "yellow"), ("📈 Statistics\n", "white"),
                    ("7. ", "yellow"), ("⚙️ Settings\n", "white"),
                    ("8. ", "yellow"), ("ℹ️ About\n", "white"),
                    ("9. ", "yellow"), ("🚪 Exit\n", "white"),
                )
            ),
            title="[bold]Options[/bold]",
            border_style="cyan"
        )
        self.console.print(menu)
        
        return Prompt.ask("[bold cyan]Enter your choice[/bold cyan]")
        
    def _handle_choice(self, choice: str):
        """Handle menu choices"""
        handlers = {
            "1": self._search_account,
            "2": self._batch_search,
            "3": self._social_mapper,
            "4": self._view_history,
            "5": self._export_data,
            "6": self._show_statistics,
            "7": self._settings,
            "8": self._show_about,
            "9": self._exit
        }
        
        if choice in handlers:
            handlers[choice]()
        else:
            self.console.print("[red]Invalid choice[/red]")
            
    def _search_account(self):
        """Search a single account"""
        self.console.clear()
        self.console.print("[bold cyan]🔍 Search Facebook Account[/bold cyan]\n")
        
        query = Prompt.ask("[yellow]Enter email, phone, or username[/yellow]")
        
        if not query:
            return
            
        try:
            self.checker = FacebookChecker(use_proxy=self.use_proxy)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"[cyan]Checking {query}...[/cyan]", total=1)
                result = self.checker.check_account(query)
                progress.update(task, completed=1)
                
            self.search_history.append(result)
            
            if result.found and result.account:
                self.current_account = result.account
                self._display_account_info(result.account)
                
                # Save to database
                self.db.save_account(result.account)
                self.db.save_search_result(result)
                
                # Offer export
                if Confirm.ask("[yellow]Export this account?[/yellow]", default=True):
                    self._export_single_account()
            else:
                self.console.print(f"\n[red]❌ Account not found: {result.error}[/red]")
                
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
            logger.error(traceback.format_exc())
            
        finally:
            if self.checker:
                self.checker.close()
                
        input("\nPress Enter to continue...")
        
    def _display_account_info(self, account: AccountInfo):
        """Display account information"""
        self.console.print("\n")
        
        table = Table(title="📊 Account Information", box=box.ROUNDED)
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="white")
        
        table.add_row("Name", account.name or "N/A")
        table.add_row("User ID", account.user_id or "N/A")
        table.add_row("Username", account.username or "N/A")
        table.add_row("Profile URL", account.profile_url or "N/A")
        table.add_row("Verified", "✅ Yes" if account.is_verified else "No")
        table.add_row("Status", f"[green]{account.status}[/green]")
        table.add_row("Confidence", f"{account.confidence_score:.1%}")
        
        if account.email:
            table.add_row("Email", account.email)
        if account.phone:
            table.add_row("Phone", account.phone)
        if account.gender:
            table.add_row("Gender", account.gender)
        if account.birthday:
            table.add_row("Birthday", account.birthday)
        if account.bio:
            table.add_row("Bio", account.bio[:100] + "..." if len(account.bio) > 100 else account.bio)
            
        if account.friends_count:
            table.add_row("Friends", str(account.friends_count))
        if account.followers_count:
            table.add_row("Followers", str(account.followers_count))
            
        self.console.print(table)
        
        # Work history
        if account.work_history:
            self.console.print("\n[bold]💼 Work History:[/bold]")
            for work in account.work_history:
                current = " (Current)" if work.is_current else ""
                self.console.print(f"  • {work.company} - {work.role}{current}")
                
        # Education
        if account.education_history:
            self.console.print("\n[bold]🎓 Education:[/bold]")
            for edu in account.education_history:
                current = " (Current)" if edu.is_current else ""
                self.console.print(f"  • {edu.school} - {edu.degree}{current}")
                
    def _export_single_account(self):
        """Export single account"""
        if not self.current_account:
            self.console.print("[red]No account to export[/red]")
            return
            
        format_choice = Prompt.ask(
            "[yellow]Export format[/yellow]",
            choices=["json", "csv", "html"],
            default="json"
        )
        
        try:
            path = self.exporter.export_account(self.current_account, format_choice)
            self.console.print(f"[green]✅ Exported to: {path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Export failed: {e}[/red]")
            
    def _batch_search(self):
        """Batch search multiple accounts"""
        self.console.clear()
        self.console.print("[bold cyan]📦 Batch Search[/bold cyan]\n")
        
        self.console.print("[yellow]Enter queries (one per line). Press Enter twice to finish.[/yellow]")
        
        queries = []
        while True:
            line = input()
            if line == "":
                if queries:
                    break
                continue
            queries.append(line.strip())
            
        if not queries:
            self.console.print("[red]No queries entered[/red]")
            return
            
        self.console.print(f"\n[cyan]Searching {len(queries)} accounts...[/cyan]")
        
        results = []
        with Progress() as progress:
            task = progress.add_task("[cyan]Processing...", total=len(queries))
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                def search_single(query):
                    with FacebookChecker(use_proxy=self.use_proxy) as checker:
                        return checker.check_account(query)
                        
                future_to_query = {
                    executor.submit(search_single, q): q 
                    for q in queries
                }
                
                for future in as_completed(future_to_query):
                    query = future_to_query[future]
                    try:
                        result = future.result()
                        results.append(result)
                        self.search_history.append(result)
                        
                        # Save to database
                        if result.found and result.account:
                            self.db.save_account(result.account)
                        self.db.save_search_result(result)
                        
                        progress.update(task, advance=1)
                    except Exception as e:
                        self.console.print(f"[red]Error searching {query}: {e}[/red]")
                        progress.update(task, advance=1)
                        
        found = [r for r in results if r.found]
        not_found = [r for r in results if not r.found]
        
        self.console.print(f"\n[bold]Results:[/bold]")
        self.console.print(f"  [green]Found: {len(found)}[/green]")
        self.console.print(f"  [red]Not found: {len(not_found)}[/red]")
        
        if found:
            self.console.print("\n[cyan]Found accounts:[/cyan]")
            for r in found:
                self.console.print(f"  • {r.input_query} -> [green]{r.account.name or 'Unknown'}[/green]")
                
        if found and Confirm.ask("[yellow]Export all found accounts?[/yellow]", default=True):
            accounts = [r.account for r in found]
            format_choice = Prompt.ask(
                "[yellow]Export format[/yellow]",
                choices=["json", "csv", "html"],
                default="json"
            )
            try:
                paths = self.exporter.export_batch(accounts, format_choice)
                self.console.print(f"[green]✅ {len(paths)} accounts exported[/green]")
            except Exception as e:
                self.console.print(f"[red]Export failed: {e}[/red]")
            
        input("\nPress Enter to continue...")
        
    def _social_mapper(self):
        """Social mapper"""
        self.console.clear()
        self.console.print("[bold cyan]🌐 Social Mapper[/bold cyan]\n")
        
        self.console.print("[yellow]Enter names to search (format: First Last)[/yellow]")
        self.console.print("[dim]Example: John Doe[/dim]\n")
        
        names = []
        while True:
            line = input()
            if line == "":
                if names:
                    break
                continue
            parts = line.strip().split()
            if len(parts) >= 2:
                first = parts[0]
                last = " ".join(parts[1:])
                names.append((first, last))
            else:
                self.console.print("[red]Please enter both first and last name[/red]")
                
        if not names:
            self.console.print("[red]No valid names entered[/red]")
            return
            
        try:
            with FacebookChecker(use_proxy=self.use_proxy) as checker:
                mapper = SocialMapper(checker)
                
                with Progress() as progress:
                    task = progress.add_task("[cyan]Mapping...", total=len(names))
                    results = mapper.batch_search(names, max_workers=5)
                    progress.update(task, completed=len(results))
                    
                self.console.print("\n[bold]Results:[/bold]")
                for result in results:
                    fb = result.get("facebook")
                    if fb:
                        verified = " ✅" if fb.get("verified") else ""
                        self.console.print(f"  ✅ {result['name']} -> [green]{fb['name']}{verified}[/green] ({fb['url']})")
                    else:
                        self.console.print(f"  ❌ {result['name']} -> Not found")
                        
                if Confirm.ask("[yellow]Export mapper results?[/yellow]", default=True):
                    format_choice = Prompt.ask(
                        "Export format",
                        choices=["json", "csv", "html"],
                        default="html"
                    )
                    path = mapper.export_results(format_choice)
                    self.console.print(f"[green]✅ Results exported to: {path}[/green]")
                    
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
            logger.error(traceback.format_exc())
            
        input("\nPress Enter to continue...")
        
    def _view_history(self):
        """View search history"""
        self.console.clear()
        self.console.print("[bold cyan]📜 Search History[/bold cyan]\n")
        
        if not self.search_history:
            # Try to load from database
            with self.db.connection() as conn:
                history = conn.execute('''
                    SELECT query, query_type, found, timestamp, duration, proxy_used
                    FROM search_history
                    ORDER BY timestamp DESC
                    LIMIT 50
                ''').fetchall()
                
            if not history:
                self.console.print("[yellow]No search history[/yellow]")
                input("\nPress Enter to continue...")
                return
                
            # Convert to SearchResult objects
            for row in history:
                result = SearchResult(
                    input_query=row['query'],
                    query_type=row['query_type'],
                    found=bool(row['found']),
                    timestamp=row['timestamp'],
                    duration=row['duration'],
                    proxy_used=row['proxy_used']
                )
                self.search_history.append(result)
                
        table = Table(title=f"History ({len(self.search_history)} entries)")
        table.add_column("#", style="dim", width=4)
        table.add_column("Query", style="cyan")
        table.add_column("Type", style="yellow", width=8)
        table.add_column("Found", style="green", width=8)
        table.add_column("Duration", style="dim", width=10)
        table.add_column("Proxy", style="dim", width=15)
        table.add_column("Timestamp", style="dim")
        
        for i, result in enumerate(reversed(self.search_history), 1):
            found_status = "✅" if result.found else "❌"
            duration = f"{result.duration:.2f}s"
            timestamp = result.timestamp[:16] if result.timestamp else "N/A"
            proxy = result.proxy_used or "Direct"
            
            table.add_row(
                str(i),
                result.input_query,
                result.query_type or "unknown",
                found_status,
                duration,
                proxy[:15] + "..." if len(proxy) > 15 else proxy,
                timestamp
            )
            
        self.console.print(table)
        input("\nPress Enter to continue...")
        
    def _export_data(self):
        """Export data menu"""
        self.console.clear()
        self.console.print("[bold cyan]📤 Export Data[/bold cyan]\n")
        
        self.console.print("1. Export current account")
        self.console.print("2. Export all accounts from database")
        self.console.print("3. Back")
        
        choice = Prompt.ask("[bold cyan]Choice[/bold cyan]", choices=["1", "2", "3"])
        
        if choice == "1":
            if self.current_account:
                self._export_single_account()
            else:
                self.console.print("[red]No current account[/red]")
                
        elif choice == "2":
            accounts_data = self.db.get_accounts()
            if accounts_data:
                accounts = []
                for row in accounts_data:
                    account = AccountInfo(
                        user_id=row['id'],
                        username=row['username'],
                        name=row['name'],
                        email=row['email'],
                        phone=row['phone'],
                        gender=row['gender'],
                        birthday=row['birthday'],
                        profile_url=row['profile_url'],
                        is_verified=bool(row['verified']),
                        status=row['status'],
                        timestamp=row['discovered_at'],
                        confidence_score=row['confidence_score'] or 0.0,
                        source_url=row['source_url'] or '',
                        friends_count=row['friends_count'] or 0,
                        followers_count=row['followers_count'] or 0,
                        posts_count=row['posts_count'] or 0
                    )
                    accounts.append(account)
                    
                format_choice = Prompt.ask(
                    "[yellow]Export format[/yellow]",
                    choices=["json", "csv", "html"],
                    default="json"
                )
                try:
                    paths = self.exporter.export_batch(accounts, format_choice)
                    self.console.print(f"[green]✅ {len(paths)} accounts exported[/green]")
                except Exception as e:
                    self.console.print(f"[red]Export failed: {e}[/red]")
            else:
                self.console.print("[red]No accounts in database[/red]")
                
        input("\nPress Enter to continue...")
        
    def _settings(self):
        """Settings menu"""
        self.console.clear()
        self.console.print("[bold cyan]⚙️ Settings[/bold cyan]\n")
        
        settings_table = Table(title="Current Configuration")
        settings_table.add_column("Setting", style="cyan")
        settings_table.add_column("Value", style="white")
        settings_table.add_row("Proxy Usage", "✅ Enabled" if self.use_proxy else "❌ Disabled")
        settings_table.add_row("Database", "✅ Connected")
        settings_table.add_row("Rich UI", "✅ Available" if RICH_AVAILABLE else "❌ Not available")
        self.console.print(settings_table)
        
        self.console.print("\n[yellow]Options:[/yellow]")
        self.console.print("1. Toggle Proxy Usage")
        self.console.print("2. Back")
        
        choice = Prompt.ask("[bold cyan]Choice[/bold cyan]", choices=["1", "2"])
        
        if choice == "1":
            self.use_proxy = not self.use_proxy
            self.console.print(f"[green]Proxy usage {'enabled' if self.use_proxy else 'disabled'}[/green]")
            time.sleep(1)
            self._settings()
            
    def _show_statistics(self):
        """Show statistics"""
        self.console.clear()
        self.console.print("[bold cyan]📈 Statistics[/bold cyan]\n")
        
        stats = self.db.get_statistics()
        
        table = Table(title="Database Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Total Accounts", str(stats['total_accounts']))
        table.add_row("Verified Accounts", str(stats['verified_accounts']))
        table.add_row("Total Searches", str(stats['total_searches']))
        table.add_row("Found Accounts", str(stats['found_count']))
        table.add_row("Success Rate", f"{stats['success_rate']:.1f}%")
        self.console.print(table)
        
        self.console.print("\n[bold]System Information:[/bold]")
        self.console.print(f"Tool: {TOOL_NAME} v{VERSION}")
        self.console.print(f"Author: {AUTHOR} ({HANDLE})")
        self.console.print(f"Python Version: {sys.version.split()[0]}")
        self.console.print(f"Platform: {sys.platform}")
        self.console.print(f"Rich Available: {'✅' if RICH_AVAILABLE else '❌'}")
        self.console.print(f"Proxy Enabled: {'✅' if self.use_proxy else '❌'}")
        
        input("\nPress Enter to continue...")
        
    def _show_about(self):
        """Show about information"""
        self.console.clear()
        
        about_text = Text.assemble(
            (f"{TOOL_NAME}\n", "bold cyan"),
            (f"Version {VERSION}\n", "green"),
            ("\n", ""),
            (f"Author: {AUTHOR}\n", "yellow"),
            (f"Handle: {HANDLE}\n", "yellow"),
            ("\n", ""),
            ("[bold]Features:[/bold]\n", "white"),
            ("  • Account Checker (Email/Phone/Username)\n", "white"),
            ("  • Full Profile Extraction\n", "white"),
            ("  • Social Mapper (Multi-Platform)\n", "white"),
            ("  • Batch Processing with Threading\n", "white"),
            ("  • SQLite Database Storage\n", "white"),
            ("  • Multi-Format Export (JSON/CSV/HTML)\n", "white"),
            ("  • Proxy Support with Rotation\n", "white"),
            ("  • Rate Limiting & Anti-Detection\n", "white"),
            ("\n", ""),
            ("[bold red]⚠️ DISCLAIMER:[/bold red]\n"),
            ("[dim]For educational and research purposes only.\n"
             "Use responsibly and in accordance with Terms of Service.[/dim]")
        )
        
        panel = Panel(about_text, border_style="cyan", padding=(2, 4))
        self.console.print(panel)
        
        input("\nPress Enter to continue...")
        
    def _exit(self):
        """Exit application"""
        self.running = False
        
    def _cleanup(self):
        """Cleanup"""
        if self.console:
            self.console.print("\n[green]Thank you for using METAØNEX! Goodbye![/green]")
            
    def _fallback_interface(self):
        """Fallback CLI interface"""
        print("\n" + "="*70)
        print("METAØNEX - FACEBOOK INTELLIGENCE SUITE (Fallback Mode)")
        print("="*70 + "\n")
        print(f"Author: {AUTHOR} ({HANDLE})")
        print(f"Version: {VERSION}\n")
        
        while True:
            print("\nOptions:")
            print("1. Search Account")
            print("2. Batch Search")
            print("3. Social Mapper")
            print("4. View History")
            print("5. Statistics")
            print("6. Exit")
            
            choice = input("\nEnter choice: ").strip()
            
            if choice == "1":
                query = input("Enter email, phone, or username: ").strip()
                if query:
                    try:
                        with FacebookChecker() as checker:
                            result = checker.check_account(query)
                            if result.found and result.account:
                                print(f"\n✅ Account found!")
                                print(f"Name: {result.account.name}")
                                print(f"Profile: {result.account.profile_url}")
                                if result.account.email:
                                    print(f"Email: {result.account.email}")
                                if result.account.phone:
                                    print(f"Phone: {result.account.phone}")
                            else:
                                print(f"\n❌ Account not found: {result.error}")
                    except Exception as e:
                        print(f"Error: {e}")
                        
            elif choice == "2":
                print("Enter queries (one per line). Empty line to finish:")
                queries = []
                while True:
                    line = input()
                    if line == "" and queries:
                        break
                    elif line == "":
                        continue
                    queries.append(line)
                    
                if queries:
                    print(f"\nSearching {len(queries)} accounts...")
                    found = 0
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        def search(q):
                            with FacebookChecker() as checker:
                                return q, checker.check_account(q)
                        futures = [executor.submit(search, q) for q in queries]
                        for future in as_completed(futures):
                            try:
                                query, result = future.result()
                                if result.found:
                                    found += 1
                                    print(f"✅ {query} -> {result.account.name}")
                            except Exception as e:
                                print(f"❌ Error: {e}")
                    print(f"\nFound: {found}/{len(queries)}")
                    
            elif choice == "6":
                print("\nGoodbye!")
                break
                
            else:
                print("Invalid choice")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN ENTRY POINT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    """Main entry point"""
    try:
        app = MetaonexUI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
