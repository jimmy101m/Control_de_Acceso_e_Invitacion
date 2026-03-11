# AGENTS.md - Development Guidelines

## Build & Run Commands

### Development Server
```bash
# Activate virtual environment (Windows: venv\Scripts\activate, Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
uvicorn main:app --reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
```bash
# Run a single test
pytest path/to/test_file.py::test_function_name -v

# Run tests matching a pattern
pytest -k "test_name_pattern" -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### Database & Linting
- Database: `sqlite+aiosqlite:///./test.db`
- Linting: `ruff check .` / `ruff check --fix .`
- Type checking: `mypy .`
- Code format: `black --check .`

---

## Code Style

### Project Structure
```
├── main.py           # FastAPI entry point
├── auth/             # Authentication module
│   ├── Controller.py # Routes
│   ├── Service.py    # Business logic
│   └── Models.py     # Pydantic schemas
├── user/             # User management
│   ├── Controller.py
│   ├── Service.py
│   ├── Models.py
│   └── Util.py
├── entities/         # SQLAlchemy ORM models
│   ├── Base.py
│   ├── User.py
│   ├── Role.py
│   ├── invitacion.py
│   └── user_roles.py
└── database/
    └── database.py   # DB engine & session
```

### Imports (order: stdlib → third-party → local)
```python
from datetime import timedelta
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from database.database import DBDependency
from entities.User import User
from auth.Service import authenticate_user
```

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/vars: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Routes: kebab-case (`/users`, `/auth/token`)

### Pydantic Models
```python
from pydantic import BaseModel, EmailStr
from uuid import UUID

class CrearUsuario(BaseModel):
    name: str
    email: EmailStr
    phone: str
    password: str

class UsuarioResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True
```

### SQLAlchemy 2.0 Models
```python
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List, TYPE_CHECKING

from entities.Base import BaseClass

if TYPE_CHECKING:
    from entities.User import User

class Invitacion(BaseClass):
    __tablename__ = "Invitaciones"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), index=True)
    expired_at: Mapped[datetime] = mapped_column(index=True)
    token: Mapped[str] = mapped_column(unique=True, index=True)
    used: Mapped[bool] = mapped_column(default=False)
    invitado_por: Mapped["User"] = relationship(back_populates="invitaciones")
```

### Async/Await
- Use `async def` for all route handlers and DB operations
- Inject DB session via dependency:

```python
@router.post("/users", status_code=201, response_model=UsuarioResponse)
async def crear_usuario_endpoint(peticion: CrearUsuario, db: DBDependency):
    return await crear_usuario(peticion, db)
```

### Error Handling
```python
from fastapi import HTTPException, status

async def authenticate_user(email: str, password: str, db: Session):
    user = await get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password'
        )
    return user
```

### Authentication
- JWT tokens with `OAuth2PasswordBearer`
- Store secrets in environment variables (currently hardcoded)

```python
from fastapi.security import OAuth2PasswordBearer
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
```

### Password Handling (bcrypt)
```python
import bcrypt

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    pwd_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)
```

### Type Hints & DB Dependency
```python
from typing import Annotated
from fastapi import Depends

DBDependency = Annotated[AsyncSession, Depends(get_session)]

async def crear_usuario(peticion: CrearUsuario, db: DBDependency):
    nuevo_usuario = User(...)
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario
```

### Configuration
- Use environment variables
- Database URL: `sqlite+aiosqlite:///./test.db`
- Create `.env` for local development (gitignored)

---

## Testing
- Add tests to `tests/` directory with `conftest.py`
- Use pytest with async support

---

## Notes
- No existing tests in project
- No .cursor/rules, .cursorrules, or .github/copilot-instructions.md
- JWT secret is hardcoded - should move to `.env`
