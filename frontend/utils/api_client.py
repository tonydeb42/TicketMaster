"""
API Client for backend communication
Centralized request handling with error management
"""
import os
import requests
from typing import Optional, Dict, Any, List

# Get base URL from environment or use default
BASE_URL = os.getenv("BACKEND_BASE_URL", "http://localhost:8000")


class APIClient:
    """Centralized API client for all backend requests"""
    
    def __init__(self):
        self.base_url = BASE_URL.rstrip('/')
        self.timeout = 30  # seconds
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None
    ) -> tuple[bool, Any, Optional[str]]:
        """
        Make HTTP request to backend API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: JSON data for request body
            files: Files to upload
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (success: bool, response_data: Any, error_message: Optional[str])
        """
        url = f"{self.base_url}{endpoint}"
        timeout = timeout or self.timeout
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, timeout=timeout)
            elif method.upper() == "POST":
                if files:
                    response = requests.post(url, files=files, timeout=timeout)
                else:
                    response = requests.post(url, json=data, timeout=timeout)
            else:
                return False, None, f"Unsupported HTTP method: {method}"
            
            # Check response status
            if response.status_code in [200, 201]:
                try:
                    return True, response.json(), None
                except ValueError:
                    return True, response.text, None
            elif response.status_code == 400:
                error_msg = "Bad request. Please check your input."
                try:
                    error_data = response.json()
                    error_msg = error_data.get('detail', error_msg)
                except ValueError:
                    pass
                return False, None, error_msg
            elif response.status_code == 404:
                return False, None, "API endpoint not found. Please check backend URL."
            elif response.status_code == 422:
                error_msg = "Validation error. Please check your input format."
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        error_msg = str(error_data['detail'])
                except ValueError:
                    pass
                return False, None, error_msg
            elif response.status_code >= 500:
                return False, None, "Server error. Please try again later."
            else:
                return False, None, f"Request failed with status code {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, None, "Request timeout. The server is taking too long to respond."
        except requests.exceptions.ConnectionError:
            return False, None, f"Connection error. Cannot reach backend at {self.base_url}. Please check if the backend is running."
        except requests.exceptions.RequestException as e:
            return False, None, f"Network error: {str(e)}"
        except Exception as e:
            return False, None, f"Unexpected error: {str(e)}"
    
    def upload_csv(self, file_data, filename: str) -> tuple[bool, Any, Optional[str]]:
        """
        Upload CSV file for batch processing
        
        Args:
            file_data: File content
            filename: Name of the file
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        files = {'file': (filename, file_data, 'text/csv')}
        return self._make_request("POST", "/upload", files=files, timeout=60)
    
    def get_departments(self) -> tuple[bool, List[str], Optional[str]]:
        """
        Fetch list of available departments
        
        Returns:
            Tuple of (success, departments_list, error_message)
        """
        success, data, error = self._make_request("GET", "/departments")
        
        if success:
            if isinstance(data, list):
                return True, data, None
            elif isinstance(data, dict) and 'departments' in data:
                return True, data['departments'], None
            else:
                return False, [], "Invalid response format from departments endpoint"
        else:
            return False, [], error
    
    def create_ticket(self, query: str, department: str) -> tuple[bool, Any, Optional[str]]:
        """
        Create a new ticket
        
        Args:
            query: Problem description
            department: Selected department
            
        Returns:
            Tuple of (success, response_data, error_message)
        """
        data = {
            "query": query,
            "department": department
        }
        return self._make_request("POST", "/tickets", data=data)


# Create singleton instance
api_client = APIClient()
