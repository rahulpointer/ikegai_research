Certainly! Here is the full content from the previous conversation, formatted as a text file. You can copy and paste this into a file named `azure_key_vault_fastapi_setup.txt`.

**`azure_key_vault_fastapi_setup.txt`:**

```plaintext
# Azure Key Vault FastAPI Setup

## Directory Structure
```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routers
│   │   ├── __init__.py
│   │   ├── keyvault.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── keyvault_service.py
├── requirements.txt
└── README.md
```

## requirements.txt
```plaintext
fastapi
uvicorn
azure-identity
azure-keyvault-keys
python-dotenv
```

## app/config.py
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AZURE_VAULT_URL: str = os.getenv('AZURE_VAULT_URL')
    AZURE_CLIENT_ID: str = os.getenv('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET: str = os.getenv('AZURE_CLIENT_SECRET')
    AZURE_TENANT_ID: str = os.getenv('AZURE_TENANT_ID')

settings = Settings()
```

## app/main.py
```python
from fastapi import FastAPI
from app.routers import keyvault

app = FastAPI()

app.include_router(keyvault.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Azure Key Vault API"}
```

## app/routers/keyvault.py
```python
from fastapi import APIRouter, HTTPException
from app.services.keyvault_service import KeyVaultService
from azure.core.exceptions import ResourceNotFoundError

router = APIRouter(prefix="/keyvault", tags=["keyvault"])

keyvault_service = KeyVaultService()

@router.get("/keys/{key_name}")
async def get_key(key_name: str):
    try:
        key = keyvault_service.get_key(key_name)
        return key
    except ResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Key not found")

@router.post("/keys/{key_name}")
async def create_key(key_name: str):
    key = keyvault_service.create_key(key_name)
    return key

@router.delete("/keys/{key_name}")
async def delete_key(key_name: str):
    keyvault_service.delete_key(key_name)
    return {"message": "Key deleted"}

# Additional endpoints for other operations can be added here
```

## app/services/keyvault_service.py
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from app.config import settings

class KeyVaultService:
    def __init__(self):
        credential = DefaultAzureCredential()
        self.client = KeyClient(vault_url=settings.AZURE_VAULT_URL, credential=credential)

    def get_key(self, key_name: str):
        key = self.client.get_key(key_name)
        return {"name": key.name, "key_type": key.key_type, "key_operations": key.key_operations}

    def create_key(self, key_name: str):
        key = self.client.create_key(key_name, "RSA")
        return {"name": key.name, "key_type": key.key_type, "key_operations": key.key_operations}

    def delete_key(self, key_name: str):
        delete_operation = self.client.begin_delete_key(key_name)
        delete_operation.wait()
        return {"name": key_name, "status": "deleted"}

    # Additional methods for other operations can be added here
```

## .env
```plaintext
AZURE_VAULT_URL=https://<your-vault-name>.vault.azure.net/
AZURE_CLIENT_ID=<your-client-id>
AZURE_CLIENT_SECRET=<your-client-secret>
AZURE_TENANT_ID=<your-tenant-id>
```

## Running the Application
- Create a `.env` file in the root directory and populate it with your Azure Key Vault credentials.
- Run the FastAPI application using `uvicorn`:
  ```sh
  uvicorn app.main:app --reload
  ```
```

You can save this content into a text file named `azure_key_vault_fastapi_setup.txt`.
