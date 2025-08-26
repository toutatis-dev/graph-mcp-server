import httpx, asyncio, msal, requests, os
from dotenv import load_dotenv
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("graph-mcp", log_level="ERROR")
load_dotenv()

def get_auth_token():
    app = msal.ConfidentialClientApplication(
        client_id=os.getenv('GRAPH_CLIENT_ID'),
        client_credential=os.getenv('GRAPH_CLIENT_SECRET'),
        authority=os.getenv('GRAPH_AUTHORITY')
    )

    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    if result != None:
        if "access_token" in result:
            print("✅ Authentication successful!")
            return result
    return None
        
@mcp.tool(
    name="get_users_verbose",
    description="gets all users in entra, uses pagination"
) 
def get_users_verbose() -> Dict[str, Any] | None:
    """Makes get request to 'https://graph.microsoft.com/v1.0/users' with no select filters to get full JSON response"""
    users = None
    auth = get_auth_token()
    
    if auth is None:
        print("❌ Authentication failed - no token received")
        return None
        
    try:
        headers = {'Authorization': f'Bearer {auth["access_token"]}'}
        users = requests.get('https://graph.microsoft.com/v1.0/users', headers=headers).json()
    except Exception as e:
        print(f"get_users_verbose failed with error {e}")
    
    return users

@mcp.tool(
    name="get_groups_verbose",
    description="gets all groups in entra, uses pagination"
) 
def get_groups_verbose() -> Dict[str, Any] | None:
    """Makes get request to 'https://graph.microsoft.com/v1.0/groups' with no select filters to get full JSON response"""
    groups = None
    auth = get_auth_token()
    
    if auth is None:
        print("❌ Authentication failed - no token received")
        return None
        
    try:
        headers = {'Authorization': f'Bearer {auth["access_token"]}'}
        groups = requests.get('https://graph.microsoft.com/v1.0/groups', headers=headers).json()
    except Exception as e:
        print(f"get_groups_verbose failed with error {e}")
    
    return groups

@mcp.tool(
    name="make_group",
    description="Creates a new group in Microsoft Entra ID. Requires displayName, mailNickname, mailEnabled (bool), securityEnabled (bool), and description parameters."
) 
def make_group(displayName: str, mailNickname: str, mailEnabled: bool, securityEnabled: bool, description: str) -> Dict[str, Any] | None:
    """
    Creates a new group in Microsoft Entra ID by making a POST request to the Microsoft Graph API.
    
    Args:
        displayName: The display name for the group
        mailNickname: The mail nickname for the group
        mailEnabled: Whether the group is mail-enabled
        securityEnabled: Whether the group is security-enabled
        description: Description of the group
        
    Returns:
        Dict containing the created group information, or None if failed
    """
    
    auth = get_auth_token()
    
    if auth is None:
        print("❌ Authentication failed - no token received")
        return None
        
    jsonBody = {
        "displayName": displayName,
        "mailNickname": mailNickname,
        "mailEnabled": mailEnabled,
        "securityEnabled": securityEnabled,
        "description": description
    }
    
    try:
        headers = {'Authorization': f'Bearer {auth["access_token"]}'}
        response = requests.post('https://graph.microsoft.com/v1.0/groups', headers=headers, json=jsonBody)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"make_group failed with error {e}")
        return None
    
@mcp.tool(
    name="add_user_to_group",
    description="Adds a user to a group. Requires user ID and group name."
) 
def add_user_to_group(user_id: str, group_id: str) -> Dict[str, Any] | None:
    """
    Adds a user to a group in Microsoft Entra ID by making a POST request to the Microsoft Graph API.
    
    Args:
        user_id: the ID of the user,
        group_id: the ID of the group
        
    Returns:
        Dict containing the group membership data , or None if failed
    """
    
    auth = get_auth_token()
    
    if auth is None:
        print("❌ Authentication failed - no token received")
        return None
        
    jsonBody = {
        "@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"
    }
    
    try:
        headers = {'Authorization': f'Bearer {auth["access_token"]}'}
        response = requests.post(f'https://graph.microsoft.com/v1.0/groups/{group_id}/members/$ref', headers=headers, json=jsonBody)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"add_user_to_group failed with error {e}")
        return None

if __name__ == "__main__":
    mcp.run(transport="stdio")