# Microsoft Graph MCP Server

A Model Context Protocol (MCP) server for managing Microsoft Entra ID users and groups via the Microsoft Graph API.

## Features

- **get_users_verbose** - Retrieve all users with full details
- **get_groups_verbose** - Retrieve all groups with full details  
- **make_group** - Create new groups
- **add_user_to_group** - Add users to groups

## Prerequisites

- Python 3.13+
- Microsoft Entra ID application with Graph API permissions
- uv package manager

## Required Permissions

Your Entra ID app needs:
- `User.Read.All`
- `Group.ReadWrite.All` 
- `GroupMember.ReadWrite.All`

## Setup

1. Clone and install:
```bash
git clone https://github.com/toutatis-dev/graph-mcp-server.git
cd graph-mcp-server
uv install
```

2. Create `.env` file:
```env
GRAPH_CLIENT_ID=your_client_id
GRAPH_CLIENT_SECRET=your_client_secret
GRAPH_AUTHORITY=https://login.microsoftonline.com/your_tenant_id
```

## Usage

Run the MCP server:
```bash
uv run python main.py
```

## Development

Quality checks:
```bash
uv run black .
uv run flake8 .  
uv run mypy .
```